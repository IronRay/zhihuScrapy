# -*- coding: utf-8 -*-

import pymysql
import getpass
import json


def connect():

    host = input('Host:')
    user = input('User:')
    password = getpass.getpass('Password:')
    db = input('DB:')

    connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 db=db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    host = ''
    user = ''
    password = ''
    db = ''

    return connection


def insertUserInfo(connection, userInfo):
    locations = json.dumps(userInfo['locations'], ensure_ascii=False)
    educations = json.dumps(userInfo['educations'], ensure_ascii=False)
    employments = json.dumps(userInfo['employments'], ensure_ascii=False)

    with connection.cursor() as cursor:
        sql = 'INSERT INTO `USER_INFO_TEST_6` (`userType`, `urlToken`, `name`, `gender`, `avatarUrl`,`locations`, `educations`, `employments`,  `business`, `questionCount`, `answerCount`, `articlesCount`, `logsCount`, `favoriteCount`, `participatedLiveCount`, `hostedLiveCount`, `followingCount`, `followingQuestionCount`, `followingTopicCount`, `followingFavlistsCount`, `followingColumnsCount`, `followerCount`, `markedAnswersCount`, `voteupCount`, `favoritedCount`, `thankedCount`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        valueTuple = (userInfo['userType'], userInfo['urlToken'], userInfo['name'],
                      userInfo['gender'], userInfo['avatarUrl'], locations, educations, employments, userInfo['business'], userInfo['questionCount'],
                      userInfo['answerCount'], userInfo['articlesCount'], userInfo['logsCount'],
                      userInfo['favoriteCount'], userInfo['participatedLiveCount'], userInfo['hostedLiveCount'],
                      userInfo['followingCount'], userInfo['followingQuestionCount'], userInfo['followingTopicCount'],
                      userInfo['followingFavlistsCount'], userInfo['followingColumnsCount'], userInfo['followerCount'],
                      userInfo['markedAnswersCount'], userInfo['voteupCount'], userInfo['favoritedCount'],
                      userInfo['thankedCount'])

        cursor.execute(sql, valueTuple)

        # print('< Result: %s >' % result)

    connection.commit()


def insertUrlToken(connection, urlToken, followerUrlToken):
    with connection.cursor() as cursor:
        sql = 'INSERT INTO `URL_TOKEN_TEST_5` (`urlToken`, `followerUrlToken`) VALUES (%s, %s)'
        valueTuple = (urlToken, followerUrlToken)

        cursor.execute(sql, valueTuple)

    connection.commit()


if __name__ == '__main__':
    connection = connect()

    userInfo = 'testInfo'

    insertUserInfo(connection, userInfo)
