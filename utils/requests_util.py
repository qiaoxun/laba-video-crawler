import requests
import json
import os


def download_html(url, session):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    headers = {
        'User-Agent': user_agent,
        'Content-Type': 'application/json',
        'Connection': 'keep-alive'
    }
    try:
        r = session.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except Exception as e:
        print(e)
        print('failed to download html')


'''
type 1 - movie, 2 - tv
data = 
{
    order: getTargetRsBoxData
    ids: 201-148746
    type: 2
    index: 7
}
'''
def post_with_form_data_return_json(url, data):
    data = requests.post(url, data).text
    json_data = json.loads(data)
    return json_data


def get_http_session(pool_connections=10, pool_maxsize=10, max_retries=10):
    session = requests.Session()
    # 创建一个适配器，连接池的数量pool_connections, 最大数量pool_maxsize, 失败重试的次数max_retries
    adapter = requests.adapters.HTTPAdapter(pool_connections=pool_connections,
                                            pool_maxsize=pool_maxsize, max_retries=max_retries)
    # 告诉requests，http协议和https协议都使用这个适配器
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def save_file(url, session, root_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
    path = root_path + url.split('/')[-1]
    try:
        if not os.path.exists(root_path):
            os.makedirs(root_path)
        if not os.path.exists(path):
            r = session.get(url, headers=headers)
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
            return path
        else:
            print('file already here')
            return path
    except Exception as e:
        print(e)
        print('error! failed to download')
