import pandas as pd
import streamlit as st
from io import BytesIO


def load_data_from_file(uploaded_file):
    """
    Load data from uploaded CSV or Excel file
    """
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            return None, "Unsupported file format. Please upload CSV or Excel."

        # Check required columns
        required_columns = ['first_name', 'email']
        missing_columns = [
            col for col in required_columns if col not in df.columns]

        if missing_columns:
            return None, f"Missing required columns: {', '.join(missing_columns)}"

        return df, "Data loaded successfully!"

    except Exception as e:
        return None, f"Error loading file: {str(e)}"


def load_sample_data():
    """
    Load sample data for demonstration
    """
    return pd.read_csv('data/sample_contacts.csv')


def validate_email_format(email):
    """
    Basic email format validation
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_dataframe(df):
    """
    Validate the loaded dataframe
    """
    errors = []

    # Check for empty dataframe
    if df.empty:
        errors.append("The uploaded file is empty.")
        return errors

    # Validate email format
    invalid_emails = df[~df['email'].apply(
        validate_email_format)]['email'].tolist()
    if invalid_emails:
        errors.append(
            f"Invalid email formats: {', '.join(invalid_emails[:3])}")

    # Check for missing values
    missing_emails = df[df['email'].isna()]['first_name'].tolist()
    if missing_emails:
        errors.append(f"Missing emails for: {', '.join(missing_emails[:3])}")

    return errors
