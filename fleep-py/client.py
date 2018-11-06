import json
import logging
import os

import requests


class FleepClient:
    def __init__(self):
        self.event_horizon = 0

    def connect(self):
        email = os.environ['FLEEP_EMAIL']
        password = os.environ['FLEEP_PASSWORD']
        self.session = requests.Session()
        r = self.session.post(
            "https://fleep.io/api/account/login",
            headers={"Content-Type": "application/json"},
            data=json.dumps({
                "email": email,
                "password": password
            }))

        if r.status_code != 200:
            logging.error(r)
            return

        logging.info("connected")
        self.ticket = r.json()['ticket']
        self.token_id = r.cookies['token_id']
        self.recv()


    def send(self, conv_id, msg, attachments=None):
        data = {"message": msg, "ticket": self.ticket}
        if attachments:
            data['attachments'] = attachments

        r = self.session.post(
            "https://fleep.io/api/message/send/{}".format(conv_id),
            headers={"Content-Type": "application/json"},
            cookies={"token_id": self.token_id},
            data=json.dumps(data))
        logging.info(">> sent")

        if 'result_message_nr' in r.json():
            return r.json()['result_message_nr']


    def upload(self, conv_id, data, name):
        r = self.session.post(
            "https://fleep.io/api/file/upload/?ticket={}".format(self.ticket),
            cookies={"token_id": self.token_id},
            files={"files": (name, data)})

        if r.json()['files']:
            return r.json()['files'][0]['upload_url']


    def recv(self):
        r = self.session.post(
            "https://fleep.io/api/account/poll",
            headers={"Content-Type": "application/json"},
            cookies={"token_id": self.token_id},
            data=json.dumps({
                "wait": True,
                "event_horizon": self.event_horizon,
                "ticket": self.ticket,
                "poll_flags": ["skip_hidden"]
            }))

        if r.status_code != 200:
           logging.error(r)
           return
 
        recv_json = r.json()
        self.event_horizon = recv_json['event_horizon']
        return recv_json['stream']


    def delete(self, conv_id, message_nr):
        r = self.session.post(
            "https://fleep.io/api/message/delete/{}".format(conv_id),
            headers={"Content-Type": "application/json"},
            cookies={"token_id": self.token_id},
            data=json.dumps({
                "message_nr": message_nr,
                "ticket": self.ticket
            }))
        if r.status_code != 200:
            logging.error(r)
            logging.error(r.json())
            return


    def edit(self, conv_id, message_nr, msg, attachments=None):
        data = {"message": msg, "ticket": self.ticket, "message_nr": message_nr}
        if attachments:
            data['attachments'] = attachments

        r = self.session.post(
            "https://fleep.io/api/message/edit/{}".format(conv_id),
            headers={"Content-Type": "application/json"},
            cookies={"token_id": self.token_id},
            data=json.dumps(data))
        logging.info(">> edited")
        
        if 'result_message_nr' in r.json():
            return r.json()['result_message_nr']

    def who(self, account_id):
        r = self.session.post(
            "https://fleep.io/api/account/lookup",
            headers={"Content-Type": "application/json"},
            cookies={"token_id": self.token_id},
            data=json.dumps({
                "lookup_list": [account_id]
            }))

        if r.status_code != 200:
            logging.error(r)
            logging.error(r.json())
            return
        print(r.json())
        
