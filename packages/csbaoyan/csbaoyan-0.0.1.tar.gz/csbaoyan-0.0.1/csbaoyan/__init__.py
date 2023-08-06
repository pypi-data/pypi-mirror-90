#!/usr/bin/env python
# encoding=utf-8

import requests
import requests

def csbaoyan():
	url = "https://gitee.com/anaivebird/csbaoyan/raw/master/csbaoyan"
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
	result = requests.get(url, headers=headers)
	print(result.content.decode())