import re

def parse(file):
    data = []
    storage = []
    index = 0
    with open(file, encoding="utf8") as fp:
        for i, line in enumerate(fp):
            if i == 540:
                print()
            if re.search("Revision History\n", line) is not None or \
                    re.search("Revision history\n", line) is not None or \
                    re.search("REVISION HISTORY\n", line) is not None or \
                    re.search("  Description\n", line) is not None or \
                    re.search("Version Control\n", line) is not None:
                index = i+1
                break


        empty_lines = 0
        tmp_string = ""

        for i, line in enumerate(fp, start=index):
            # skip new lines
            tmp = re.search("^$", line)
            if tmp is not None:
                if empty_lines == 1:
                    break
                empty_lines += 1
                continue

            empty_lines = 0

            tmp = re.search("\d\.\d+", line)
            if tmp is not None:
                data.append(parseItem(line))


    return data

def parseItem(line):
    item = {}

    version = re.search("\d\.\d+", line)

    if version:
        version = version.group()
        line = line.replace(version, '', 1)
    else:
        version = ""

    date = re.search("\d+\-\w+\-\d+", line)
    if date:
        date = date.group()
        line = line.replace(date, '')
        date = transferDate(date)
    else:
        date = ""

    description = " ".join(line.split())

    item["version"] = version
    item["date"] = date
    item["description"] = description

    return item

def transferDate(date):
    tmp = date.split("-")
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