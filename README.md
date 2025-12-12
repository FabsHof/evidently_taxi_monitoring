# evidently_taxi_monitoring

Grafana & Evidently used for taxi model drift monitoring

# 📊 Data

The dataset used for this project is the [NYC Taxi Trip dataset]()

| Variable | Description | Informatic type |
|----------|-------------|-----------------|
| VendorID | Supplier ID | int64 |
| lpep_pickup_datetime | Race start time | datetime64[us] |
| lpep_dropoff_datetime | Race end time | datetime64[us] |
| store_and_fwd_flag | Indicates whether the data was stored before transmission | object |
| RatecodeID | Applicable tariff identifier | int64 |
| PULocationID | Pickup Location Identifier | int64 |
| DOLocationID | Drop-off location identifier | int64 |
| passenger_count | Number of passengers | int64 |
| trip_distance | Distance covered during the race | float64 |
| fare_amount | Basic fare of the race | float64 |
| extra | Additional Charges | float64 |
| mta_tax | Metropolitan Transport Authority Tax | float64 |
| tip_amount | Tip given to the driver | float64 |
| tolls_amount | Toll charges during the race | float64 |
| ehail_fee | Fee for electronic reservation (all zero values) | object |
| improvement_surcharge | Supplement for improvements | float64 |
| total_amount | Total amount of the trip | float64 |
| payment_type | Payment Method | int64 |
| trip_type | Type of trip | int64 |
| congestion_surcharge | Supplement during periods of heavy traffic | float64 |


# 🚀 Getting Started

## Installation
1. Install uv: [Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)
2. Get dependencies:
   ```bash
   uv sync
   ```
3. Set up environment variables:
   - Copy the `.env.example` file to `.env`
   - Edit values as needed

## Usage
1. Download datasets:
   ```bash
   make step_1_download_data
   ```
     