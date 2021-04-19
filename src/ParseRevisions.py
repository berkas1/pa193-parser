import re

def parse(file):
    data = []
    index = 0
    with open(file, encoding="utf8") as fp:
        for i, line in enumerate(fp):
            if i == 540:
                print()
                # re.search("Rev.+Date.+Description\n", line) is not None or \
            if re.search("Revision History\n", line) is not None or \
                    re.search("Revision history\n", line) is not None or \
                    re.search("REVISION HISTORY\n", line) is not None or \
                    re.search("Rev.+Date.+Description\n", line) is not None or \
                    re.search("Version Control\n", line) is not None:
                index = i+1
                break


        empty_lines = 0
        str = ""
        firstOcc = False

        for i, line in enumerate(fp, start=index):
            # skip new lines
            tmp = re.search("^$", line)
            if tmp is not None:
                if empty_lines == 1 and firstOcc:
                    break
                empty_lines += 1
                continue

            empty_lines = 0

            tmp = re.search("\d\.\d+", line)
            if tmp is not None:
                firstOcc = True
                if str:
                    data.append(parseItem(str))
                str = ""
            if firstOcc:
                str += line

        # last one
        if str:
            data.append(parseItem(str))

    removeUnwantedItems(data)
    return data

def parseItem(line):
    item = {}

    version = re.search("\d+\.\d+", line)

    if version:
        version = version.group()
        line = line.replace(version, '', 1)
    else:
        version = ""

    date_un = re.search("\d+\-\w+\-\d+\D{1}", line)
    date_dot = re.search("\d{2}\.\w+\.\d+\D{1}", line)
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
    if arr[0] == "v" or arr[0] == "Rev." or arr[0] == "Version":
        arr.remove(arr[0])
    description = " ".join(arr)

    item["version"] = version
    item["date"] = date
    item["description"] = description

    return item

def transferDate(date, delim):
    tmp = date.split(delim)
    # swap years and days
    if len(tmp[0]) < len(tmp[2]):
        x = tmp[2]
        tmp[2] = tmp[0]
        tmp[0] = x
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

def removeUnwantedItems(data):
    prev = ""
    for item in data:
        if item["version"] == prev:
            data.remove(item)
            break
        prev = item["version"]