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

# Custom CSS for better styling
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
    .attachment-list {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #1f77b4;
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

        # Important notes in sidebar
        st.markdown("---")
        st.subheader("💡 Important Notes")
        st.markdown("""
        - **Gmail Users**: Use an [App Password](https://myaccount.google.com/apppasswords) if 2FA is enabled
        - **Daily Limits**: Gmail free tier: 500 emails/day
        - **Attachments**: Keep files under 25MB for best compatibility
        """)

    # Main content area with tabs
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

                # File attachment section
                st.subheader("📎 File Attachments")
                uploaded_files = st.file_uploader(
                    "Add attachments to your email",
                    type=['pdf', 'txt', 'doc', 'docx', 'xlsx',
                          'xls', 'csv', 'jpg', 'jpeg', 'png', 'zip'],
                    accept_multiple_files=True,
                    help="Select one or multiple files to attach to all emails",
                    key="attachment_uploader"
                )

                # Display selected attachments
                if uploaded_files:
                    st.markdown('<div class="attachment-list">',
                                unsafe_allow_html=True)
                    st.success(
                        f"📎 {len(uploaded_files)} file(s) selected for attachment")
                    total_size = sum(file.size for file in uploaded_files)
                    for file in uploaded_files:
                        st.write(f"• {file.name} ({file.size / 1024:.1f} KB)")
                    st.write(
                        f"**Total size:** {total_size / 1024 / 1024:.2f} MB")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Warning for large attachments
                    if total_size > 20 * 1024 * 1024:  # 20MB
                        st.warning(
                            "⚠️ Large attachments may cause delivery issues with some email providers.")

                # Markdown formatting helper
                with st.expander("📝 Markdown Formatting Guide", expanded=False):
                    st.markdown("""
                    **Simple formatting that works in your emails:**
                    
                    - **Bold text**: `**bold**` → **bold**
                    - *Italic text*: `*italic*` → *italic*
                    - Bullet lists: Use `-` or `*` for items
                    - Numbered lists: Use `1.`, `2.`, etc.
                    - [Links]: `[text](http://url.com)` → clickable link
                    - Line breaks: Just press Enter
                    - Paragraphs: Press Enter twice for space between paragraphs
                    
                    **Available variables:**
                    - `{first_name}` - Recipient's first name
                    - `{email}` - Recipient's email address
                    
                    **Pro Tip:** Use empty lines between paragraphs for better readability!
                    """)

                # Initialize session state for email body
                if 'email_body' not in st.session_state:
                    st.session_state.email_body = """Hello {first_name},

Thank you for your interest in our services! 

Here are your **important updates** for this week:

*   New feature releases
*   Upcoming webinars and events  
*   Special offers available

You can visit our [website](http://example.com) for more detailed information.

Please don't hesitate to reach out if you have any questions.

Best regards,

**The Team**"""

                email_template = st.text_area(
                    "Email Body Template",
                    height=500,
                    value=st.session_state.email_body,
                    help="Write your email using simple Markdown formatting for bold, italics, lists, and links.",
                    key="email_body_template"
                )

            with col2:
                st.subheader("Email Preview")
                preview_option = st.radio(
                    "Preview type:", ["Formatted", "Raw Markdown"], key="preview_type")

                if st.button("Generate Preview", key="generate_preview"):
                    if 'df' in st.session_state and not st.session_state.df.empty:
                        sample_contact = st.session_state.df.iloc[0]
                        preview_body = email_template.format(
                            first_name=sample_contact['first_name'],
                            email=sample_contact['email']
                        )

                        if preview_option == "Formatted":
                            st.markdown("**Formatted Preview:**")
                            # This will render the Markdown
                            st.markdown(preview_body)
                        else:
                            st.markdown("**Raw Markdown:**")
                            st.text(preview_body)
                    else:
                        st.warning("No contact data available for preview.")

                # Quick formatting buttons
                st.subheader("Quick Formatting")
                format_col1, format_col2 = st.columns(2)

                with format_col1:
                    if st.button("Bold", key="bold_btn"):
                        st.session_state.email_body += " **bold text** "
                    if st.button("Italic", key="italic_btn"):
                        st.session_state.email_body += " *italic text* "
                    if st.button("Bullet List", key="bullet_btn"):
                        st.session_state.email_body += "\n- List item 1\n- List item 2\n- List item 3"

                with format_col2:
                    if st.button("Numbered List", key="numbered_btn"):
                        st.session_state.email_body += "\n1. First item\n2. Second item\n3. Third item"
                    if st.button("Link", key="link_btn"):
                        st.session_state.email_body += " [link text](http://example.com)"
                    if st.button("Reset Template", key="reset_btn"):
                        st.session_state.email_body = """Hello {first_name},

Thank you for your interest!

Best regards,
**The Team**"""

    with tab3:
        st.header("Send Emails")

        if 'df' not in st.session_state:
            st.warning("⚠️ Please load your contact data first.")
        elif not all(key in smtp_config for key in ['sender_email', 'password']):
            st.warning("⚠️ Please configure SMTP settings in the sidebar.")
        else:
            # Summary of sending operation
            st.info(
                f"📧 Ready to send emails to {len(st.session_state.df)} contacts")
            if uploaded_files:
                st.info(
                    f"📎 {len(uploaded_files)} file(s) will be attached to each email")

            # Send configuration
            st.subheader("Send Configuration")
            send_delay = st.slider(
                "Delay between emails (seconds)",
                min_value=0.0,
                max_value=5.0,
                value=0.5,
                help="Add delay to avoid being flagged as spam",
                key="send_delay"
            )

            # Send emails button
            if st.button("🚀 Send All Emails", type="primary", key="send_emails"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                results = []

                for i, (index, row) in enumerate(st.session_state.df.iterrows()):
                    status_text.text(
                        f"Sending email {i+1} of {len(st.session_state.df)} to {row['first_name']}...")

                    # Send email with attachments
                    success, message = send_single_email(
                        row['first_name'],
                        row['email'],
                        email_subject,
                        email_template,
                        smtp_config,
                        attachments=uploaded_files if uploaded_files else None,
                        format_type='markdown'
                    )

                    results.append({
                        'name': row['first_name'],
                        'email': row['email'],
                        'success': success,
                        'message': message
                    })

                    # Update progress
                    progress_bar.progress((i + 1) / len(st.session_state.df))

                    # Add delay between emails
                    if send_delay > 0:
                        time.sleep(send_delay)

                # Display results
                st.subheader("📊 Sending Results")
                success_count = sum(1 for r in results if r['success'])
                failure_count = len(results) - success_count

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Emails Sent Successfully",
                              f"{success_count}/{len(results)}")
                with col2:
                    st.metric("Failed Attempts", failure_count)

                # Detailed results
                with st.expander("View Detailed Results"):
                    for result in results:
                        if result['success']:
                            st.success(result['message'])
                        else:
                            st.error(result['message'])

                # Summary
                if failure_count == 0:
                    st.balloons()
                    st.success(
                        f"🎉 All {success_count} emails sent successfully!")
                else:
                    st.warning(
                        f"✅ {success_count} emails sent, ❌ {failure_count} failed")


if __name__ == "__main__":
    main()
