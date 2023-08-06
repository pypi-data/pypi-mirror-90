#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AUTHOR: XYCoder
# FILE: ~/Desktop/Project/xyscript/xyscript/crawler/version.py
# DATE: 2021/01/05 Tue
# TIME: 14:00:05

# DESCRIPTION:用于实时爬取pypi.org本库最新版本

import requests
from bs4 import    BeautifulSoup
url = 'https://pypi.org/project/xyscript/'

class Version:
    def get_last_version():
        strhtml = requests.get(url)
        soup = BeautifulSoup(strhtml.text,'lxml')
        data = soup.select('#history > div > div.release.release--latest.release--current > a > p.release__version')
        version_string = data[0].get_text()
        version_string = version_string.strip()
        # version_string = version_string.replace(' ', '')
        # print(version_string)
        return version_string

if __name__ == "__main__":
    Version.get_last_version()
