import argparse
import time
import json
from collections import Iterable
from operator import attrgetter
import re

from urllib.parse import urlparse, parse_qsl
import http.cookiejar as cookielib
import urllib.request
import urllib.parse
from html.parser import HTMLParser

import requests

class MyParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.url = None
        self.params = {}
        self.in_form = False
        self.form_parsed = False
        self.method = "GET"

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "form":
            self.in_form = True

        if not self.in_form:
            return

        attrs = dict((name.lower(), value) for name, value in attrs)

        if tag == "form":
            self.url = attrs["action"]
            if "method" in attrs:
                self.method = attrs["method"].upper()

        elif tag == "input" and "type" in attrs and "name" in attrs:

            if attrs["type"] in ["hidden", "text", "password"]:
                self.params[attrs["name"]] =\
                 attrs["value"] if "value" in attrs else ""

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "form":
            if not self.in_form:
                raise RuntimeError("Unexpected end of <form>")

            self.in_form = False
            self.form_parsed = True

class API(object):
    def __init__(self,
                 app_id=None,
                 user_login=None,
                 user_password=None,
                 access_token=None,
                 scope='offline',
                 timeout=300,
                 api_version='5.28'):

        self.app_id = app_id
        self.user_login = user_login
        self.user_password = user_password

        self.scope = scope
        self.api_version = api_version

        self.default_timeout = timeout

        if not access_token and (user_login or user_password):
            try:
                self.get_access_token()
            except Exception:
                self.access_token = self.get_token()
        else:
            self.access_token = access_token

        self.session = requests.Session()
        self.session.headers['Accept'] = 'application/json'
        self.session.headers['Content-Type'] =\
         'application/x-www-form-urlencoded'

    #not work anymore
    def get_access_token(self):
        session = requests.Session()

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
                except ValueError:
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

    def get_token(self):
        def split_key_value(key_value_pair):
            key_value = key_value_pair.split("=")
            return key_value[0], key_value[1]

        def auth_user(email, password, client_id, scope, opener):
            response = opener.open(
                "http://oauth.vk.com/oauth/authorize?" + \
                "redirect_uri=http://oauth.vk.com/blank.html&" + \
                "response_type=token&" + \
                "client_id=%s&scope=%s&display=wap" % (client_id, ",".join(scope))
                )
            doc = response.read().decode()
            parser = MyParser()
            parser.feed(doc)
            parser.close()

            if not parser.form_parsed or parser.url is None \
             or "pass" not in parser.params or \
                "email" not in parser.params:
                raise RuntimeError("Something wrong")

            parser.params["email"] = email
            parser.params["pass"] = password

            if parser.method == "POST":
                response = opener.open(
                    parser.url, urllib.parse.urlencode(parser.params).encode())
            else:
                raise NotImplementedError("Method '%s'" % parser.method)
            return response.read(), response.geturl()

        def give_access(doc, opener):
            parser = MyParser()
            parser.feed(doc.decode())
            parser.close()
            if not parser.form_parsed or parser.url is None:
              raise RuntimeError("Something wrong")

            if parser.method == "POST":
                response = opener.open(
                    parser.url, urllib.parse.urlencode(parser.params).encode())
            else:
                raise NotImplementedError("Method '%s'" % parser.method)
            return response.geturl()


        if not isinstance(self.scope, list):
            self.scope = [self.scope]

        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cookielib.CookieJar()),
            urllib.request.HTTPRedirectHandler())

        data, url = auth_user(self.user_login, self.user_password, self.app_id, self.scope, opener)
        if urlparse(url).path != "/blank.html":
            url = give_access(data, opener)

        if urlparse(url).path != "/blank.html":
            raise RuntimeError("Expected success here")

        answer =\
         dict(
            split_key_value(key_value_pair) for key_value_pair in urlparse(url)
            .fragment.split("&"))

        if "access_token" not in answer or "user_id" not in answer:
            raise RuntimeError("Missing some values in answer")
        return answer["access_token"]


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
               self.first_name.encode('cp866','replace').decode('cp866','replace')\
               + ' ' +\
               self.last_name.encode('cp866','replace').decode('cp866','replace')\
               + ' Friends:' \
               + str(self.friends_count)\
               + ' Likes:' +\
               str(self.gav_gav)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='VK client for calculate popularity of your friend')
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
            print("Fetching data:" + str(int(i/l*100)) + '%')
        except KeyError:
            print('The user was deleted: ' + str(all_friends_uid[i]))

    s = sorted(friends, key=attrgetter('popularity'), reverse=True)
    for i in s:
        print(i)
