import requests

class line_notify:
    def __init__(self, token_id):
        self.token_id = token_id

    def send_msg(self, msg):
        url = 'https://notify-api.line.me/api/notify'
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+self.token_id}
        requests.post(url, headers=headers, data = {'message':msg})