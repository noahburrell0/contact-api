"""
Required Environment Variables:

SUBJECT_PREAMBLE (str)
FROM_ADDRESS (str)
TO_ADDRESS (str)
SMTP_SERVER (str)
"""

from flask import Flask, request, escape
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
import os

app = Flask(__name__)

# Set rate limiting by IP address to 2 per hour
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["2 per hour"],
)

# Define email regex for address validation
emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Define the contact endpoint, only accept POST requests
@app.route("/contact", methods=['POST'])
def contact():

    # Get form data and sanatize
    replyTo = escape(request.form['reply_to'])
    body = escape(request.form['body'])
    subject = escape(request.form['subject'])
    name = escape(request.form['name'])

    # Validate email
    if not (re.fullmatch(emailRegex, replyTo)):
        return '', 401
    
    print(replyTo)
    print(body)

    # Prepare Email
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = os.getenv('SUBJECT_PREAMBLE')+' '+subject
    msg['Reply-To'] = replyTo
    msg['From'] = formataddr((name, os.getenv('FROM_ADDRESS')))
    msg['To'] = os.getenv('TO_ADDRESS')

    # Send Email
    s = smtplib.SMTP(os.getenv('SMTP_SERVER'), timeout=2)
    s.send_message(msg)
    s.quit()

    # If everything is successful, send a 201
    return '', 201

if __name__ == "__main__":
    app.run(host='0.0.0.0')