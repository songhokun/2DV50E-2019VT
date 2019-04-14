
#!/usr/bin/python3

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import util


def main():
    doh_profile = __get_dns_over_https_profile()
    driver = webdriver.Firefox(firefox_profile=doh_profile)

    website_dict = util.read_json_to_dict()
    if not website_dict:
        print("Dictionary could not be loaded! ")
        exit(1)

    for alexawebsite in website_dict['de']:
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


if __name__ == "__main__":
    main()