# -*- coding: utf-8 -*-

from socket import *
import dataSaver
import json

myHost = ''
myPort = 50007
address = (myHost, myPort)
dbConnection = dataSaver.connect()

taskQueue = set()
taskQueue.add('miao-miao-miao-38-64')

taskJson = {'type': 'urlToken', 'urlToken': ''}

sockObj = socket(AF_INET, SOCK_STREAM)
sockObj.bind(address)
sockObj.listen(5)

print('< Server Start.>')
print('< StartQueue: %s >' % taskQueue)

while True:
    connection, address = sockObj.accept()

    print('< Server connected by ', address, ' >')

    while True:
        response = connection.recv(10240)

        print('< Response: %s >' % response)
        if not response:
            break
        else:
            response = response.decode()
            responseDict = json.loads(response)

            if responseDict['type'] == 'connection':
                taskJson['urlToken'] = taskQueue.pop()
                message = json.dumps(taskJson).encode('utf-8')
                connection.send(message)

            elif responseDict['type'] == 'task':
                if responseDict['followingList']:
                    for urlToken in responseDict['followingList']:
                        taskQueue.add(urlToken)

                taskJson['urlToken'] = taskQueue.pop()
                message = json.dumps(taskJson).encode('utf-8')
                connection.send(message)

        response = ''
        urlToken = ''

    print('< taskQueue: %s >' % taskQueue)
