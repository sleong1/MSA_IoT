# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time
import threading

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

class IntruderDetector(object):
    def __init__(self):
        # The device connection string to authenticate the device with your IoT hub.
        # Using the Azure CLI:
        # az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
        self.CONNECTION_STRING = "HostName=su-MSA.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=ZqigHWDCQ696rya1jI24fA9X3/RAtgbIqkN6WEo0ROc="

        # Define the JSON message to send to IoT Hub.
        self.DISTANCE = 250.0
        self.INTENSITY = 255
        MSG_TXT = '{{"Distance": {distance}, "intensity": {intensity}}}'

        INTERVAL = 1

        # Create an IoT Hub client
        self.client = IoTHubDeviceClient.create_from_connection_string(self.CONNECTION_STRING)


    # Listener currently not neccessary for current code
    # def device_method_listener(self, device_client):
    #     while True:
    #         method_request = device_client.receive_method_request()
    #         print (
    #             "\nMethod callback called with:\nmethodName = {method_name}\npayload = {payload}".format(
    #                 method_name=method_request.name,
    #                 payload=method_request.payload
    #             )
    #         )
    #         if method_request.name == "SetTelemetryInterval":
    #             try:
    #                 INTERVAL = int(method_request.payload)
    #             except ValueError:
    #                 response_payload = {"Response": "Invalid parameter"}
    #                 response_status = 400
    #             else:
    #                 response_payload = {"Response": "Executed direct method {}".format(method_request.name)}
    #                 response_status = 200
    #         else:
    #             response_payload = {"Response": "Direct method {} not defined".format(method_request.name)}
    #             response_status = 404

    #         method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
    #         device_client.send_method_response(method_response)



    def run(self):
        print ( "IoT Hub devices sending periodic messages, press Ctrl-C to exit" )
        try:
            # # Start a thread to listen 
            # device_method_thread = threading.Thread(target=device_method_listener, args=(self.client,))
            # device_method_thread.daemon = True
            # device_method_thread.start()

            while True:
                # Build the message with simulated telemetry values.
                distance = self.DISTANCE - (random.random() * 150)
                intensity = self.INTENSITY - (random.random() * 100)
                msg_txt_formatted = MSG_TXT.format(distance=distance, intensity=intensity)
                message = Message(msg_txt_formatted)

                # Add a custom application property to the message.
                # An IoT hub can filter on these properties without access to the message body.
                if self.DISTANCE < 100. && self.INTENSITY < 200:
                  message.custom_properties["intruderAlert"] = "true"
                else:
                  message.custom_properties["intruderAlert"] = "false"

                # Send the message.
                print( "Sending message: {}".format(message) )
                self.client.send_message(message)
                print( "Message sent" )
                time.sleep(INTERVAL)

        except KeyboardInterrupt:
            print ( "intruderAlert stopped" )

if __name__ == '__main__':
    print ( "Simulated Intruder Detector" )
    print ( "Press Ctrl-C to exit" )
    iotid = IntruderDetector()
    iotid.run()