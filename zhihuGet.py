# -*- coding: utf-8 -*-
import random
import requests

from config import ZHIHUGetConfig


USER_AGENTS = ZHIHUGetConfig['USER_AGENTS']


def getUrlData(url, params=None):
    HEADER = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    }

    headers = HEADER

    # print('< UA: %s >' % headers['User-Agent'])

    # cookie
    cookies = ZHIHUGetConfig['cookies']

    response = requests.get(url, headers=headers, cookies=cookies, params=params, timeout=30)

    # print('< Get URL Data Status_code: %s >' % response.status_code)
    # print('< Text: %s >' % response.text)

    return response


def getApiData(urlToken, offset='0', limit='10'):
    HEADER = {
        'User-Agent': random.choice(USER_AGENTS),
    }

    headers = HEADER

    headers['authorization'] = ZHIHUGetConfig['authorization']

    baseApiUrl = 'https://www.zhihu.com/api'
    version = 'v4'
    requestType = 'members'
    responseType = 'followees'

    params = {'include': 'data[*].answer_count,articles_count,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics',
              'offset': str(offset),
              'limit': str(limit),
              }

    url = baseApiUrl + '/' + version + '/' + requestType + '/' + urlToken + '/' + responseType

    response = requests.get(url=url, headers=headers, params=params, timeout=10)

    # print('< Get API Data Status_code: %s >' % response.status_code)
    # print('< Text: %s >' % response.text)

    return response


if __name__ == '__main__':

    getApiData(urlToken='chibaole', offset='10', limit='30')
