import datetime
import urllib3
import threading
from queue import Queue
from utils.requests_util import *

url_queue = Queue()


'''
from m3u8 file, get all ts file urls
m3u8_path - http://cn4.18787000118.com/hls/20200321/4dfaf4acba8a1de9ddad068068069cd1/index.m3u8
base_url - http://cn4.18787000118.com/hls/20200321/4dfaf4acba8a1de9ddad068068069cd1/
'''
def get_ts_urls(m3u8_path, base_url):
    headers = {'Content-Type': 'application/json', 'Connection': 'keep-alive'}
    session = get_http_session(pool_connections=10, pool_maxsize=20, max_retries=5)
    r = session.get(m3u8_path, headers=headers)
    time_stamp = '{0:%Y-%m-%d-%H-%M}'.format(datetime.datetime.now())
    local_path = './m3u8' + time_stamp

    with open(local_path, "wb") as m3u8_file:
        m3u8_file.write(r.content)

    with open(local_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.endswith(".ts\n"):
                # print(base_url + line)
                line = line.strip("\n")
                line = line.split("/")[-1]
                url_queue.put(base_url + line.strip("\n"))


'''
download file
'''
def download(download_path, session):
    while True:
        ts_url = url_queue.get()
        if ts_url is None:
            break
        file_name = ts_url.split("/")[-1]
        print('开始下载 %s' % ts_url)
        start = datetime.datetime.now().replace(microsecond=0)
        try:
            headers = {'Connection': 'keep-alive'}
            response = session.get(ts_url, stream=True, verify=False, headers=headers)
        except Exception as e:
            print("异常请求：%s" % e.args)
            return
        ts_path = download_path + '/' + file_name
        with open(ts_path, "wb+") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

        end = datetime.datetime.now().replace(microsecond=0)
        print("耗时：%s" % (end - start))


def main(m3u8_url, base_url, download_path):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    get_ts_urls(m3u8_url, base_url)
    threads = []

    thread_num = 5
    for i in range(thread_num):
        session = get_http_session(pool_connections=10, pool_maxsize=20, max_retries=5)
        t = threading.Thread(target=download, args=(download_path, session,))
        t.start()
        threads.append(t)

    url_queue.join()

    for i in range(thread_num):
        url_queue.put(None)

    for i in range(thread_num):
        t = threads[i]

    print('download finished')


# if __name__ == '__main__':
#     urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#     m3u8_url = 'https://us-4.wl-cdn.com/hls/20200321/e1413dc624a2e99a796825c995b9d02a/index.m3u8'
#     base_url = 'https://us-4.wl-cdn.com/hls/20200321/e1413dc624a2e99a796825c995b9d02a/'
#     download_path1 = 'C:/Users/admin/Desktop/laba_video'
#     threads = []
#
#     get_ts_urls(m3u8_url, base_url)
#
#     thread_num = 5
#     for i in range(thread_num):
#         session = get_http_session(pool_connections=10, pool_maxsize=20, max_retries=5)
#         t = threading.Thread(target=download, args=(download_path1, session,))
#         t.start()
#         threads.append(t)
#
#     url_queue.join()
#
#     for i in range(thread_num):
#         url_queue.put(None)
#
#     for i in range(thread_num):
#         t = threads[i]
#
#     print('download finished')
