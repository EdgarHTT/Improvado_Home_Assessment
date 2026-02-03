# Libraries
import numpy as np
import pandas as pd
import yaml
from faker import Faker

# Loading Config
with open("./data_generation/config.yaml", "r") as stream:
    config = yaml.safe_load(stream)

np.random.seed(config["random_seed"])
Faker.seed(config["random_seed"])

output_dir = "./data/processed/"

# Generating dim_date
dates = pd.date_range(
    config["date_range"]["start"],
    config["date_range"]["end"],
    freq="D"
)

dim_date = pd.DataFrame({
    "date_id": range(1, len(dates) + 1),
    "date": dates,
    "day": dates.day,
    "month": dates.month,
    "month_name": dates.month_name(),
    "quarter": dates.quarter,
    "year": dates.year,
    "week": dates.isocalendar().week
})

dim_date.to_csv(output_dir + "dim_date.csv", index=False)

# Generate dim_channel
channels = list(config['channels'].keys())

dim_channel = pd.DataFrame({
    "channel_id": range(1, len(channels) + 1),
    "channel_name": channels
})

dim_channel.to_csv(output_dir + "dim_channel.csv", index=False)

channel_id_map = dict(zip(dim_channel.channel_name, dim_channel.channel_id))

# Generating dim_data_source
data_sources = []
data_source_id = 1

for channel, sources in config["data_sources"].items():
    for source in sources:
        data_sources.append({
            "data_source_id": data_source_id,
            "data_source_name": source,
            "platform_type": channel
        })
        data_source_id += 1

dim_data_source = pd.DataFrame(data_sources)
dim_data_source.to_csv(output_dir + "dim_data_source.csv", index=False)

# Generate dim_campaign
campaigns = []
campaign_id = 1
fake = Faker()

for channel, campaign_cfg in config["campaigns"].items():
    for i in range(campaign_cfg["count"]):
        campaigns.append({
            "campaign_id": campaign_id,
            "campaing_name": fake.bs(),
            "channel_id": channel_id_map[channel],
            "objective": np.random.choice(campaign_cfg["objectives"]),
            "start_date": config['date_range']['start'],
            "end_date": config["date_range"]['end'],
            "status": "Active"
        })
        campaign_id += 1

dim_campaign = pd.DataFrame(campaigns)
dim_campaign.to_csv(output_dir + "dim_campaign.csv", index=False)

# Generate fact_marketing_performance
fact_rows = []

for _, date_row in dim_date.iterrows():
    date_id = date_row["date_id"]
    month = date_row["month"]

    for _, campaign in dim_campaign.iterrows():

        channel_name = dim_channel.loc[
            dim_channel.channel_id == campaign.channel_id,
            "channel_name"
        ].values[0]

        channel_cfg = config["channels"][channel_name]

        # Impressions
        impressions = int(
            channel_cfg["base_impressions"] *
            np.random.normal(1, config["daily_variation"]["std_dev"])
        )
        impressions = max(impressions, 1)

        # Seasonality adjustments
        if config["seasonality"]["enabled"]:
            if month == 12:
                impressions = int(impressions * config["seasonality"]["q4_multiplier"])
            if month in [6, 7]:
                impressions = int(impressions * config["seasonality"]["summer_dip_multiplier"])
        
        # Reach (must be <= impressions)
        reach = int(impressions * np.random.uniform(0.4, 0.9))
        reach = max(reach, 1)

        # clicks, costs and conversions i calculated by desired CTR, CPC and CVR range
        # Clicks
        ctr = np.random.uniform(*channel_cfg["ctr_range"])
        clicks = int(impressions * ctr)

        # Cost
        cpc = np.random.uniform(*channel_cfg["cpc_range"])
        cost = clicks * cpc

        # Organic channels has no cost
        if channel_name == "Organic":
            cost = 0

        # Conversions
        conv_rate = np.random.uniform(*channel_cfg["conversion_rate_range"])
        conversions = int(clicks * conv_rate)

        if clicks < config["rules"]["min_clicks_before_conversions"]:
            conversions = 0

        # Video views (where it makes sense)
        if channel_name in ["Paid Social", "Programmatic"]:
            video_views = int(impressions * np.random.uniform(0.1, 0.6))
        else:
            video_views = 0

        # Create rows per source
        for _, source in dim_data_source[
            dim_data_source.platform_type == channel_name
        ].iterrows():
            
            fact_rows.append({
                "date_id": date_id,
                "campaign_id": campaign.campaign_id,
                "data_source_id": source.data_source_id,
                "impressions": impressions,
                "reach": reach,
                "clicks": clicks,
                "video_views": video_views,
                "cost": round(cost, 2),
                "conversions": conversions
            })

fact_marketing = pd.DataFrame(fact_rows)

fact_marketing.to_csv(output_dir + "fact_marketing_performance.csv", index=False)

print("Finished dummy generation :)")