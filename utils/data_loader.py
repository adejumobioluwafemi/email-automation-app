import pandas as pd
import streamlit as st
from io import BytesIO


def load_data_from_file1(uploaded_file):
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


def validate_dataframe_with_mapping(df, mapping):
    """
    Validate the dataframe using user-provided column mapping
    """
    errors = []

    if df.empty:
        errors.append("The uploaded file is empty.")
        return errors

    # Check if mapped email column exists and has valid data
    if mapping['email'] not in df.columns:
        errors.append(
            f"Selected email column '{mapping['email']}' not found in data.")
    else:
        # Check for invalid emails in the mapped column
        invalid_emails = df[~df[mapping['email']].apply(
            validate_email_format)][mapping['email']].tolist()
        if invalid_emails:
            errors.append(
                f"Invalid email formats found: {', '.join(map(str, invalid_emails[:3]))}")

    # Check if mapped first_name column exists
    if mapping['first_name'] not in df.columns:
        errors.append(
            f"Selected first name column '{mapping['first_name']}' not found in data.")

    return errors


def extract_first_name1(full_name):
    """
    Extract first name from a full name string.
    Handles cases like "John Doe", "John", "John M. Doe", etc.
    Returns the original string if no space is found.
    """
    if pd.isna(full_name):
        return ""

    # Convert to string and strip whitespace
    name_str = str(full_name).strip()

    # Split on spaces and return first part
    parts = name_str.split()
    return parts[0] if parts else name_str


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

        return df, "Data loaded successfully! Please map your columns below."

    except Exception as e:
        return None, f"Error loading file: {str(e)}"


def validate_dataframe_columns(df, required_columns):
    """
    Check if dataframe has the required columns
    Returns list of missing columns
    """
    missing_columns = [
        col for col in required_columns if col not in df.columns]
    return missing_columns


def extract_first_name(full_name):
    """
    Extract first name from a full name string
    """
    if pd.isna(full_name):
        return ""
    name_str = str(full_name).strip()
    parts = name_str.split()
    return parts[0] if parts else name_str


def apply_column_mapping(df, mapping):
    """
    Apply column mapping to create standardized dataframe
    """
    mapped_df = pd.DataFrame()

    # Map email column
    if 'email' in mapping and mapping['email']:
        mapped_df['email'] = df[mapping['email']]

    # Map first_name column with extraction if needed
    if 'first_name' in mapping and mapping['first_name']:
        source_column = mapping['first_name']

        # Check if this might be a full name column
        column_name_lower = source_column.lower()
        needs_extraction = any(term in column_name_lower for term in [
                               'name', 'full', 'complete'])

        if needs_extraction:
            mapped_df['first_name'] = df[source_column].apply(
                extract_first_name)
        else:
            mapped_df['first_name'] = df[source_column]

    return mapped_df
