# -*- coding: utf-8 -*-

import pymysql
# import getpass
import json


def connect():

    # host = input('Host:')
    # user = input('User:')
    # password = getpass.getpass('Password:')
    # db = input('DB:')

    host = 'localhost'
    user = 'ray'
    password = 'codeForRay123'
    db = 'ZHIHU_SCRAPING'

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

    connection.autocommit(True)

    return connection


def insertUserInfo(userInfo):
    connection = connect()

    locations = json.dumps(userInfo['locations'], ensure_ascii=False)
    educations = json.dumps(userInfo['educations'], ensure_ascii=False)
    employments = json.dumps(userInfo['employments'], ensure_ascii=False)

    with connection.cursor() as cursor:
        sql = 'INSERT INTO `USER_INFO_TEST_5` (`userType`, `urlToken`, `name`, `gender`, `avatarUrl`,`locations`, `educations`, `employments`,  `business`, `questionCount`, `answerCount`, `articlesCount`, `logsCount`, `favoriteCount`, `participatedLiveCount`, `hostedLiveCount`, `followingCount`, `followingQuestionCount`, `followingTopicCount`, `followingFavlistsCount`, `followingColumnsCount`, `followerCount`, `markedAnswersCount`, `voteupCount`, `favoritedCount`, `thankedCount`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
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
        cursor.close()

    connection.commit()

    connection.close()


def insertUrlTokenRelation(urlToken, followerUrlToken):
    connection = connect()

    with connection.cursor() as cursor:
        sql = 'INSERT INTO `URL_TOKEN_RELATION_TEST_5` (`urlToken`, `followerUrlToken`) VALUES (%s, %s)'
        valueTuple = (urlToken, followerUrlToken)

        cursor.execute(sql, valueTuple)
        cursor.close()

    connection.commit()

    connection.close()


def insertUrlToken(urlToken, status):
    connection = connect()

    with connection.cursor() as cursor:
        sql = 'INSERT INTO `URL_TOKEN_TEST_5` (`urlToken`, `status`) VALUES (%s, %s)'
        valueTuple = (urlToken, status)

        cursor.execute(sql, valueTuple)
        cursor.close()

    connection.commit()

    connection.close()


def updateUserTokenStatus(urlToken, status):
    connection = connect()

    with connection.cursor() as cursor:
        sql = 'UPDATE `URL_TOKEN_TEST_5` SET status = %s WHERE urlToken = %s'
        valueTuple = (status, urlToken)

        cursor.execute(sql, valueTuple)
        cursor.close()

    connection.commit()

    connection.close()


def getUrlToken(numOfUrlToken=10, status=0):
    connection = connect()

    with connection.cursor() as cursor:
        sql = 'SELECT urlToken FROM `URL_TOKEN_TEST_5` WHERE status=%s LIMIT %s'
        valueTuple = (status, numOfUrlToken)

        cursor.execute(sql, valueTuple)

        result = cursor.fetchall()

        cursor.close()

    connection.close()

    return result


if __name__ == '__main__':

    # userInfo = 'testInfo'

    # insertUserInfo(connection, userInfo)

    print(type(getUrlToken()))
    print(getUrlToken())
