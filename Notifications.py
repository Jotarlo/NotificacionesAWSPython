from flask import Flask, request
import os
import boto3

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Hola, soy Flask"


@app.route("/sms", methods=['POST'])
def sms():
    destination = request.form['destination']
    message = request.form['message']
    print(destination)
    print(message)
    # Create an SNS client
    client = boto3.client(
        "sns",
        aws_access_key_id="IAM_ACCESS_KEY",
        aws_secret_access_key="IAM_SECRET_ACCESS_KEY",
        region_name="us-east-1"
    )

    # Send your sms message.
    client.publish(
        PhoneNumber=destination,
        Message=message
    )
    return "OK"

# based on the code above, build the email api method using AWS SES
@app.route("/email", methods=['POST'])
def email():
    destination = request.form['destination']
    message = request.form['message']
    subject = request.form['subject']
    # Create an SES client
    client = boto3.client(
        "ses",
        aws_access_key_id="IAM_ACCESS_KEY",
        aws_secret_access_key="IAM_SECRET_ACCESS_KEY",
        region_name="us-east-1"
    )
    # send the email message using the client
    response = client.send_email(
        Destination={
            'ToAddresses': [
                destination,
            ],
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': "UTF-8",
                    'Data': message,
                },
            },
            'Subject': {
                'Charset': "UTF-8",
                'Data': subject,
            },
        },
        Source="jeferson.arango@ucaldas.edu.co"
    )
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)

