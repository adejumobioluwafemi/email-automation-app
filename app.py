import streamlit as st
import pandas as pd
import time
from utils.data_loader import load_data_from_file, load_sample_data, validate_dataframe
from utils.email_sender import send_single_email, test_smtp_connection, markdown_to_html

# Page configuration
st.set_page_config(
    page_title="Email Automation App",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-message {
        padding: 10px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
    }
    .error-message {
        padding: 10px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)


def main():
    st.markdown('<h1 class="main-header">📧 Automated Email Sender</h1>',
                unsafe_allow_html=True)

    # Sidebar for SMTP configuration
    with st.sidebar:
        st.header("🔧 SMTP Configuration")

        smtp_config = {}
        smtp_config['sender_name'] = st.text_input(
            "Sender Name", "Your Company", key="sender_name")
        smtp_config['sender_email'] = st.text_input(
            "Sender Email", "your.email@gmail.com", key="sender_email")
        smtp_config['password'] = st.text_input(
            "SMTP Password", type="password", key="smtp_password")
        smtp_config['host'] = st.selectbox("SMTP Host", [
            "smtp.gmail.com",
            "smtp.office365.com",
            "smtp.mail.yahoo.com",
            "smtp.sendgrid.net",
            "smtp.mailgun.org"
        ], key="smtp_host")
        smtp_config['port'] = st.selectbox(
            "SMTP Port", [587, 465, 2525], key="smtp_port")

        if st.button("Test SMTP Connection", key="test_connection"):
            success, message = test_smtp_connection(smtp_config)
            if success:
                st.success(message)
            else:
                st.error(message)

    # Main content area
    tab1, tab2, tab3 = st.tabs(
        ["📁 Upload Data", "✍️ Compose Email", "🚀 Send Emails"])

    with tab1:
        st.header("Upload Your Contact Data")

        col1, col2 = st.columns(2)

        with col1:
            upload_option = st.radio(
                "Choose data source:",
                ["Upload CSV/Excel", "Use Sample Data"],
                key="upload_option"
            )

            if upload_option == "Upload CSV/Excel":
                uploaded_file = st.file_uploader(
                    "Choose a file",
                    type=['csv', 'xlsx', 'xls'],
                    help="File should contain 'first_name' and 'email' columns",
                    key="file_uploader"
                )

                if uploaded_file:
                    df, message = load_data_from_file(uploaded_file)
                    if df is not None:
                        st.success(message)
                        st.session_state.df = df
                    else:
                        st.error(message)
            else:
                if st.button("Load Sample Data", key="load_sample"):
                    df = load_sample_data()
                    st.session_state.df = df
                    st.success("Sample data loaded successfully!")

        with col2:
            if 'df' in st.session_state:
                st.subheader("Data Preview")
                st.dataframe(st.session_state.df, use_container_width=True)

                st.subheader("Data Validation")
                errors = validate_dataframe(st.session_state.df)
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    st.success("✅ Data validation passed!")

                st.info(f"📊 Total contacts: {len(st.session_state.df)}")

    with tab2:
        st.header("Compose Your Email")

        if 'df' not in st.session_state:
            st.warning(
                "⚠️ Please load your contact data first in the 'Upload Data' tab.")
        else:
            col1, col2 = st.columns([2, 1])

            with col1:
                email_subject = st.text_input(
                    "Email Subject", "Important Update from Our Team", key="email_subject")

                # Markdown formatting helper
                with st.expander("📝 Formatting Help (Markdown Supported)"):
                    st.markdown("""
                    **Simple Formatting Examples:**
                    - **Bold**: `**text**` → **text**
                    - *Italic*: `*text*` → *text*
                    - Lists: Use `-` or `1.` for bullet points
                    - Line breaks: Just press Enter twice for paragraphs
                    - [Links]: `[text](http://url.com)` → clickable link
                    
                    **Pro Tip:** Use empty lines between paragraphs for better spacing!
                    """)

                # Initialize session state for email body
                if 'email_body' not in st.session_state:
                    st.session_state.email_body = """Hello {first_name},

Thank you for your interest in our services. 

Here are your **important updates**:

- *Item 1*: Description with **bold** and *italic* text
- *Item 2*: Another important point
- *Item 3*: Final reminder

Visit our [website](http://example.com) for more information.

Best regards,
**The Team**"""

                email_template = st.text_area(
                    "Email Body Template",
                    height=300,
                    value=st.session_state.email_body,
                    help="Use Markdown formatting: **bold**, *italic*, [links](http://example.com), lists with - or 1.",
                    key="email_template"
                )

            with col2:
                st.subheader("Email Preview")
                if st.button("Generate Preview", key="generate_preview"):
                    sample_contact = st.session_state.df.iloc[0]
                    preview_body = email_template.format(
                        first_name=sample_contact['first_name'],
                        email=sample_contact['email']
                    )

                    # Show HTML preview
                    html_preview = markdown_to_html(preview_body)
                    st.markdown("**HTML Preview:**")
                    st.markdown(html_preview, unsafe_allow_html=True)

                    # Show raw Markdown
                    with st.expander("View Raw Markdown"):
                        st.text(preview_body)

    with tab3:
        st.header("Send Emails")

        if 'df' not in st.session_state:
            st.warning("⚠️ Please load your contact data first.")
        elif not all(key in smtp_config for key in ['sender_email', 'password']):
            st.warning("⚠️ Please configure SMTP settings in the sidebar.")
        else:
            st.info(
                f"📧 Ready to send emails to {len(st.session_state.df)} contacts")

            if st.button("🚀 Send All Emails", type="primary", key="send_emails"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                results = []

                for i, (index, row) in enumerate(st.session_state.df.iterrows()):
                    status_text.text(
                        f"Sending email {i+1} of {len(st.session_state.df)} to {row['first_name']}...")

                    success, message = send_single_email(
                        row['first_name'],
                        row['email'],
                        email_subject,
                        email_template,
                        smtp_config,
                        format_type='markdown'
                    )

                    results.append({
                        'name': row['first_name'],
                        'email': row['email'],
                        'success': success,
                        'message': message
                    })

                    progress_bar.progress((i + 1) / len(st.session_state.df))
                    time.sleep(0.1)  # Small delay to avoid rate limiting

                # Display results
                st.subheader("Sending Results")
                success_count = sum(1 for r in results if r['success'])

                st.metric("Emails Sent Successfully",
                          f"{success_count}/{len(results)}")

                for result in results:
                    if result['success']:
                        st.success(result['message'])
                    else:
                        st.error(result['message'])


if __name__ == "__main__":
    main()
