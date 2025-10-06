import os
import requests
import json

def send_email(to_email, subject, text_content, html_content=None):
    auth_token = os.environ.get('REPL_IDENTITY')
    if auth_token:
        auth_token = f"repl {auth_token}"
    else:
        auth_token = os.environ.get('WEB_REPL_RENEWAL')
        if auth_token:
            auth_token = f"depl {auth_token}"
    
    if not auth_token:
        print("Warning: No authentication token found for email sending")
        return None
    
    payload = {
        "to": to_email,
        "subject": subject,
        "text": text_content
    }
    
    if html_content:
        payload["html"] = html_content
    
    try:
        response = requests.post(
            "https://connectors.replit.com/api/v2/mailer/send",
            headers={
                "Content-Type": "application/json",
                "X_REPLIT_TOKEN": auth_token
            },
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Email sending failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return None
