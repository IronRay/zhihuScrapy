# -*- coding: utf-8 -*-
from multiprocessing import Pool
import os

import zhihuScrapy
import dataSaver


def worker(urlToken, num):
    print('< TaskNum: %s >< PID: %s >< Token: %s >< Start! >' % (num, os.getpid(), urlToken))

    user = zhihuScrapy.User(urlToken)
    userInfo = user.getUserInfo()
    userFollowings = user.getUserFollowings()
    # user.outputUserInfo()

    dataSaver.updateUserTokenStatus(urlToken=urlToken, status='1')
    dataSaver.insertUserInfo(userInfo=userInfo)

    for token in userFollowings:
        dataSaver.insertUrlTokenRelation(urlToken=token, followerUrlToken=urlToken)
        dataSaver.insertUrlToken(urlToken=token, status=0)

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
            urlTokenDicts = dataSaver.getUrlToken(numOfUrlToken=10, status=0)
            # print('<Dicts: %s >' % urlTokenDicts)
