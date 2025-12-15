import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from typing import Tuple
from src.utils.logging import log_info, log_warning
from src.utils.timestamp import remove_timestamp_from_filename, add_current_timestamp_to_filename
import joblib
import argparse
import os
from os import path

def train_and_evaluate_df(df: pd.DataFrame, features: list[str], target: str, model: LinearRegression = None, split_ratio: float = 0.2) -> Tuple[LinearRegression, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    '''
    Trains and evaluates a Linear Regression model on the given dataframe.
    Args:
        df (pd.DataFrame): The preprocessed taxi trip data.
        features (list[str]): List of feature column names.
        target (str): Target variable column name.
        model (LinearRegression, optional): An existing Linear Regression model to continue training. Defaults to None.
        split_ratio (float, optional): The ratio of data to use for validation. Defaults to 0.2.
    Returns:
        Tuple[LinearRegression, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]: The trained model, training features, validation features, training target, validation target.
    '''
    # Split the data into features and target variable
    X = df[features]
    y = df[target]

    # Split the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=split_ratio, random_state=42)
    log_info(f'Data split into training and validation sets with ratio {1 - split_ratio}:{split_ratio}')

    # Initialize and train a Linear Regression model
    if model is None:
        model = LinearRegression()
        log_info('Initializing new Linear Regression model')
    model.fit(X_train, y_train)

    # Make predictions on the training and validation sets
    train_preds = model.predict(X_train)
    val_preds = model.predict(X_val)
    log_info('Model training complete and predictions made on training and validation sets')

    # Add the prediction column to the training and validation dataframes
    X_train['prediction'] = train_preds
    X_val['prediction'] = val_preds

    # Print the mean absolute error of the model on the training and validation data
    log_info(f'Model Evaluation:\nTraining Mean Absolute Error: {mean_absolute_error(y_train, train_preds):.2f}\nValidation Mean Absolute Error: {mean_absolute_error(y_val, val_preds):.2f}')

    # Return the trained model and the training and validation data
    return model, X_train, X_val, y_train, y_val

def train_and_evaluate(processed_data_dir: str, models_dir: str, features: list[str], target: str, base_model_path: str = None, save_per_epoch: bool = True, valid_file_formats: list[str] = ['.csv', '.parquet']) -> list[Tuple[str, str, LinearRegression, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]]:
    '''
    Main function to load processed data files, train and evaluate the model.
    Args:
        processed_data_dir (str): Directory where processed data files are stored.
        models_dir (str): Directory where models will be saved.
        features (list[str]): List of feature column names.
        target (str): Target variable column name.
        base_model_path (str, optional): Path to an existing model file to continue training. Defaults to None.
        save_per_epoch (bool, optional): Whether to save the model after each epoch. Defaults to True.
        valid_file_formats (list[str], optional): List of valid file formats to process. Defaults to ['.csv', '.parquet'].
    Returns:
        Tuple[str, list[Tuple[str, str, LinearRegression, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]]]: The filename of the last saved model and a list of results for each processed file.
    '''
    model = None
    model_name = 'linear_regression_model.bin'
    if base_model_path:
        try:
            model = joblib.load(base_model_path)
            model_name = os.path.basename(base_model_path)
            log_info(f'Loaded base model from {base_model_path}')
        except Exception as e:
            log_warning(f'Error loading model from {base_model_path}: {e}')
    
    os.makedirs(models_dir, exist_ok=True)

    results = []
    # Get all files in the processed data directory, concat
    supported_files = [f for f in os.listdir(processed_data_dir) if any(f.endswith(ext) for ext in valid_file_formats)]
    num_files = len(supported_files)
    log_info(f'Found {num_files} files to process in {processed_data_dir}')
    for i, file in enumerate(supported_files):
        is_last_file = (i == num_files - 1)
        processed_file_path = os.path.join(processed_data_dir, file)
        log_info(f'Processing file {i + 1}/{num_files}: {processed_file_path}')
        # Load the processed data file
        if file.endswith('.parquet'):
            df = pd.read_parquet(processed_file_path)
        elif file.endswith('.csv'):
            df = pd.read_csv(processed_file_path)
        else:
            log_warning(f'Skipping unsupported file format: {file}')
            continue

        # Train and evaluate the model
        model, X_train, X_val, y_train, y_val = train_and_evaluate_df(df, features, target, model=model)

        # Save at least the last model, or every epoch if specified
        model_filename = ''
        if save_per_epoch or is_last_file:
            model_filename = add_current_timestamp_to_filename(remove_timestamp_from_filename(model_name))
            joblib.dump(model, os.path.join(models_dir, model_filename))
            log_info(f'Saving {"epoch" if save_per_epoch else "final"} model to {os.path.join(models_dir, model_filename)}')
        results.append((os.path.basename(file), model_filename, model, X_train, X_val, y_train, y_val))
    
    # Return the filename of the last saved model and all results
    last_model_filename = results[-1][1] if results else ''
    return last_model_filename, results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train and evaluate a Linear Regression model on taxi trip data.')
    parser.add_argument('--processed_data_dir', type=str, default='data/processed', help='Directory where processed data files are stored.')
    parser.add_argument('--models_dir', type=str, default='models', help='Directory where models will be saved.')
    parser.add_argument('--valid_file_formats', type=str, nargs='+', default=['.csv', '.parquet'], help='List of valid file formats to process.')
    parser.add_argument('--base_model_path', type=str, help='Path to an existing model file.')
    parser.add_argument('--target', type=str, default='duration_min', help='Target variable for prediction.')
    parser.add_argument('--features', type=str, nargs='+', default=['passenger_count', 'trip_distance', 'fare_amount', 'total_amount', 'PULocationID', 'DOLocationID'], help='List of feature names.')
    args = parser.parse_args()

    last_model_filename, results = train_and_evaluate(args.processed_data_dir, args.models_dir, args.features, args.target, base_model_path=args.base_model_path, valid_file_formats=args.valid_file_formats)
    log_info(f'Final model saved as: {last_model_filename}')
    for file_name, model_file, model, X_train, X_val, y_train, y_val in results:
        log_info(f'File: {file_name}, Model saved as: {model_file}')
        # Store validation data for further analysis if needed
        model_file_base = f'validation_data_{path.splitext(model_file)[0] if model_file else ""}.parquet'
        model_file_base = add_current_timestamp_to_filename(remove_timestamp_from_filename(model_file_base))
        X_val.copy().to_parquet(os.path.join(args.models_dir, model_file_base), index=False)
        log_info(f'Saved validation data to {os.path.join(args.models_dir, model_file_base)}')




    