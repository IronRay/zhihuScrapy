# -*- coding: utf-8 -*-
from multiprocessing import Pool
import os

import baseClass
import dataGenerator


def worker(urlToken, num):
    print('< TaskNum: %s >< PID: %s >< Token: %s >< Start! >' % (num, os.getpid(), urlToken))

    user = baseClass.User(urlToken)
    userInfo = user.getUserInfo()
    userFollowings = user.getUserFollowings()
    # user.outputUserInfo()

    dataGenerator.updateUserTokenStatus(urlToken=urlToken, status='1')
    dataGenerator.insertUserInfo(userInfo=userInfo)

    for token in userFollowings:
        dataGenerator.insertUrlTokenRelation(urlToken=token, followerUrlToken=urlToken)
        dataGenerator.insertUrlToken(urlToken=token, status=0)

    print('< TaskNum: %s >< PID: %s >< Token: %s >< Finish! >' % (num, os.getpid(), urlToken))


if __name__ == '__main__':
    urlTokenDicts = []
    num = 0

    while True:

        if urlTokenDicts:
            workerPool = Pool(10)

            # print('<Dicts: %s >' % urlTokenDicts)

            for urlTokenDict in urlTokenDicts:
                num += 1

                urlToken = urlTokenDict['urlToken']

                workerPool.apply_async(worker, args=(urlToken, num))

            workerPool.close()
            workerPool.join()

            urlTokenDicts = []
        else:
            urlTokenDicts = dataGenerator.getUrlToken(numOfUrlToken=10, status=0)
            # print('<Dicts: %s >' % urlTokenDicts)
