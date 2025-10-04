# 📧 Bulk Email Automation App

A powerful, user-friendly Streamlit application for sending personalized bulk emails with support for attachments, Markdown formatting, and flexible data source integration.

## 🚀 Live Demo

**The app is deployed and available at:**  
👉 **[https://bulkmailing.streamlit.app/](https://bulkmailing.streamlit.app/)**

## ✨ Features

### 📊 Flexible Data Integration
- **Multiple File Formats**: Upload CSV, Excel (.xlsx, .xls) files
- **Smart Column Mapping**: Automatically detect and map columns like `name`, `firstname`, `emails` to required `first_name` and `email` fields
- **First Name Extraction**: Automatically extracts first names from full name columns (e.g., "John Doe" → "John")
- **Data Validation**: Real-time validation of email formats and required fields

### ✍️ Rich Email Composition
- **Markdown Support**: Write emails using simple Markdown syntax (`**bold**`, `*italic*`, `[links]()`, lists)
- **Live Preview**: See exactly how your email will look before sending
- **Template Variables**: Personalize with `{first_name}` and `{email}` placeholders
- **Quick Formatting Buttons**: One-click formatting for common elements

### 📎 Advanced Attachment Handling
- **Multiple Files**: Attach multiple files to all emails
- **Various Formats**: Support for PDF, images, documents, spreadsheets, and more
- **Size Monitoring**: Real-time file size tracking with warnings for large attachments

### 🔧 SMTP Configuration
- **Multiple Providers**: Pre-configured for Gmail, Office 365, Yahoo, SendGrid, Mailgun
- **Connection Testing**: Test SMTP settings before sending
- **Secure Authentication**: Support for App Passwords and OAuth-ready structure

### 📈 Sending Management
- **Controlled Sending**: Configurable delays between emails to avoid spam filters
- **Progress Tracking**: Real-time progress bars and status updates
- **Detailed Reporting**: Success/failure tracking with comprehensive results

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### 1. Clone and Setup Environment
```bash
# Create and activate conda environment
conda env create -f environment.yml
conda activate email-automation-app

# Or create manually
conda create -n email-automation-app python=3.9
conda activate email-automation-app
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
email-automation-app/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── environment.yml       # Conda environment configuration
├── .streamlit/
│   └── config.toml      # Streamlit configuration
├── utils/
│   ├── __init__.py
│   ├── email_sender.py  # SMTP email handling functions
│   └── data_loader.py   # Data processing and validation
├── data/
│   └── sample_contacts.csv  # Example contact data
└── staticfiles/
    └── dftlabs_logo.png    # Company branding
```

## 🔐 SMTP Configuration Guide

### Gmail Setup
1. Enable 2-Factor Authentication in your Google Account
2. Generate an App Password (https://myaccount.google.com/apppasswords):
   - Go to Google Account → Security → App passwords
   - Generate password for "Mail"
   - Use this 16-character password in the app - Copy the generated 16-character password

### Other Providers
- **Office 365**: Use your email and password
- **SendGrid**: Use API key as password with `smtp.sendgrid.net`
- **Custom SMTP**: Configure host, port, and credentials

## 📋 Usage Guide

### Step 1: Upload Contact Data
1. Choose between uploading your file or using sample data
2. If your columns don't match exactly, use the column mapping feature
3. Preview and validate your data before proceeding

### Step 2: Compose Email
1. Write your email subject
2. Compose the body using Markdown formatting
3. Use `{first_name}` for personalization
4. Add attachments if needed
5. Preview how the email will look

### Step 3: Send Emails
1. Configure sending delay (recommended: 0.5-1 second)
2. Test SMTP connection if needed
3. Click "Send All Emails" and monitor progress
4. Review sending results and any failures

## 🚀 Deployment

This app is deployed using **Streamlit Community Cloud**:

1. Push code to GitHub repository
2. Connect repository to Streamlit Community Cloud
3. Configure secrets for SMTP credentials
4. Deploy automatically on git push

**Live URL**: [https://bulkmailing.streamlit.app/](https://bulkmailing.streamlit.app/)

## ⚙️ Configuration Files

### environment.yml
```yaml
name: email-automation-app
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - pip
  - pandas
  - openpyxl
  - pip:
    - streamlit>=1.50.0
    - plotly
    - python-dotenv
    - markdown
```

### requirements.txt
```txt
streamlit>=1.50.0
pandas>=1.5.0
openpyxl>=3.0.0
markdown>=3.0
python-dotenv>=1.0.0
```

## 🔒 Security Features

- Secure credential management
- SMTP connection encryption (TLS/SSL)
- Input validation and sanitization
- Rate limiting to prevent spam detection
- No hardcoded credentials in source code

## 📊 Performance Notes

- **Gmail Limits**: 500 emails per day (free accounts)
- **Attachment Size**: Keep under 25MB for best deliverability
- **Sending Speed**: 0.5-1 second delays recommended
- **Memory Usage**: Optimized for large contact lists

## 🐛 Troubleshooting

### Common Issues
- **SMTP Connection Failed**: Check credentials and App Passwords for Gmail
- **Column Mapping Not Working**: Ensure your file has header rows
- **Emails Going to Spam**: Reduce sending speed, improve email content
- **Attachment Too Large**: Compress files or use cloud links

### Getting Help
1. Check the app's validation messages
2. Test SMTP connection separately
3. Verify file formats and encoding
4. Check email provider sending limits

## 🤝 Contributing

We welcome contributions! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is proprietary software developed by DeepFly Tech Labs.

## 👥 Developed By

**DeepFly Tech Labs**  


---
