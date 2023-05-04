# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = "ACcfcc6645d9cb4d0fce93402ee7a2eade"
auth_token = "e29cc14f8dd2d4e24af341a83e01a6d2"
verify_sid = "VA155f27d48b712ac5f9ca2c5ca67a4caa"
verified_number = "+918137974704"




class MessaHandler:
    
    phone_number=None
    otp= None

    def __init__(self,phone_number,otp) -> None:
        self.phone_number=phone_number
        self.otp=otp

    
    def send_otp_on_phone(self):
        client = Client(account_sid, auth_token)

        message=client.messages.create(
            body=f"your otp is {self.otp}",
            from_='+16203838737',
            to=self.phone_number,

        )