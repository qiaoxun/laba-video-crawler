from bs4 import BeautifulSoup
from utils.requests_util import *
import re

# all episodes in the current page
episodes_m3u8_url = []
video_title = ''
video_root_dir = 'D:/videos/'


def parse_html(url, session, tab_index):
    html = download_html(url, session)
    soup = BeautifulSoup(html, 'html.parser')
    # 1. find video title
    global video_title
    video_title = soup.find('div', attrs={'class': 'title_line'}).h1.a.text

    # 2. find all episodes's url， could be 201-150332 also could be201-150332-watch-0-1
    ids = url.split('/')[-1]
    if ids.find('watch') > -1:
        ids_arr = ids.split('-')
        ids = ids_arr[0] + '-' + ids_arr[1]
    # data_type 1 - movie, 2 - tv
    data_type = soup.find('a', attrs={'class': 'huan-yi-huan more fr'}).get('data-type')
    find_all_episodes(ids, data_type, tab_index, session)


'''
get the result of http://www.labayy.com/common/api_getTargetRsBoxData.php
'''
def find_all_episodes(ids, data_type, tab_index, session):
    url = 'http://www.labayy.com/common/api_getTargetRsBoxData.php'
    data = {
        'order': 'getTargetRsBoxData',
        'ids': ids,
        'type': data_type,
        'index': tab_index
    }
    json_data = post_with_form_data_return_json(url, data)
    episodes = json_data['data']['episodes']
    if type(episodes) is list:
        for epi in episodes:
            epi_url = epi['url']
            epi_title = epi['title']
            if epi_url.endswith('.m3u8'):
                get_real_m3u8_url(epi_url, epi_title, session)
                episodes_m3u8_url.append({'episode_title': epi_title, 'm3u8_url': epi_url, 'video_title': video_title})
            else:
                # sometimes what we got is not a m3u8 url like https://qiaozhen.com.cn/share/MzM1NDk3JOesrDHpm4Y=
                m3u8_url = get_m3u8_url(epi_url, session)
                if m3u8_url.strip():
                    get_real_m3u8_url(m3u8_url, epi_title, session)
                    episodes_m3u8_url.append({'episode_title': epi_title, 'm3u8_url': m3u8_url, 'video_title': video_title})


# sometimes what we got is not a m3u8 url like https://qiaozhen.com.cn/share/MzM1NDk3JOesrDHpm4Y=
def get_m3u8_url(url, session):
    print(url)
    try:
        html = download_html(url, session)
        print(html)
        soup = BeautifulSoup(html, 'html.parser')
        pattern = re.compile(r'url="(.*?)";', re.MULTILINE | re.DOTALL)
        script = soup.find("script", text=pattern)
        m3u8_url = pattern.search(script.text).group(1)
        return m3u8_url
    except Exception as e:
        print(e)
        print('failed to ' + url)
        return ''


# some m3u8 file are like
# #EXTM3U
# #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=800000,RESOLUTION=1080x608
# 1000k/hls/index.m3u8
def get_real_m3u8_url(m3u8_url, episode_title, session):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    headers = {
        'User-Agent': user_agent,
        'Connection': 'keep-alive'
    }
    r = session.get(url, headers=headers)
    dir_path = video_root_dir + video_title + '/' + episode_title + '/'
    file_path = save_file(url, session, dir_path)
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if lines[1].startswith('#EXT-X-STREAM-INF'):
            print(lines[1])
            last_uri = lines[2]
            m3u8_url = m3u8_url.replace('index.m3u8', last_uri)
            file.close()
            get_real_m3u8_url(m3u8_url, episode_title, session)


def main(url, tab_index):
    session = get_http_session()
    parse_html(url, session, tab_index)
    return episodes_m3u8_url


if __name__ == '__main__':
    url = 'http://www.labayy.com/movie-details/201-150332-watch-0-0'
    session = get_http_session()
    parse_html(url, session, 1)
    for u in episodes_m3u8_url:
        print(u)

