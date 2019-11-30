# Date: 11/29/2019
# Author: Mohamed
# Description: A Simple Discord message deleter

import time
import json
import requests


config_file = 'config.json'


class Deleter:

    api = 'https://discordapp.com/api/v6/channels'

    def __init__(self, auth_token, chan_id, latest_msg_id, is_admin_user):
        self.latest_msg_id = latest_msg_id
        self.base_url = f'{self.api}/{chan_id}/messages'

        self.user_id = None
        self.is_alive = True
        self.is_done = False
        self.chan_id = chan_id
        self.total_deleted = 0
        self.is_admin_user = is_admin_user

        self.headers = {
            'Authorization': auth_token,
            'content-type': 'application/json',
        }

    def get_user_id(self, msg_id):
        url = f'{self.base_url}/{msg_id}'

        try:
            resp = requests.patch(url, data=json.dumps({}),
                                  headers=self.headers).json()
            return resp['author']['id']
        except:
            pass

    def get_messages(self):

        messages = []
        url = f'{self.base_url}?before={self.latest_msg_id}&limit=100'

        if not self.is_admin_user and self.user_id == None:
            self.user_id = self.get_user_id(self.latest_msg_id)

            if not self.user_id:
                self.is_done = True
                return messages

        try:
            msgs = requests.get(url, headers=self.headers).json()

            for msg in msgs:
                msg_id = msg['id']

                if not self.is_admin_user:
                    if msg['author']['id'] == self.user_id:
                        messages.append(msg_id)
                else:
                    messages.append(msg_id)

            self.delete_msg(self.latest_msg_id)
        except:
            pass
        finally:
            if not messages:
                self.is_done = True

        return messages

    def delete_msg(self, msg_id: str):
        url = f'{self.base_url}/{msg_id}'

        try:
            requests.delete(url, headers=self.headers)
            self.total_deleted += 1

            print(f'Total messages deleted: {self.total_deleted:02}')
            time.sleep(0.5)
        except:
            pass

    def error_check(self):
        url = f'{self.api}/{self.chan_id}/messages?limit=1'
        r = requests.get(url, headers=self.headers).json()

        if 'code' in r:
            code = r['code']

            if code == 0:
                print('Error: Invalid authorization token')
                exit()
            elif code == 10003:
                print('Error: Invalid channel id')
                exit()

            print(f'Error: {r["message"]}')
            exit()

        url = f'{self.base_url}/{self.latest_msg_id}'

        resp = requests.patch(url, data=json.dumps({}),
                              headers=self.headers).json()

        if 'code' in resp:
            if resp['code'] == 10008:
                print('Error: Invalid message id')
                exit()

    def start(self):

        self.error_check()
        while self.is_alive and not self.is_done:
            messages = self.get_messages()

            if not messages:
                continue

            while len(messages) > 1:
                msg_id = messages.pop()
                self.delete_msg(msg_id)

            self.latest_msg_id = messages.pop()


if __name__ == '__main__':

    with open(config_file, 'rt') as f:
        data = json.load(f)

    auth_token = data['authorizationToken']
    channel_id = data['channelID']
    message_id = data['messageID']
    is_admin_user = data['isAdminUser']

    Deleter(auth_token, channel_id, message_id, is_admin_user).start()
