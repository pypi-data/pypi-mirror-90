import paho.mqtt.client as mqtt
import ssl
import time
import signal
import json
import sys
import uuid
import hashlib

class Client(object):

    def __init__(self, API_KEY=None, USER_ID=None, CALLBACK=None, SALT="x9nFgM1ioxAOPmT3Fdyeh483lerc1J7k"):    
        ctx = ssl.create_default_context()
        ctx.set_alpn_protocols(["mqtt"])
        client_id , username, password = self.gen_user_client_pass(API_KEY, SALT)

        self.callback_function = CALLBACK

        self.client = mqtt.Client(client_id=client_id,protocol=mqtt.MQTTv311)
        self.channel_name = "locations/+/+/+"
        self.account_id = None
        self.project_id = None
        self.user_id = None
        self.is_user_received = False
        self.channel_name_checker = False
        
        self.client.on_message = self.on_message
        if USER_ID is None:
            self.client.on_connect = self.on_connect
        else:
            self.is_user_received = True
            self.user_id = USER_ID
            self.client.on_connect = self.on_connect_user_id
        self.client.tls_set_context(context=ctx)
        self.client.username_pw_set(username+"?x-amz-customauthorizer-name=iot-authorizer" , password)
        self.client.connect("az91jf6dri5ey-ats.iot.eu-central-1.amazonaws.com" , port=443)
        
        print("Successfully Initialised")

    def gen_user_client_pass(self, API_KEY, SALT):
        timestamp = str(time.time())
        client_id = API_KEY + "_" + str(uuid.uuid4())
        username = "api_"+timestamp
        password = hashlib.sha512((API_KEY+timestamp+SALT).encode()).hexdigest()
        return client_id , username , password

    def on_message(self, client,userdata,msg):
        json_data = json.loads(msg.payload)
        if not self.callback_function:
            print("Location Data: ", json_data)
        else:
            print("Passing to callback function.")
            self.callback_function(json_data)
        if not self.channel_name_checker:
            self.client.unsubscribe(self.channel_name)
            temp_values = msg.topic.split("/")[1:]
            self.account_id = temp_values[0]
            self.project_id = temp_values[1]
            self.user_id = temp_values[2]
            if not self.is_user_received:
                self.channel_name = "locations/"+ self.account_id + "/" + self.project_id + "/+"
            else:
                self.channel_name = msg.topic
            self.client.subscribe(self.channel_name)
            self.channel_name_checker = True

    
    def on_connect(self, client,userdata,flags,rc):
        print("Connected successfully")
        client.subscribe(self.channel_name)
    
    def on_connect_user_id(self, client,userdata,flags,rc):
        print("Connected successfully")
        self.channel_name = self.channel_name[:-1] + self.user_id
        client.subscribe(self.channel_name)

    def disconnect(self):
        self.client.unsubscribe(self.channel_name)
        self.client.disconnect()
        print("Disconnected successfully.")
    
    def sub(self):
        try:
            self.client.loop_forever()
        except KeyboardInterrupt:
            self.disconnect()
