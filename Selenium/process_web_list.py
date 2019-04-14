#!/usr/bin/python3

from sys import exit

import util


def main():

    if not util.is_there_csvfile():
        print("A CSV of Alexa list does not exist!")
        if not util.fetch_alexa_list():
            print("It could not fetch the file!")
            exit(1)

    website_dict = util.read_csv_file(10)
    print(website_dict['de'])
    util.write_dict_to_json(website_dict)
    util.dict_to_bookmark(website_dict)


if __name__ == "__main__":
    main()