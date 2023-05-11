import os
import requests
from dotenv import load_dotenv
import jinja2

load_dotenv()
template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)


def render_template(template_filename, **context):
    """function that render the template html"""
    return template_env.get_template(template_filename).render(**context)


def send_simple_message(to, subject, body, html):
    """Mailgun code to send mail"""
    domain = os.getenv("MAILGUN_DOMAIN")
    api_key = os.getenv("MAILGUN_API_KEY")
    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={
            "from": f"store admin user <mailgun@{domain}>",
            "to": [to],
            "subject": subject,
            "text": body,
            "html": html,
        },
    )


def send_user_registration_email(email, username):
    """function that call send_simple_message"""
    return send_simple_message(
        email,
        "successfully signed up to store flask",
        f"Hi {username}! You have successfully signed up to the stores REST API",
        render_template("email/action.html", username=username),
    )
