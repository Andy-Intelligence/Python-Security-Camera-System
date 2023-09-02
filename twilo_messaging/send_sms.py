import os
from twilio.rest import Client
from dotenv import load_dotenv
import datetime

load_dotenv()
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)




def send_notification(url):
    current_time = datetime.datetime.now()
    formattted_current_time = current_time.strftime("%d-%m-%y-%H-%M-%S")

    message = client.messages.create(
                        body=f"Detected motion at {formattted_current_time}, URL to Watch:{url}",
                        from_=os.getenv("TWILIO_SEND_NUMBER"),
                        to=os.getenv("TWILIO_RECEIVE_NUMBER")
                    )

    print(message.sid)




#this is what the response looks like after message has been sent

# {
#   "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#   "api_version": "2010-04-01",
#   "body": "Join Earth's mightiest heroes. Like Kevin Bacon.",
#   "date_created": "Thu, 30 Jul 2015 20:12:31 +0000",
#   "date_sent": "Thu, 30 Jul 2015 20:12:33 +0000",
#   "date_updated": "Thu, 30 Jul 2015 20:12:33 +0000",
#   "direction": "outbound-api",
#   "error_code": null,
#   "error_message": null,
#   "from": "+15017122661",
#   "messaging_service_sid": "MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#   "num_media": "0",
#   "num_segments": "1",
#   "price": null,
#   "price_unit": null,
#   "sid": "SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#   "status": "sent",
#   "subresource_uris": {
#     "media": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Media.json"
#   },
#   "to": "+15558675310",
#   "uri": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.json"
# }