#  QuickStart Guide

pip install Geospark-python-sdk

# To import package

from roam import Client

# To get locations for all users at project level
client = Client(API_KEY=<API-KEY>)

# To get locations for all users at user level
client = Client(API_KEY=<API-KEY>, USER_ID=<USER-ID>)

# To start listening to locations
client.sub()

# To stop listening to locations
client.disconnect()

By default the SDK prints out the locations. If the locations are required to any other output, then
please use a callback function. 

# Define callback function and pass in client initialization

def custom_callback_function(payload):
    # print(payload)
    # save_to_file(payload)
    # log(payload)

client = Client(API_KEY=<API-KEY>, CALLBACK=<custom_callback_function>)
