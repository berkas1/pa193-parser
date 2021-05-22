

def replaceLinesAndStrip(data):
    data = data.replace('\n', "")
    data = ' '.join(data.split())

    return data


def parseBetweenForFrom(string, index):
    data = string[index + 4:].strip()
    data = replaceLinesAndStrip(data)

    return data[:data.find("from")].strip()


def parseUntilSecurityTarget(string, index):
    data = string[:index]
    data = replaceLinesAndStrip(data)

    return data


def parseCertificationReport(string, index):
    data = string[index:]
    data = data.split('\n', 2)[2]

    data = data.strip()
    data = data[:data.find("\n\n")]

    data = replaceLinesAndStrip(data)

    return data


def parseSecTargetuntilCC(string):
    # skip until \n
    data = string.split('\n', 1)[1].strip()
    data = data[:data.find("Common")]
    data = replaceLinesAndStrip(data)

    return data


def parseCCuntilDV(string, index):
    data = string[index:].split('\n', 1)[1]
    data = data.strip()

    tmp_index = data.find("Document version")
    data = data[:tmp_index].strip()

    return data


def parseUntilCCDoc(string):
    data = string[:string.find('\n')]

    return data


def parse(file):
    data = ""

    orig_string = ""

    with open(file, encoding="utf8", errors="ignore") as fp:
        for i, line in enumerate(fp):
            orig_string += line
            if i > 30:
                break

        # if "Security Target" on the first line, until common criteria
        index = orig_string.find("Security Target")
        if 10 > index > 0:
            data = parseSecTargetuntilCC(orig_string)

        index = -1
        # if "Certification Report" almost at the beginning
        index = orig_string.find("Certification Report")
        if 600 > index > 0:
            data = parseCertificationReport(orig_string, index)

        # between for & from
        stringWithoutForIndex = orig_string.find("for")

        if 100 > stringWithoutForIndex > 0:
            data = parseBetweenForFrom(orig_string, stringWithoutForIndex)

        # parse from beginning of file until "Security Target Lite"
        index = -1
        index = orig_string.find("Security Target Lite")
        if 500 > index > 10:
            data = parseUntilSecurityTarget(orig_string, index)

        # parse CC until Document version
        index = -1
        index = orig_string.find("Common Criteria")
        if 50 > index > 10:
            data = parseCCuntilDV(orig_string, index)

        # parse first line if "CC Document" in the document
        index = -1
        index = orig_string.find("CC Document")
        if index != -1:
            data = parseUntilCCDoc(orig_string)

    return data
