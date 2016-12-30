# -*- coding: utf-8 -*-

from socket import *
import json

import zhihuScrapy
import dataSaver

serverHost = 'localHost'
serverPort = 50007
address = (serverHost, serverPort)
dbConnection = dataSaver.connect()

connectionJson = {'type': 'connection', 'status': '0'}
taskStatusJson = {'type': 'task', 'status': '0', 'urlToken': '', 'followingList': []}

connectionMessage = json.dumps(connectionJson).encode('utf-8')

socketObj = socket(AF_INET, SOCK_STREAM)
socketObj.connect(address)
socketObj.send(connectionMessage)

print('< Client Start.>')

while True:
    responseUTF8 = socketObj.recv(1024)

    if responseUTF8:
        print(responseUTF8.decode())
        response = json.loads(responseUTF8.decode())

        if response['type'] == 'urlToken':
            urlToken = response['urlToken']
            taskStatusJson['urlToken'] = urlToken
            userData = zhihuScrapy.UserData(urlToken=urlToken, DBConnection=dbConnection)

            userData.getUserInfo()
            userData.saveUserInfo()
            userFollowingList = userData.getUserFollowingList()

            if userFollowingList:
                userData.saveUserRelation()

                for userFollowing in userFollowingList:
                    taskStatusJson['followingList'].append(userFollowing)

                message = json.dumps(taskStatusJson).encode('utf-8')
                socketObj.send(message)

            else:
                message = json.dumps(taskStatusJson).encode('utf-8')
                socketObj.send(message)

socketObj.close()
