import argparse
import time
import json
from collections import Iterable
from urllib.parse import urlparse, parse_qsl
from operator import attrgetter
import re

import requests


class API(object):
    def __init__(self,
                 app_id=None,
                 user_login=None,
                 user_password=None,
                 access_token=None,
                 scope='offline',
                 timeout=30,
                 api_version='5.28'):

        self.app_id = app_id
        self.user_login = user_login
        self.user_password = user_password

        self.scope = scope
        self.api_version = api_version

        self.default_timeout = timeout

        if not access_token and (user_login or user_password):
            self.get_access_token()
        else:
            self.access_token = access_token

        self.session = requests.Session()
        self.session.headers['Accept'] = 'application/json'
        self.session.headers['Content-Type'] = 'application/x-www-form-urlencoded'

    def get_access_token(self):
        session = requests.Session()

        # Login
        login_data = {
            'act': 'login',
            'utf8': '1',
            'email': self.user_login,
            'pass': self.user_password,
            'redirect_uri': 'https://oauth.vk.com/blank.html'
        }

        response = session.post('https://login.vk.com', login_data)

        if 'remixsid' in session.cookies or 'remixsid6' in session.cookies:
            pass
        elif 'sid=' in response.url:
            self.auth_captcha(response.content, session)
        elif 'act=authcheck' in response.url:
            self.auth_code(response.content, session)
        elif 'security_check' in response.url:
            self.phone_number(response.content, session)
        else:
            raise AuthorizationError('Authorization error (bad password)')

        # OAuth2
        oauth_data = {
            'response_type': 'token',
            'client_id': self.app_id,
            'scope': self.scope,
            'display': 'mobile',
        }
        response = session.post('https://oauth.vk.com/authorize', oauth_data)

        if 'access_token' not in response.url:
            form_action = re.findall(u'<form method="post" action="(.+?)">', response.text)
            if form_action:
                response = session.get(form_action[0])
            else:
                try:
                    json_data = response.json()
                except ValueError:  # not json in response
                    error_message = 'OAuth2 grant access error'
                else:
                    error_message = 'VK error: [{0}] {1}'.format(
                        json_data['error'],
                        json_data['error_description']
                    )
                session.close()
                raise AuthorizationError(error_message)

        session.close()

        parsed_url = urlparse(response.url)
        token_dict = dict(parse_qsl(parsed_url.fragment))
        if 'access_token' in token_dict:
            self.access_token = token_dict['access_token']
            self.expires_in = token_dict['expires_in']
        else:
            raise AuthorizationError('OAuth2 authorization error')


    def method_request(self, method_name, timeout=None, **method_kwargs):
        params = {
            'timestamp': int(time.time()),
            'v': self.api_version,
        }
        if self.access_token:
            params['access_token'] = self.access_token

        string_method_kwargs = {}
        for key, value in method_kwargs.items():
            if not isinstance(value, (str, bytes, bytearray)) and isinstance(value, Iterable):
                value = ','.join(map(str, value))
            string_method_kwargs[key] = value
        params.update(string_method_kwargs)
        url = 'https://api.vk.com/method/' + method_name

        return self.session.post(url, params, timeout=timeout or self.default_timeout)

    def captcha(self, error_data, method_name, **method_kwargs):
        raise MethodError(error_data)

    def auth_code(self, content, session):
        raise AuthorizationError('Authorization error (2-factor code is needed)')

    def auth_captcha(self, content, session):
        raise AuthorizationError('Authorization error (captcha)')

    def phone_number(self, content, session):
        raise AuthorizationError('Authorization error (phone number is needed)')


class VError(Exception):
    pass


class AuthorizationError(VError):
    pass


class MethodError(VError):
    __slots__ = ['error', 'code', 'message', 'request_params', 'redirect_uri']

    def __init__(self, error):
        super(MethodError, self).__init__()
        self.error = error
        self.code = error.get('error_code')
        self.message = error.get('error_msg')
        self.request_params = error.get('request_params')
        self.redirect_uri = error.get('redirect_uri')

    def __str__(self):
        error_message = '{self.code}.' \
                        ' {self.message}.' \
                        ' request_params = {self.request_params}'\
            .format(self=self)
        if self.redirect_uri:
            error_message += ',\nredirect_uri = "{self.redirect_uri}"'\
                .format(self=self)
        return error_message


class Friend:
    def __init__(self, uid, vkapi):
        self.uid = uid
        self.info = json.loads(vkapi.method_request('users.get', user_id = uid, fields='counters').text)['response']
        self.first_name = self.info[0]['first_name']
        self.last_name = self.info[0]['last_name']
        self.friends_count = int(self.info[0]['counters']['friends'])
        self.photos = json.loads(vkapi.method_request('photos.get', owner_id=uid,album_id='profile', extended=1).text)['response']
        self.gav_gav = 0
        for i in self.photos['items']:
            self.gav_gav += int(i['likes']['count'])
        self.popularity = self.gav_gav + self.friends_count

    def __str__(self):
        return str(self.popularity) + ' ' +\
               str(bytes(self.first_name, 'utf-8'))\
               + ' ' +\
               str(bytes(self.last_name,'utf-8'))\
               + ' Friends:' \
               + str(self.friends_count)\
               + ' Likes:' +\
               str(self.gav_gav)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='VK client for calculate popularity of your friend')
    parser.add_argument('user', help='user')
    parser.add_argument('password', help='password')
    parser.add_argument('appid', help='app id')
    args = parser.parse_args()
    vk_api = API(args.app_id,args.user, args.password, scope='friends,photos')
    owner_uid = int(json.loads(vk_api.method_request('users.get').text)['response'][0]['id'])

    all_friends_uid = json.loads(vk_api.method_request('friends.get', user_id=owner_uid, order='name').text)['response']['items']
    l = len(all_friends_uid)
    friends = []
    for i in range(len(all_friends_uid)):
        try:
            x = Friend(all_friends_uid[i], vk_api)
            time.sleep(1)
            friends.append(x)
            print(str(int(i/l*100)) + '%')
        except KeyError:
            print('Deleted: ' + str(all_friends_uid[i]))

    s = sorted(friends, key=attrgetter('popularity'), reverse=True)
    for i in s:
        print(i)