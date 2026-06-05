# from multiprocessing.dummy.connection import Client


# class NotificationManager:
#     #This class is responsible for sending notifications with the deal flight details.


#     def send_sms(self, message):
#         client = Client(
#             "YOUR_TWILIO_SID",
#             "YOUR_AUTH_TOKEN"
#         )

#         client.messages.create(
#             body=message,
#             from_="YOUR_TWILIO_NUMBER",
#             to="YOUR_PHONE_NUMBER"
#         )