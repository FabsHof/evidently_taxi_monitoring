import pandas as pd
import os
from os import path
from src.utils.logging import log_info, log_error, log_warning
from dotenv import load_dotenv

load_dotenv()

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Preprocesses the taxi trip data.
    Args:
        df (pd.DataFrame): The raw taxi trip data.
    Returns:
        pd.DataFrame: The preprocessed taxi trip data.
    '''
    # Calculate the duration of each trip in minutes
    df['duration_min'] = (df.lpep_dropoff_datetime - df.lpep_pickup_datetime).dt.total_seconds() / 60

    # Filter out trips with unrealistic durations
    df = df[(df.duration_min >= 0) & (df.duration_min <= 60)]

    # Filter out trips with unrealistic passenger counts
    df = df[(df.passenger_count > 0) & (df.passenger_count <= 8)]

    return df

def main(raw_data_dir: str, processed_data_dir: str, valid_file_formats: list = ['parquet', 'csv']) -> None:
    '''
    Main function to load, preprocess, and save the data.
    Args:
        raw_data_dir (str): Directory where raw data files are stored.
        processed_data_dir (str): Directory where processed data files will be saved.
        valid_file_formats (list): List of valid file formats to process.
    Returns:
        None
    '''
    os.makedirs(processed_data_dir, exist_ok=True)

    for file in os.listdir(raw_data_dir):
        if any(file.endswith(ext) for ext in valid_file_formats):
            file_path = path.join(raw_data_dir, file)
            if file.endswith('parquet'):
                df = pd.read_parquet(file_path)
            elif file.endswith('csv'):
                df = pd.read_csv(file_path)
            else:
                log_warning(f'Skipping unsupported file format: {file}')
                continue

            preprocessed_df = preprocess_data(df)
            output_path = path.join(processed_data_dir, f'processed_{file}')
            preprocessed_df.to_parquet(output_path, index=False)
            log_info(f'Preprocessed data saved to {output_path}')

if __name__ == '__main__':
    raw_data_dir = os.getenv('RAW_DATA_DIR', 'data/raw')
    processed_data_dir = os.getenv('PROCESSED_DATA_DIR', 'data/processed')
    main(raw_data_dir, processed_data_dir)