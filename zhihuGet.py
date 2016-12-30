# -*- coding: utf-8 -*-
import random
import requests


USER_AGENTS = [
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5"
]


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
    cookies = {"z_c0":
               '"Mi4wQUlCQ0FLdk1BQXNBZ01JRGMtNENDeGNBQUFCaEFsVk4zbVI4V0FDT1IwRWRqeXdlUFlvZ0pQMHJTQ2tCWTR0VVRB|1481962390|99f60599dd79d0cfa00678cebda3ee46306edb80"',
               "login":
               '"M2JlOTIxYTAxYzU1NDVjZTk5NjE0OWY5MDk1OTY4MDk=|1481955294|bc6b6c0e109a37bb827e3fb102d29a3be25ab1d2"',
               "n_c": "1",
               "q_c1": "873d8955799e43fe8b05f12979932618|1481955286000|1481955286000",
               "l_cap_id":
               '"MDc1OTkwYmRhYWMwNGMxOTg5Y2VjNWQ0MzM3ZTBiOWU=|1481955286|2183926147ed2c953092e67f9b21d8f41c1bbdf2"',
               "d_c0": '"AIDCA3PuAguPTvx05ZARA8WZa8zumYR7ezY=|1481955286"',
               "cap_id":
               '"ZTMzNDc2ZDI1ODdlNDc2YmI2ZjM0OWZjNDg3Njc2OGU=|1481955286|908bd75b06b5810f47ccf2bea82a6c82851308b0"'}

    response = requests.get(url, headers=headers, cookies=cookies, params=params, timeout=30)

    # print('< Get URL Data Status_code: %s >' % response.status_code)
    # print('< Text: %s >' % response.text)

    return response


def getApiData(urlToken, offset='0', limit='10'):
    HEADER = {
        'User-Agent': random.choice(USER_AGENTS),
    }

    headers = HEADER

    headers['authorization'] = 'Bearer Mi4wQUlCQ0FLdk1BQXNBWUlMMFZPSUZDeGNBQUFCaEFsVk41V3BfV0FCQmt6ZlNlTHBjNldYaGNhQlB6cGEyMGZDcTBR|1482164686|99f4a8f22c50f3e5162680664d343b378759abfd'

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
