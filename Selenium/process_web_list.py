#!/usr/bin/python3

import os
from collections import defaultdict
from sys import exit
import urllib.request
import json
import zipfile
from glob import glob

MAX_ENTRY = 50


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

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    # https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable


def main():
    dir_name, _ = os.path.split(os.path.abspath(__file__))
    websites_dir = os.path.join(dir_name, 'websites')
    csv_filepath = os.path.join(websites_dir, 'top-1m.csv')

    website_dict = defaultdict(list)

    if not os.path.exists(csv_filepath):
        print("A CSV of Alexa list does not exist!")
        if not __fetch_alexa_list(websites_dir):
            print("It could not fetch the file!")
            exit(1)

    with open(csv_filepath, 'r') as alexafile:
        for line in alexafile:
            data = line.rstrip().split(',')
            temp = WebsitePair(data[0], data[1])
            if len(website_dict[temp.tld]) <= MAX_ENTRY:
                website_dict[temp.tld].append(temp.url)

    json_filepath = os.path.join(websites_dir, 'web_dic.json')
    with open(json_filepath, 'w') as output_file:
        json.dump(website_dict, output_file)


def __fetch_alexa_list(websites_dir):
    """
    The method downloads a zip file of alexa top 1 million statistics and unzips the content.
    :param websites_dir:
    :return: path of the extracted CSV file
    """
    if not os.path.exists(websites_dir):
        os.mkdir(websites_dir)
    url = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
    filename, headers = urllib.request.urlretrieve(url, filename=os.path.join(websites_dir, 'top-1m.csv.zip'))

    with zipfile.ZipFile(filename, 'r') as alexa_zipfile:
        alexa_zipfile.extractall(websites_dir)

    return glob(os.path.join(websites_dir, '*.csv'))


if __name__ == "__main__":
    main()