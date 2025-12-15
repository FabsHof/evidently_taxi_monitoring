from evidently import ColumnMapping
from src.utils.logging import log_warning
import pandas as pd
from evidently.report import Report
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric

def generate_report(train_data: pd.DataFrame, val_data: pd.DataFrame, num_features: list[str], cat_features: list[str]):
    '''
    Generates an Evidently report to analyze data drift and missing values between training and validation datasets.
    Args:
        train_data (pd.DataFrame): The training dataset.
        val_data (pd.DataFrame): The validation dataset.
        num_features (list[str]): List of numerical feature column names.
        cat_features (list[str]): List of categorical feature column names.
    Returns:
        Report: The generated Evidently report.
    '''
    # Define the column mapping for the Evidently report
    # This includes the prediction column, numerical features, and categorical features
    column_mapping = ColumnMapping(
        target=None,
        prediction='prediction',
        numerical_features=num_features,
        categorical_features=cat_features
    )

    # Initialize the Evidently report with the desired metrics
    # In this case, we're using the ColumnDriftMetric for the 'prediction' column,
    # the DatasetDriftMetric to measure drift across the entire dataset,
    # and the DatasetMissingValuesMetric to measure the proportion of missing values
    report = Report(metrics=[
        ColumnDriftMetric(column_name='prediction'),
        DatasetDriftMetric(),
        DatasetMissingValuesMetric()
    ])

    # Run the report on the training and validation data
    # The training data is used as the reference data, and the validation data is the current data
    report.run(reference_data=train_data, current_data=val_data, column_mapping=column_mapping)
    # Return the generated report
    return report

if __name__ == '__main__':
    log_warning('This module is intended to be imported and used within the main pipeline.')