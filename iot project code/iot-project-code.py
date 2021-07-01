from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from playsound import playsound
import wiotp.sdk.device
import time
import random
import os
myConfig = { 
    "identity": {
        "orgId": "aeqag9",
        "typeId": "iotdevice",
        "deviceId":"1234"
    },
    "auth": {
        "token": "1234567890"
    }
}
authenticator = IAMAuthenticator('8oF1v86EliXvM143bGIGFHjzzWOxvlhjdb15k_FAP3LA')
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)

text_to_speech.set_service_url('https://api.us-south.text-to-speech.watson.cloud.ibm.com/instances/8f6159d7-7bc0-4e7b-89ef-2eadd048b9bd')

def myCommandCallback(cmd):
    print("Message received from IBM IoT Platform: %s" % cmd.data['command'])
    m=cmd.data['command']
def phvalue():
    with open('new.mp3', 'wb') as audio_file:
        audio_file.write(
                text_to_speech.synthesize(
                    'ph value of water is exceeded ,dont drink river water',
                    voice='en-US_AllisonV3Voice',
                    accept='audio/mp3'        
                ).get_result().content)
    playsound('new.mp3')
    time.sleep(1)
    os.remove('new.mp3')
    return
def waterquality():
    with open('new1.mp3', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                'water quality is not good ,dont drink river water',
                voice='en-US_AllisonV3Voice',
                accept='audio/mp3'        
            ).get_result().content)
    playsound('new1.mp3')
    time.sleep(1)
    os.remove('new1.mp3')
    return
def both():
    with open('new2.mp3', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                'water is not suitable for drinking',
                voice='en-US_AllisonV3Voice',
                accept='audio/mp3'        
            ).get_result().content)
    playsound('new2.mp3')
    time.sleep(1)
    os.remove('new2.mp3')
    return
client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()

while True:
    
    wq=random.randint(0,100)
    ph=float("{:.1f}".format(random.uniform(1,14)))
    myData={'waterquality':wq, 'phvalue':ph}
    if ph>=8.5 and wq<=70:
        both()
    elif wq<=70:
        waterquality()
    elif ph>=8.5:
        phvalue()
    time.sleep(2)
    client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
    print("Published data Successfully: %s", myData)
    client.commandCallback = myCommandCallback
    
client.disconnect()
