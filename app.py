import json

from flask import Flask, render_template, send_from_directory, request
import os
from flask_cors import CORS
import episodes_crawler
from utils import requests_util

app = Flask(__name__)
CORS(app)

video_root_dir = 'D:/videos/'


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')


@app.route("/download/<dir>/<filename>")
def download_file(dir, filename):
    directory = os.path.abspath(video_root_dir + dir + '/')
    return send_from_directory(directory, filename, as_attachment=True)


@app.route("/find_all_videos", methods=['GET', 'POST'])
def find_m3u8_url():
    url = request.form.get('url')
    result_arr = episodes_crawler.main(url, 1)
    return json.dumps(result_arr)


if __name__ == '__main__':
    app.run()

