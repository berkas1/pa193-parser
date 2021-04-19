import re


def replaceLinesAndStrip(data):
    data = data.replace('\n', "")
    data = ' '.join(data.split())

    return data

def parseUntilFor(string, index):
    data = string[:index]
    data = replaceLinesAndStrip(data)

    return data

def parseUntilReference(string, index):
    data = string[:index]
    data = replaceLinesAndStrip(data)

    return data

def parseUntilReportNumber(string, index):
    data = string[:index]
    data = replaceLinesAndStrip(data)

    return data

def parseSTLuntilCC(string, index):
    data = string[index:].split('\n', 1)[1]
    data = data.strip()

    tmp_index = data.find("Common Criteria")
    data = data[:tmp_index].strip()

    return data

def parseDocumentInformation(string, index):
    data = string[index:]
    data = data.split('\n', 2)[2]

    data = data.strip()
    data = data[:data.find("\n\n")]

    data = replaceLinesAndStrip(data)

    return data

def parse(file):

    data = ""

    orig_string = ""
    tmp_i = 0
    with open(file, encoding="utf8") as fp:
        for i, line in enumerate(fp):
            orig_string += line
            if i > 50:
                break

        # if "Document Information" almost at the beginning
        index = orig_string.find("Document Information")
        if (index < 600 and index > 0):
            data = parseDocumentInformation(orig_string, index)

        # between "Security Target Lite" and Common "Criteria"
        stringWithoutForIndex = orig_string.find("Security Target Lite")

        if (stringWithoutForIndex < 100 and stringWithoutForIndex > 0):
            data = parseSTLuntilCC(orig_string, stringWithoutForIndex)

        # If "for" in the begining
        index = orig_string.find("for")
        if (index < 100 and index > 10):
            data = parseUntilFor(orig_string, index)

        # report number
        index = orig_string.find("Report number:")
        if (index < 500 and index > 10):
            data = parseUntilSecurityTarget(orig_string, index)

    return {"certid": data}