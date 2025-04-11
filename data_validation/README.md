# Great Expectations Data Validation

This directory contains scripts for data validation using Great Expectations.

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