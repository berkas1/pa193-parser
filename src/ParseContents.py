import re


def helperRemoveTrailingChars(s):
    if len(s) < 1:
        return ""

    if s[0] == ".":
        s = s[1:]

    if len(s) > 1 and s[-1] == ".":
        s = s[:-2]
    s = s.strip()

    return s


def contentsGetHeadlinePageNumber(line, previous):
    headline = ""
    page_number = 0
    # print(line[(previous.span()[1] + 1):].strip())
    start_position = (previous.span()[1])

    newline = line[start_position:].strip()
    tmp2 = re.search("^((.*?)\.\.)|((.*?)\ \ )", newline)
    if tmp2 is not None:
        headline = tmp2.group().strip()

        headline = helperRemoveTrailingChars(headline)

        # get page number

        tmp_page = re.search("[1-9][0-9]*", (line[tmp2.span()[1] + start_position + 10:]).strip())

        if tmp_page is not None:

            page_number = tmp_page.group()
        else:
            page_number = -1
    return headline, page_number


def parse(file):
    data = []

    contents_firstLine = 0
    with open(file, encoding="utf8", errors="ignore") as fp:
        # find line with "content" word and jump to next line
        for i, line in enumerate(fp):
            if (str(line).lower()).find("content") != -1:
                contents_firstLine = i + 1
                break
        # find line without section number
        empty_lines = 0
        previous_line_empty = False
        for i, line in enumerate(fp, start=contents_firstLine):
            if empty_lines >= 5 or i > contents_firstLine + 1500:
                break

            line = line.strip()
            res = re.search("^((\d*\ )|(\d+\.)|([A-Z]\ )|([A-Z]\.))", line)

            # skip new lines
            tmp = re.search("^$", line)
            if tmp is not None:
                if previous_line_empty is True or empty_lines == 0:
                    empty_lines += 1
                previous_line_empty = True
                continue

            previous_line_empty = False
            # parse line without a section number
            if res is None:
                headline = ""
                page_number = 0

                # get the headline
                tmp = re.search("^((.*?)\.\.)|((.*?)\ \ )", line)
                if tmp is not None:
                    headline = tmp.group()
                    headline = helperRemoveTrailingChars(headline)

                    # get page number
                    tmp_page = re.search("[1-9][0-9]*", line[tmp.span()[1]:])

                    if tmp_page is not None:
                        page_number = tmp_page.group()
                        # print(line)
                    else:
                        page_number = -1
                result = ["", headline, int(page_number)]

                data.append(result)

            else:
                # now pages with section number
                section = ""
                tmp = re.search("^(((\d+\.)*\d+)|[A-Z](\ |\.))", line)
                if tmp is not None:
                    section = str(tmp.group())
                # get the headlineq
                headline, page_number = contentsGetHeadlinePageNumber(line, tmp)

                result = [str(section), str(headline), int(page_number)]

                data.append(result)

    # now remove all false entries
    if len(data) < 1:
        return []

    last_page_number = int(data[0][2])
    to_remove = []
    for e in data:
        if int(e[2]) < last_page_number or int(e[2]) > 10 * last_page_number:
            to_remove.append(e)
        else:
            last_page_number = int(e[2])
    # print(data)
    for e in to_remove:
        data.remove(e)

    return data
