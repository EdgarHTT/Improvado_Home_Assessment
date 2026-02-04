### fact_marketing_performance
| Field Name | Data Type | Description |
|---|---|---|
| date_id | int | ID corresponding to a date in dim_date |
| campaign_id | int | ID corresponding to a campaing in dim_campaign |
| data_source_id | int | ID corresponding to a data source in dim_data_source |
| impressions | int | Number of times ads were shown |
| reach | int | The number of unique, individual viewers |
| clicks | int | Number of user clicks |
| video_views | int | Amount of daily views for videos (where applicable) |
| cost | float | daily cost of the ad campaign |
| conversions | int | Desired actions completed |

### dim_campaign
| Field Name | Data Type | Description |
|---|---|---|
| campaign_id | int | ID corresponding to a campaign |
| campaign_name | string | Name of the campaign |
| channel_id | int | ID corresponding to the pathway of communication |
| objective | string | Objective of the campaign |
| start_date | date | Start date of the campaign (YYYY-MM-DD format) |
| end_date | date | End date of the campaign (YYYY-MM-DD format) |
| status | string | Status of the campaign | 

### dim_channel
| Field Name | Data Type | Description |
|---|---|---|
| channel_id | int | ID corresponding to the pathway of communication |
| channel_name | string | Name of the channel |

### dim_data_source
| Field Name | Data Type | Description |
|---|---|---|
| data_source_id | int | ID corresponding to the data source |
| data_source_name | string | Name of the data source |
| platform_type | string | Asociated platform type |

### dim_date
| Field Name | Data Type | Description |
|---|---|---|
| date_id | int | Id of a unique date |
| date | date | Date in YYYY-MM-DD format |
| day | int | Day of the month |
| month | int | Month in integer |
| month_name | string | Name of the month |
| quarter | int | Corresponding quarter of the year |
| year | int | Year |
| week | int | Week of the year |
