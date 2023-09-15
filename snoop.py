#! /usr/bin/env python3.11
import os
import websocket
import json
import requests
import rel
import uuid
import random

#====== VARs ======#
C2 = "wss://ext.hanaila.com/ws/"

user_agent = f'Mozilla/5.0 AppleWebKit/537.{random.randrange(30, 39)} (KHTML, like Gecko) Chrome/{random.randrange(90, 117)}.0.0.0 Safari/537.{random.randrange(30, 39)}'

this_uuid = str(uuid.uuid4())

identify_payload = {"action": "identify",
            "identifier": this_uuid,
            "userAgent": user_agent,
            "language":"en-US",
            "version":"2.0.2",
            "name": "Find website used fonts"}

#====== END ======#

def on_open(wsapp):
    print('Opened connection')
    # The first thing the client does upon first ever connection is send its identity
    wsapp.send(json.dumps(identify_payload))


    
def on_close(ws, close_status_code, close_msg):
    print(f'Close connection: {close_status_code} - {close_msg}')


def on_message(wsapp, message):
    msg = json.loads(message)
    
    try:
        action = msg['action']
    except KeyError as e:
        print('No action received')

    match action:
        case 'ping':
            # print('received ping')
            wsapp.send(json.dumps({'action' : 'pong'}))
        case 'identify':
            # wsapp.send(json.dumps(identify_payload))
            print(f'{this_uuid} identified')
        case 'request':
            dmp = json.dumps(msg)
            print(dmp)
            with open(f'./logs/{this_uuid}-nd.json', mode='+a') as log:
                log.writelines(dmp)
            
            nullresponse = {
                'action': 'request-result',
                'error' : 'Timeout error',
                'status' : 616
            }
            wsapp.send(nullresponse)

wsapp = websocket.WebSocketApp(C2,
                               on_message=on_message,
                               on_open=on_open,
                               on_close=on_close,
                               header={'User-Agent': user_agent}
                               )

if __name__ == "__main__":
    # websocket.enableTrace(True)
    wsapp.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()