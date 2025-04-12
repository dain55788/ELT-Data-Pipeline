# OpenAQ Data Validation

This directory contains scripts for validating OpenAQ data using Great Expectations.

## Data Validation Workflow

The data validation process follows these steps:

1. Connect to the PostgreSQL database (OpenAQ_DWH)
2. Define data quality expectations for the stg_measurement_by_sensors table
3. Create a validation checkpoint to run all expectations
4. Execute the validation process
5. If validation passes, save results to the database
6. Generate data quality documentation

## Scripts

### openaq_data_validation.py

Main script for running data validation. This script:

- Connects to PostgreSQL database
- Defines expectations for the OpenAQ measurement data
- Creates a validation checkpoint
- Runs the validation
- Saves results to the data_quality.validation_results table

To run:

```bash
python openaq_data_validation.py
```

### check_validation_results.py

Script to check and display validation results stored in the database.

To run:

```bash
python check_validation_results.py
```

This will display:
- Recent validation runs
- Success rates
- Detailed information about failures

## Expectations

The following data quality expectations are validated:

| Expectation | Description |
|-------------|-------------|
| ExpectColumnValuesToNotBeNull | Ensures critical columns have values |
| ExpectColumnValuesToBeUnique | Ensures sensor_id values are unique |
| ExpectColumnValuesToBeInSet | Validates parameter names against allowed values |
| ExpectColumnValuesToBeOfType | Validates data types (e.g., measurement values are FLOAT) |
| ExpectColumnValuesToBeBetween | Validates geographic coordinates are in expected ranges |

## Database Schema

Validation results are stored in:

```
data_quality.validation_results
```

Schema:
- id: Serial primary key
- validation_time: Timestamp when validation was run
- table_name: Name of validated table
- success: Boolean indicating overall validation success
- expectation_count: Total number of expectations checked
- successful_expectations: Number of passed expectations
- failed_expectations: Number of failed expectations
- validation_result_json: Full JSON result of validation

## Integration with ELT Pipeline

This validation is designed to be run as a quality gate before data processing:

1. Extract and load data from source
2. Run data validation
3. Only proceed with transformation if validation passes
4. Log validation results for monitoring and reporting

## Issue with Python 3.11

The original notebook (`openaq_data_quality.ipynb`) was encountering an error because Great Expectations 1.3.14 is not fully compatible with Python 3.11. The error was:

```
AttributeError: 'FileDataContext' object has no attribute 'add_or_update_expectation_suite'
```

## Solution

I've created a fixed version of the script (`openaq_data_quality_fixed.py`) that uses the correct API for Great Expectations 1.3.14 with Python 3.11. The main changes are:

1. Using `context.create_expectation_suite()` instead of `context.add_or_update_expectation_suite()`
2. Using the validator object to add expectations instead of the batch object
3. Using `column` parameter instead of `columns` in the expectation methods

## How to Run

You can run the fixed script with:

```bash
python data_validation/openaq_data_quality_fixed.py
```

## Alternative Solutions

If you continue to have issues with Great Expectations and Python 3.11, you have a few options:

1. **Downgrade Python**: Create a virtual environment with Python 3.10, which is fully supported by Great Expectations 1.3.14
2. **Use an older version of Great Expectations**: Try version 0.15.x which might have better compatibility with Python 3.11
3. **Wait for an update**: Great Expectations team might release a version with full Python 3.11 support in the future

## Notes

- The script connects to a PostgreSQL database named `OpenAQ_DWH` with a table `stg_measurement_by_sensors` in the `staging` schema
- It validates various aspects of the data including non-null values, data types, and value ranges
- The validation results are saved and can be viewed in the Great Expectations Data Docs 