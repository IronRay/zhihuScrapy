# -*- coding: utf-8 -*-
import os
import json

from bs4 import BeautifulSoup

import zhihuGet
from config import ABSDIR


class User():
    """docstring for user"""

    def __init__(self, urlToken):
        # Waiting for handler
        self.infoList = ['userType',
                         'urlToken',
                         'name',
                         'gender',
                         'avatarUrl',
                         'locations',
                         'educations',
                         'employments',
                         'business',
                         'questionCount',
                         'answerCount',
                         'articlesCount',
                         'logsCount',
                         'favoriteCount',
                         'participatedLiveCount',
                         'hostedLiveCount',
                         'followingCount',
                         'followingQuestionCount',
                         'followingTopicCount',
                         'followingFavlistsCount',
                         'followingColumnsCount',
                         'followerCount',
                         'markedAnswersCount',
                         'voteupCount',
                         'favoritedCount',
                         'thankedCount']

        # self.delInfoList = ['headline',
        #                     'description']

        self.urlToken = urlToken
        self.type = 'user'
        self.url = self.urlGenerator()
        self.pageContent = ''
        self.userInfo = {}
        self.userFollowings = []

    def urlGenerator(self):
        baseUrl = 'https://www.zhihu.com'
        pageType = 'people'

        url = baseUrl + pageType + '/' + self.urlToken + '/' + 'following'

        return url

    def userInfoGenerator(self, userDict):
        userInfo = {
            'userType': '',
            'urlToken': '',
            'name': '',
            'gender': 3,
            'avatarUrl': '',
            'locations': [],
            'educations': [],
            'employments': [],
            'business': '',
            'questionCount': 0,
            'answerCount': 0,
            'articlesCount': 0,
            'logsCount': 0,
            'favoriteCount': 0,
            'participatedLiveCount': 0,
            'hostedLiveCount': 0,
            'followingCount': 0,
            'followingQuestionCount': 0,
            'followingTopicCount': 0,
            'followingFavlistsCount': 0,
            'followingColumnsCount': 0,
            'followerCount': 0,
            'markedAnswersCount': 0,
            'voteupCount': 0,
            'favoritedCount': 0,
            'thankedCount': 0
        }

        try:
            for key in userInfo.keys():
                if key not in userDict.keys():
                    userInfo[key] = 'None'
                else:
                    if key in ['locations', 'educations', 'employments', 'business']:
                        if key == 'locations':
                            for location in userDict[key]:
                                userInfo[key].append(location['name'])
                        elif key == 'educations':
                            userEducation = {'school': '', 'major': ''}

                            for education in userDict[key]:
                                if 'school' in education.keys():
                                    userEducation['school'] = education['school'].get('name')

                                if 'major' in education.keys():
                                    userEducation['major'] = education['major'].get('name')

                                userInfo[key].append(userEducation)
                        elif key == 'employments':
                            userEmployment = {'name': '', 'job': ''}

                            for employment in userDict[key]:
                                if 'company' in employment.keys():
                                    userEmployment['name'] = employment['company'].get('name', 'None')

                                if 'job' in employment.keys():
                                    userEmployment['job'] = employment['job'].get('name', 'None')

                                userInfo[key].append(userEmployment)
                        else:
                            userInfo[key] = userDict[key]['name']
                    else:
                        userInfo[key] = userDict[key]

        except KeyError as e:
            print('< Error: %s >' % e)
            print('< Key: %s >' % key)

        return userInfo

    def getPageContent(self):
        pageData = zhihuGet.getUrlData(self.url)
        pageContent = BeautifulSoup(pageData.text, 'lxml')

        self.pageContent = pageContent

        return pageContent

    def getUserInfo(self):
        userData = self.pageContent.find('div', {'id': 'data'})

        # print('< Data: %s >' % userData)

        convertToDict = json.loads(userData['data-state'])
        userDict = convertToDict['entities']['users'][self.urlToken]
        # print('< Dict: %s >' % userDict)

        userInfo = self.userInfoGenerator(userDict)

        self.userInfo = userInfo

        return userInfo

    def getUserFollowings(self, limits=10):
        userFollowings = []

        maxOffset = int(self.userInfo['followingCount'])

        minOffset = 0

        for offset in range(minOffset, maxOffset, limits):
            try:
                response = zhihuGet.getApiData(self.urlToken, offset, limits)
                responseContent = BeautifulSoup(response.text, 'lxml').find('p').get_text()

                # print('< Content: %s >' % responseContent)
                responseDict = json.loads(responseContent)

            except Exception as e:
                print('< Error: %s >' % e)
                continue

            for userData in responseDict['data']:
                userFollowings.append(userData['url_token'])

        self.userFollowing = userFollowings

        return userFollowings

    def outputUserInfo(self):
        for key in self.infoList:
            print('< key: %s >< value: %s >' % (key, self.userInfo[key]))


class Question(object):
    """docstring for Question"""

    def __init__(self, id):
        self.id = id


class Answer(object):
    """docstring for Answer"""

    def __init__(self, id, questionID, questionTitle):
        self.id = id
        self.type = 'answer'
        self.questionID = questionID
        self.questionTitle = questionTitle
        self.url = self.urlGenerator()

    def urlGenerator(self):
        baseUrl = 'https://www.zhihu.com'

        url = '%s/question/%s/%s/%s' % (baseUrl, self.questionID, self.type, self.id)

        return url

    def getAnswerContent(self):
        answerData = zhihuGet.getUrlData(self.url)
        rawAnswerContent = BeautifulSoup(answerData.text, 'lxml')

        answerContent = rawAnswerContent.find('div', {'class', 'zh-question-answer-wrapper'})

        return answerContent

    def saveImgs(self, answerContent):
        imgs = answerContent.findAll('img', {'class': 'origin_image'})

        for img in imgs:
            imgUrl = img.get('data-original')

            self.saveImg(imgUrl=imgUrl)

    def saveImg(self, imgUrl):
        imgName = imgUrl.split('/')[-1]

        questionName = '%s_%s' % (self.questionID, self.questionTitle)

        questionPath = os.path.join(ABSDIR, questionName)
        answerPath = os.path.join(questionPath, str(self.id))
        imgPath = os.path.join(answerPath, str(imgName))

        if not os.path.exists(questionPath):
            os.mkdir(questionPath)
            os.mkdir(answerPath)
        else:
            if not os.path.exists(answerPath):
                os.mkdir(answerPath)

        if not os.path.isfile(imgPath):
            picData = zhihuGet.getUrlData(imgUrl, useCookie=False).content

            with open(imgPath, 'wb') as jpg:
                jpg.write(picData)

    def saveContent():
        pass


class Collection(object):
    """docstring for Collection"""

    def __init__(self, id):
        self.id = id
        self.type = 'collection'
        self.url = self.urlGenerator()

    def urlGenerator(self):
        baseUrl = 'https://www.zhihu.com'

        url = '%s/%s/%s' % (baseUrl, self.type, self.id)

        return url

    def getCollectedAnswer(self, pageNum=1):
        params = {
            'page': pageNum
        }

        collectionData = zhihuGet.getUrlData(url=self.url, params=params)
        collectionContent = BeautifulSoup(collectionData.text, 'lxml')

        num = collectionContent.find('a', text='下一页')

        if num:
            nextPageNum = num.get('href').split('=')[-1]
        else:
            nextPageNum = 0

        answerPreviews = collectionContent.findAll('div', {'class': 'zm-item'})

        for content in answerPreviews:
            questionTitle = content.h2.a.get_text().strip()
            url = content.find('link', {'itemprop': 'url'}).get('href')

            questionID = url.split('/')[2]
            answerID = url.split('/')[4]

            answer = Answer(id=answerID, questionID=questionID, questionTitle=questionTitle)
            answerContent = answer.getAnswerContent()

            if answerContent:
                answer.saveImgs(answerContent=answerContent)
            else:
                continue

        print(len(answerPreviews))

        return nextPageNum

    def getAllCollectedAnswers(self):
        pageNum = 1

        while pageNum:
            pageNum = self.getCollectedAnswer(pageNum)


if __name__ == '__main__':
    # My class test case
    collection = Collection(id='')
    collection.getAllCollectedAnswers()
