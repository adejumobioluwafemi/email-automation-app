import smtplib
import markdown
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from markdown.extensions import Extension


def markdown_to_html(markdown_text):
    """
    Convert Markdown text to HTML with basic styling
    """
    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_text, extensions=['extra'])

    # Add basic email styling
    styled_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            {html_content}
        </body>
    </html>
    """
    return styled_html


def send_single_email(recipient_name, recipient_email, subject, body, smtp_config, format_type='markdown'):
    """
    Send email with support for Markdown formatting
    """
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = formataddr(
            (smtp_config['sender_name'], smtp_config['sender_email']))
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Personalize the body
        personalized_body = body.replace('{first_name}', recipient_name)

        if format_type == 'markdown':
            # Convert Markdown to HTML
            html_content = markdown_to_html(personalized_body)
            # Also include plain text version
            # plain_text = personalized_body
        else:
            # Fallback to existing HTML processing
            html_content = format_email_body(personalized_body, 'html')
            # plain_text = format_email_body(personalized_body, 'plain')

        # Attach both HTML and plain text versions
        # msg.attach(MIMEText(plain_text, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))

        # Rest of your SMTP code remains the same...
        if smtp_config['port'] == 465:
            server = smtplib.SMTP_SSL(smtp_config['host'], smtp_config['port'])
        else:
            server = smtplib.SMTP(smtp_config['host'], smtp_config['port'])
            server.starttls()

        server.login(smtp_config['sender_email'], smtp_config['password'])
        server.send_message(msg)
        server.quit()

        return True, f"✅ Email sent to {recipient_name} ({recipient_email})"

    except Exception as e:
        return False, f"❌ Failed to send to {recipient_name}: {str(e)}"


def send_single_email1(recipient_name, recipient_email, subject, body, smtp_config):
    """
    Send a single personalized email using SMTP
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = formataddr(
            (smtp_config['sender_name'], smtp_config['sender_email']))
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Personalize the body and convert newlines to HTML breaks
        personalized_body = body.replace('{first_name}', recipient_name)
        html_body = personalized_body.replace('\n', '<br>')

        # Create proper HTML email
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                {html_body}
            </body>
        </html>
        """

        # Add both HTML and plain text versions
        msg.attach(MIMEText(html_content, 'html'))
        # msg.attach(MIMEText(personalized_body, 'plain'))

        # Connect to SMTP server and send
        if smtp_config['port'] == 465:
            # SSL connection
            server = smtplib.SMTP_SSL(smtp_config['host'], smtp_config['port'])
        else:
            # TLS connection
            server = smtplib.SMTP(smtp_config['host'], smtp_config['port'])
            server.starttls()

        server.login(smtp_config['sender_email'], smtp_config['password'])
        server.send_message(msg)
        server.quit()

        return True, f"✅ Email sent to {recipient_name} ({recipient_email})"

    except Exception as e:
        return False, f"❌ Failed to send to {recipient_name}: {str(e)}"


def send_single_email2(recipient_name, recipient_email, subject, body, smtp_config):
    """
    Send a single personalized email using SMTP
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = formataddr(
            (smtp_config['sender_name'], smtp_config['sender_email']))
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Personalize the body
        personalized_body = body.replace('{first_name}', recipient_name)

        # Add HTML or plain text body
        msg.attach(MIMEText(personalized_body, 'html'))

        # Connect to SMTP server and send
        if smtp_config['port'] == 465:
            # SSL connection
            server = smtplib.SMTP_SSL(smtp_config['host'], smtp_config['port'])
        else:
            # TLS connection
            server = smtplib.SMTP(smtp_config['host'], smtp_config['port'])
            server.starttls()

        server.login(smtp_config['sender_email'], smtp_config['password'])
        server.send_message(msg)
        server.quit()

        return True, f"✅ Email sent to {recipient_name} ({recipient_email})"

    except Exception as e:
        return False, f"❌ Failed to send to {recipient_name}: {str(e)}"


def format_email_body(body_text, format_type='html'):
    """
    Format email body text to preserve paragraph structure
    """
    if format_type == 'html':
        # Convert newlines to HTML line breaks
        formatted = body_text.replace('\n', '<br>')
    elif format_type == 'plain':
        # Ensure proper paragraph spacing for plain text
        formatted = body_text.replace('\n', '\n\n')
    else:
        formatted = body_text

    return formatted


def test_smtp_connection(smtp_config):
    """
    Test SMTP connection with provided credentials
    """
    try:
        if smtp_config['port'] == 465:
            server = smtplib.SMTP_SSL(smtp_config['host'], smtp_config['port'])
        else:
            server = smtplib.SMTP(smtp_config['host'], smtp_config['port'])
            server.starttls()

        server.login(smtp_config['sender_email'], smtp_config['password'])
        server.quit()
        return True, "✅ SMTP connection successful!"

    except Exception as e:
        return False, f"❌ SMTP connection failed: {str(e)}"
