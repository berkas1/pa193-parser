import re

def parse(file):

    data = {}

    with open(file, encoding="utf8") as fp:

        bibliography_firstLine = 0
        previous_line_empty = False
        for i, line in enumerate(fp):
            # find line with "REFERENCE DOCUMENTS" and the row > 150 to get next occurrence
            if re.search("REFERENCE DOCUMENTS\n", line) is not None and i > 150:
                bibliography_firstLine = i + 2
                break

            # find line with "References" or "Bibliography" or "Literature" leading with new line
            # and with previous line empty and the row > 150 to get next occurrence
            if (re.search("References\n", line) is not None or
               re.search("Bibliography\n", line) is not None or
               re.search("Literature\n", line) is not None) and i > 150 and previous_line_empty:

                bibliography_firstLine = i + 2
                break

            # find empty line
            tmp = re.search("^$", line)
            if tmp is not None:
                previous_line_empty = True
            else:
                previous_line_empty = False

        firstOccurence = True
        section = ""
        content = ""
        empty_lines = 0
        previous_line_empty = False
        for i, line in enumerate(fp, start=bibliography_firstLine):

            # find end of the bibliography or the document
            if empty_lines >= 10 or i > bibliography_firstLine + 300:
                section, content = removeSpaces(section, content)
                data[section] = content
                section = ""
                break

            # skip new lines
            tmp = re.search("^$", line)
            if tmp is not None:
                if previous_line_empty is True or empty_lines == 0:
                    empty_lines += 1
                previous_line_empty = True
                continue

            previous_line_empty = False
            # search for [..] (called section)
            result = re.search("^\s*\[.+]", line)
            # just for the first occurence of []
            if result is None and firstOccurence is True:
                continue

            # add section+content to data if the new [...] is found
            if result is not None and firstOccurence is False:
                section, content = removeSpaces(section, content)
                data[section] = content

            firstOccurence = False

            # if [..] was found, parse it and start filling content
            if result is not None:
                content = ""
                # sekce např. [1]
                section = result.group(0)
                content = line.split(section)[1]
            elif empty_lines > 0:
                continue
            # to avoid adding pages to content
            elif re.search("^\s+\w+", line) is not None and empty_lines == 0:
                content += line
            empty_lines = 0

        # if the cycle finished due to end of document, add the last section+content to data
        if section != "":
            section, content = removeSpaces(section, content)
            data[section] = content

    return data


# method to white spaces before and after and truncate inside
def removeSpaces(section, content):
    section = section.strip()
    content = content.strip()
    content = " ".join(content.split())
    return section, content