import re


def parse(file):
    data = []
    index = 0
    with open(file, encoding="utf8") as fp:
        for i, line in enumerate(fp):
            if re.search("Revision History\n", line) is not None or \
                    re.search("Revision history\n", line) is not None or \
                    re.search("REVISION HISTORY\n", line) is not None or \
                    re.search("Rev.+Date.+Description\n", line) is not None or \
                    re.search("Version Control\n", line) is not None:
                index = i + 1
                break

        empty_lines = 0
        s_line = ""
        first_occ = False

        for i, line in enumerate(fp, start=index):
            # skip new lines
            tmp = re.search("^$", line)
            if tmp is not None:
                if empty_lines == 1 and first_occ:
                    break
                empty_lines += 1
                continue

            empty_lines = 0

            # find first part of record = version
            tmp = re.search("\d\.\d+", line)
            if tmp is not None:
                first_occ = True
                # save previous record
                if s_line:
                    data.append(parseItem(s_line))
                s_line = ""

            # if we are already in the revisions section, fill the string
            # for later saving
            if first_occ:
                s_line += line

        # save the last record
        if s_line:
            data.append(parseItem(s_line))

    removeUnwantedItems(data)
    return data


# get info from the line
# parse version, date and description
def parseItem(line):
    item = {}

    version = re.search("\d+\.\d+", line)

    if version:
        version = version.group()
        line = line.replace(version, '', 1)
    else:
        version = ""

    # there are 3 different types of date
    # 01-01-1970
    date_un = re.search("\d+\-\w+\-\d+\D{1}", line)
    # 01.01.1970
    date_dot = re.search("\d{2}\.\w+\.\d+\D{1}", line)
    # 01 01 1970
    date_space = re.search("\d{2}\s\w+\s\d+\D{1}", line)

    if date_un:
        date = date_un.group()
        line = line.replace(date, '')
        date = date[:-1]
        date = transferDate(date, "-")
    elif date_dot:
        date = date_dot.group()
        line = line.replace(date, '')
        date = date[:-1]
        date = transferDate(date, ".")
    elif date_space:
        date = date_space.group()
        line = line.replace(date, '')
        date = date[:-1]
        date = transferDate(date, " ")
    else:
        date = ""

    arr = line.split()
    # remove unwanted text in description
    if arr[0] == "v" or arr[0] == "Rev." or arr[0] == "Version":
        arr.remove(arr[0])
    description = " ".join(arr)

    item["version"] = version
    item["date"] = date
    item["description"] = description

    return item


# the date has different format in json
# so it has to be changed
def transferDate(date, delim):
    tmp = date.split(delim)
    # swap years and days
    if len(tmp[0]) < len(tmp[2]):
        x = tmp[2]
        tmp[2] = tmp[0]
        tmp[0] = x
    # if the year is written as string, then convert it to number
    if len(tmp[1]) > 2:
        switcher = {
            "January": "01",
            "February": "02",
            "March": "03",
            "April": "04",
            "May": "05",
            "June": "06",
            "July": "07",
            "August": "08",
            "September": "09",
            "October": "10",
            "November": "11",
            "December": "12"
        }
        tmp[1] = switcher.get(tmp[1])
    return "-".join(tmp)

# data might contain unwanted items at the end, e.g. duplicities
# here are data filtered and the un. items removed
def removeUnwantedItems(data):
    prev = ""
    for item in data:
        if item["version"] == prev:
            data.remove(item)
            break
        prev = item["version"]
