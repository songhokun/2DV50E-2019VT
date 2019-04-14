#!/usr/bin/python3

import json
from collections import defaultdict
import urllib.request
import zipfile
from glob import glob
import os

dir_name, _ = os.path.split(os.path.abspath(__file__))
websites_dir = os.path.join(dir_name, 'websites')
csv_filepath = os.path.join(websites_dir, 'top-1m.csv')
json_filepath = os.path.join(websites_dir, 'web_dic.json')
html_filepath = os.path.join(websites_dir, 'bookmark.html')

class WebsitePair(object):
    def __init__(self, rank, url):
        self.rank = rank
        self.url = url

        splitted_url = url.split('.')
        if splitted_url[-1]:
            self.tld = splitted_url[-1]
        else:
            self.tld = '.'

    def __str__(self):
        return self.url

    # https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def is_there_csvfile():
    return os.path.exists(csv_filepath)


def read_csv_file(max_entry=-1):
    """
    This method reads a alexa rank csv file
    :param max_entry: maximum entry per TLD
    :return: a dictionary collection sorted by tld if a file exists
    """

    website_dict = defaultdict(list)
    if not is_there_csvfile():
        return ""

    with open(csv_filepath, 'r') as alexafile:
        for line in alexafile:
            data = line.rstrip().split(',')
            temp = WebsitePair(data[0], data[1])
            if max_entry != -1 and len(website_dict[temp.tld]) < max_entry:
                website_dict[temp.tld].append(temp.url)

    return website_dict


def fetch_alexa_list():
    """
    The method downloads a zip file of alexa top 1 million statistics and unzips the content.
    :return: path of the extracted CSV file
    """
    if not os.path.exists(websites_dir):
        os.mkdir(websites_dir)
    url = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
    filename, headers = urllib.request.urlretrieve(url, filename=os.path.join(websites_dir, 'top-1m.csv.zip'))

    with zipfile.ZipFile(filename, 'r') as alexa_zipfile:
        alexa_zipfile.extractall(websites_dir)

    return glob(os.path.join(websites_dir, '*.csv'))


def write_dict_to_json(website_dict):
    """
    :param website_dict:
    :return:
    """
    with open(json_filepath, 'w') as output_file:
        json.dump(website_dict, output_file)


def read_json_to_dict():
    website_dic = defaultdict(list)

    if os.path.exists(json_filepath):
        with open(json_filepath, 'r') as file_reader:
            website_dic = json.load(file_reader)

    return website_dic


def dict_to_bookmark(website_dict):
    with open(html_filepath, 'w') as output_file:
        output_file.write('<!DOCTYPE NETSCAPE-Bookmark-file-1>\n'
                              '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n'
                              '<TITLE>Bookmarks</TITLE>\n'
                              '<H1>Bookmarks Menu</H1>\n'
                              '<DL><p>\n')
        for tld in website_dict.keys():
            output_file.write('\t<DT><H3 ADD_DATE="1551622567" LAST_MODIFIED="1553349030">' + tld + '</H3>\n')
            output_file.write('\t<DL><p>\n')
            for site in website_dict[tld]:
                output_file.write('\t\t<DT><A HREF="http://' + site + '/" >' + site + '</A>\n')
            output_file.write('\t</DL><p>\n')
