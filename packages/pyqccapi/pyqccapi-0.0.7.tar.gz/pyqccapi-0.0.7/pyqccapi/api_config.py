import yaml
import requests
import json
import pywildcard


def to_config(path_yaml: str):
    with open(path_yaml, 'r', encoding='utf-8') as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)


headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,zh;q=0.8,zh-TW;q=0.7",
    "authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIiLCJjcmVhdGVUaW1lIjoxNjA5NTEwNDI2LCJhY2NvdW50Tm8iOiIxODkxNzYxODUwOSIsImlzcyI6IlNhY2hpZWwuWmhhbyIsInVzZXJJZCI6ImUzMTJmMWRkN2Q4M2U0ZDQyM2IyODg2NzY5ZjZjYWY1In0.gaKAuPN2Z0i92dFE6rpbCWxTHoiWUL3F0zp4S9DuRJg",
    "content-type": "application/x-www-form-urlencoded",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "Hm_lvt_5cd3bf91755d53008b430f15579b08c6=1609471544; _uab_collina=160947879460966050149085; token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIiLCJjcmVhdGVUaW1lIjoxNjA5NTEwNDI2LCJhY2NvdW50Tm8iOiIxODkxNzYxODUwOSIsImlzcyI6IlNhY2hpZWwuWmhhbyIsInVzZXJJZCI6ImUzMTJmMWRkN2Q4M2U0ZDQyM2IyODg2NzY5ZjZjYWY1In0.gaKAuPN2Z0i92dFE6rpbCWxTHoiWUL3F0zp4S9DuRJg; shopCartCnt=0; UserBalance=399.9; isUserAuthentication=false; Hm_lpvt_5cd3bf91755d53008b430f15579b08c6=1609511337; getCurrentDataNav=6c02d82a-ebcc-4a3a-a933-49a4ea5e4087"
}


def deserialize(p):
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)


def serialize(p, l):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(l, f, ensure_ascii=False)


def to_category_list():
    url = 'https://openapi.qcc.com/API/DataApi/index'
    r = requests.post(url=url, headers=headers)
    if r.status_code == 200:
        result = r.json()['result']
        serialize('category_list.json', result)


def to_api_list():
    url = 'https://openapi.qcc.com/API/DataApi/getApiList'
    data = {
        'pageNum': 1,
        'pageSize': 1000,
        'apiType': 'cate_all'
    }
    r = requests.post(url=url, headers=headers, data=data)
    if r.status_code == 200:
        api_list = r.json()['result']['apiPage']['list']
        serialize('api_list.json', api_list)


def to_method_list():
    url = 'https://openapi.qcc.com/API/DataApiDetail/getApiMethodTree'
    data = {
        'apiId': ''
    }
    method_list = []
    api_list = deserialize('api_list.json')
    for api in api_list:
        data['apiId'] = api['Id']
        r = requests.post(url=url, headers=headers, data=data)
        if r.status_code == 200:
            methods = r.json()['result']
            for method in methods:
                method['apiId'] = api['Id']
                method['apiTitle'] = api['Title']
                method_list.append(method)
        else:
            print(r.status_code)
    serialize('method_list.json', method_list)


def to_method_detail_list():
    url = 'https://openapi.qcc.com/API/DataApiDetail/getApiMethodDetailInfo'
    data = {
        'apiId': '',
        'methodApiId': ''
    }
    method_detail_list = []
    method_list = deserialize('method_list.json')
    for method in method_list:
        data['apiId'] = method['apiId']
        data['methodApiId'] = method['methodApiId']
        r = requests.post(url=url, headers=headers, data=data)
        if r.status_code == 200:
            detail = r.json()['result']
            detail['Method'] = method
            method_detail_list.append(detail)
        else:
            print(r.status_code)
    serialize('method_detail_list.json', method_detail_list)


def to_method_url_dict():
    method_url_dict = {}
    method_detail_list = deserialize('method_detail_list.json')
    for method_detail in method_detail_list:
        method_url_dict[method_detail['Method']['methodApiId']] = method_detail['Titles']['paramList']['apiUrl']
    return method_url_dict


def md_to_rst(from_file, to_file):
    response = requests.post(
        url='http://c.docverter.com/convert',
        data={'to': 'rst', 'from': 'markdown'},
        files={'input_files[]': open(from_file, 'rb')}
    )

    if response.ok:
        with open(to_file, "wb") as f:
            f.write(response.content)


def prettify(data):
    print(json.dumps(data, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))


def view_method(pattern):
    result = []
    method_list = deserialize('method_list.json')
    for method in method_list:
        if pywildcard.fnmatch(method['methodApiName'],pattern) or pywildcard.fnmatch(method['apiTitle'],pattern):
            result.append(method)
    prettify(result)


def view_method_detail(pattern):
    result = []
    method_detail_list = deserialize('method_detail_list.json')
    for method_detail in method_detail_list:
        if pywildcard.fnmatch(method_detail['Method']['methodApiName'],pattern) or \
                pywildcard.fnmatch(method_detail['Method']['apiTitle'],pattern):
            result.append(method_detail)
    prettify(result)


