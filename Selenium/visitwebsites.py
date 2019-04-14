
#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from collections import defaultdict
import time
import os
import json


def advanced_main():
    doh_profile = __get_dns_over_https_profile()
    driver = webdriver.Firefox(firefox_profile=doh_profile)
  
    for alexawebsite in load_website_dict()['de']:
        try:
            driver.get("http://" + alexawebsite)
        except WebDriverException as identifier:
            print(alexawebsite + " was not accessible! \n" + identifier)
        time.sleep(3)

    driver.close()


def __get_dns_over_https_profile():
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('network.trr.mode', 2)
    firefox_profile.set_preference('network.trr.uri', 'https://mozilla.cloudflare-dns.com/dns-query')

    return firefox_profile


def load_website_dict():
    dir_name, _ = os.path.split(os.path.abspath(__file__))
    websites_dir = os.path.join(dir_name, 'websites')
    json_filepath = os.path.join(websites_dir, 'web_dic.json')
    website_dic = defaultdict(list)

    if os.path.exists(json_filepath):
        with open(json_filepath, 'r') as file_reader:
            website_dic = json.load(file_reader)

    return website_dic


if __name__ == "__main__":
    advanced_main()