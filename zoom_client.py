#!/usr/bin/python3

import socket
import json
from zoomus import ZoomClient

zoom_client = ZoomClient(
    'znkEibraRYSrLAUk2EuCog',
    'APISECRET'
)

#response = zoom_client.meeting.create(user_id='Qz4rYHpCT0--uPBuqNxPAA')
#json_response = json.loads(response.content.decode("utf-8"))
#print(json_response)

#user_list = json.loads(user_list_response.content)
exit()

# Placeholder netcode
HOST = '127.0.0.1'
PORT = 1337
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
msg = client_socket.recv(1024)
client_socket.close()
print(msg.decode('ascii'))
