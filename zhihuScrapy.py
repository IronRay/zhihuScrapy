# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import json

import zhihuGet


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
        self.url = self.urlGenerator()
        self.pageContent = ''
        self.userInfo = {}
        self.userFollowings = []

    def urlGenerator(self):
        baseUrl = 'https://www.zhihu.com'
        pageType = 'people'

        url = baseUrl + '/' + pageType + '/' + self.urlToken + '/' + 'following'

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


if __name__ == '__main__':
    # My class test case
    user = User(urlToken='mmymmy')
    user.getUserInfo()
