import argparse
import json
import sys
import re

import src.ParseContents as p_contents
import src.ParseBibliography as p_bibliography
import src.ParseTitle as p_title
import src.ParseVersions as p_versions

config = {'all': False, 'parse_title': False, 'biblio': False, 'versions': False, 'contents': False, 'revisions': False}
inputFiles = []

outputData = []
input_file = ""

parser = argparse.ArgumentParser(description='Parse Common Criteria certificates. Input has to be plain txt file. '
                                             'You can define what part to parse using arguments. Use --all to parse'
                                             ' entire file.')
parser.add_argument('string', metavar='FILE.TXT', type=str,
                    help='file to parse', nargs='+')
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
parser.add_argument('--revisions', action='store_true',
                    help='Parse revisions')


args = parser.parse_args()


def main():
    config["all"] = args.all
    config["title"] = args.title
    config["versions"] = args.versions
    config["revisions"] = args.revisions
    config["biblio"] = args.bibliography
    config["contents"] = args.contents

    # if no arguments are supplied, consider --all as True
    if (not config["title"] and not config["versions"] and not config["revisions"] and not config["biblio"] and not config[
        "contents"]):
        args.all = True

    # set everything to True if parameter --all is used (entire file will be parsed)
    if (args.all):
        for key in config.keys():
            config[key] = True

    inputFiles = args.string

    for f in inputFiles:
        fileData = {}

        if config["title"]:
            fileData["title"] = parse_title(f)

        if config["versions"]:
            fileData["versions"] = parse_versions(f)

        if config["biblio"]:
            fileData["bibliography"] = parse_biblio(f)

        if config["contents"]:
            fileData["table_of_contents"] = parse_contents(f)

        if config["revisions"]:
            fileData["revisions"] = parse_revisions(f)

        outputData.append(fileData)

    # print(json.dumps(outputData))
    for f in range(0, len(outputData)):
        print(json.dumps(outputData[f]))
        pass


def parse_title(file):
    return p_title.parse(file)


def parse_versions(file):
    return p_versions.parse(file)


def parse_biblio(file):
    return p_bibliography.parse(file)


def parse_contents(file):
    return p_contents.parse(file)


def parse_revisions(file):
    return []


if __name__ == "__main__":
    main()
