import os
from os import path
import pandas as pd
from src.utils.logging import log_info
from src.step_1_download_data import download_files
from src.step_2_load_and_process_data import load_and_process_data
from src.step_3_train_and_evaluate_model import train_and_evaluate
from src.step_4_generate_report import generate_report

from dotenv import load_dotenv

load_dotenv()

def run_step4_generate_report(train_data: pd.DataFrame, val_data: pd.DataFrame, num_features: list[str], cat_features: list[str], report_path: str) -> None:
    log_info('ℹ️ Starting Step 4: Generate Report')
    report = generate_report(train_data, val_data, num_features, cat_features)
    os.makedirs(path.dirname(report_path), exist_ok=True)
    report.save_html(report_path)
    log_info(f'✅ Completed Step 4: Generate Report. Report saved to {report_path}')

def run_step3_train_and_evaluate_model(processed_data_dir: str, models_dir: str, features: list[str], target: str, valid_file_formats: list[str], base_model_path: str = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    log_info('ℹ️ Starting Step 3: Train and Evaluate Model')
    _, results = train_and_evaluate(processed_data_dir, models_dir, features, target, base_model_path=base_model_path, valid_file_formats=valid_file_formats)
    _, _, _, X_train, X_val, y_train, y_val = results[-1]
    log_info('✅ Completed Step 3: Train and Evaluate Model')
    return (X_train, X_val)

def run_step2_preprocess_data(raw_data_dir: str, processed_data_dir: str, valid_file_formats: list):
    log_info('ℹ️ Starting Step 2: Preprocess Data')
    load_and_process_data(raw_data_dir, processed_data_dir, valid_file_formats)
    log_info('✅ Completed Step 2: Preprocess Data')
    

def run_step1_download_data(data_urls: list[str], raw_data_dir: str):
    log_info('ℹ️ Starting Step 1: Download Data')
    download_files(data_urls, raw_data_dir)
    log_info('✅ Completed Step 1: Download Data')

def main():
    data_urls = [url.strip() for url in os.getenv('DATASET_URLS', '').split(',')]
    valid_file_formats = [ext.strip() for ext in os.getenv('VALID_FILE_FORMATS', '.csv,.parquet').split(',')]
    raw_data_dir = os.getenv('RAW_DATA_DIR', 'data/raw')
    processed_data_dir = os.getenv('PROCESSED_DATA_DIR', 'data/processed')

    models_dir = os.getenv('MODELS_DIR', 'models')
    num_features = [feat.strip() for feat in os.getenv('MODEL_FEAT_NUM', 'passenger_count,trip_distance,fare_amount,total_amount').split(',')]
    cat_features = [feat.strip() for feat in os.getenv('MODEL_FEAT_CAT', 'PULocationID,DOLocationID').split(',')]
    target = os.getenv('MODEL_TARGET', 'duration_min')
    report_path = os.getenv('REPORT_PATH', 'reports/data_drift_report.html')

    # Run the complete pipeline
    run_step1_download_data(data_urls, raw_data_dir)
    run_step2_preprocess_data(raw_data_dir, processed_data_dir, valid_file_formats)
    X_train, X_val = run_step3_train_and_evaluate_model(processed_data_dir, models_dir, num_features + cat_features, target, valid_file_formats=valid_file_formats)
    run_step4_generate_report(X_train, X_val, num_features, cat_features, report_path)

if __name__ == '__main__':
    main()