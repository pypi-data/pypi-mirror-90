import requests
import time
import hashlib
import json
from pyqccapi import api_config

encode = 'utf-8'
url_base = 'http://api.qichacha.com/'

dict_method_url = api_config.to_method_url_dict()


class Task:
    def __init__(self, method, params):
        self.method = method
        self.params = params


class ApiInvoker:

    def __init__(self, config_path):
        self.config = api_config.to_config(config_path)

    def to_token(self, timespan):
        token = self.config['appkey'] + timespan + self.config['seckey']
        hl = hashlib.md5()
        hl.update(token.encode(encoding=encode))
        return hl.hexdigest().upper()

    def to_header(self):
        timespan = str(int(time.time()))
        return {'Token': self.to_token(timespan), 'Timespan': timespan}

    def invoke(self, task: Task):
        result = {
            'success': False,
            'code': '',
            'data': None
        }
        url_req = dict_method_url[task.method]
        params = task.params
        params['key'] = self.config['appkey']

        r = requests.get(url=url_req,
                         headers=self.to_header(),
                         params=params)
        if r.status_code == 200:
            j = json.dumps(str(r.content, encoding=encode))
            result['data'] = j.encode(encode).decode("unicode-escape")
            result['success'] = True
        else:
            result['code'] = r.status_code
        return result


# params = {
#     'keyword': '长风',
#     'provinceCode': 'SH'
# }
# task = Task('8d23ff9d-a8ee-4c32-99d3-2129f101617b', params)
# invoker = ApiInvoker('config.yaml')
# result = invoker.invoke(task)
# print(result)
