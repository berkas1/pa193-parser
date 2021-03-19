import argparse
import json
import sys
import re

import src.ParseContents as p_contents

config = {'all': False, 'parse_title': False, 'biblio': False, 'versions': False, 'contents': False}

outputData = {}
input_file = ""

parser = argparse.ArgumentParser(description='Parse Common Criteria certificates. Input has to be plain txt file. '
                                             'You can define what part to parse using arguments. Use --all to parse'
                                             ' entire file.')
parser.add_argument('string', metavar='FILE.TXT', type=str,
                    help='file to parse')
parser.add_argument('--verbose', action='store_true',
                    help='sum the integers (default: find the max)')

parser.add_argument('--all', action='store_true',
                    help='Parse the entire file')
parser.add_argument('--title', action='store_true',
                    help='Parse the title')
parser.add_argument('--bibliography', action='store_true',
                    help='Parse the bibliography')
parser.add_argument('--contents', action='store_true',
                    help='Parse the table of contents')
parser.add_argument('--versions', action='store_true',
                    help='Parse versions')

args = parser.parse_args()




def main():
    config["all"] = args.all
    config["title"] = args.title
    config["versions"] = args.versions
    config["biblio"] = args.bibliography
    config["contents"] = args.contents

    # if no arguments are supplied, consider --all as True
    if len(sys.argv) == 2:
        args.all = True

    # set everything to True if parameter --all is used (entire file will be parsed)
    if (args.all):
        for key in config.keys():
            config[key] = True

    if config["title"]:
        parse_title()

    if config["versions"]:
        parse_versions()

    if config["biblio"]:
        parse_biblio()

    if config["contents"]:
        parse_contents()

    print(json.dumps(outputData))


def parse_title():
    title = ""

    outputData["title"] = title


def parse_versions():
    data = []

    outputData["versions"] = data


def parse_biblio():
    data = []

    outputData["bibliography"] = data

def parse_contents():
    data = []

    outputData["table_of_content"] = p_contents.parse(args.string)



if __name__ == "__main__":
    main()


