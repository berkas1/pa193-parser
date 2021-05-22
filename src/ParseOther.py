import re


def replaceLinesAndStrip(data):
    data = data.replace('\n', "")
    data = ' '.join(data.split())

    return data

def parseUntilFor(string, index):
    data = string[:index]
    data = replaceLinesAndStrip(data)

    return data

def parseUntilReportNumber(string, index):
    data = string[index:]
    data = replaceLinesAndStrip(data)
    #print (data)
    tmp_index = data.find("Report number")
    data = data[tmp_index:].strip()
    
    return (data.split()[2])

def parseSTLuntilCC(string, index):
    data = string.split('\n', 1)[1].strip()
    data = data[:data.find("Common Criteria")]
    data = replaceLinesAndStrip(data)

    return data

def parseDocumentInformation(string, index):
    data = string[:index]
    data = replaceLinesAndStrip(data)
    index = data.find("BSI")
    data = data[index:]
    print ()
    print (index)

    return data

def parse(file):

    data = ""

    orig_string = ""
    tmp_i = 0
    with open(file, encoding="utf8", errors="ignore") as fp:
        for i, line in enumerate(fp):
            orig_string += line
            if i > 100:
                break

        # between "Security Target Lite" and Common "Criteria"
        stringWithoutForIndex = orig_string.find("Security Target Lite")

        if (stringWithoutForIndex < 1000 and stringWithoutForIndex > 0):
            data = parseSTLuntilCC(orig_string[stringWithoutForIndex+20:], stringWithoutForIndex)
            return {"certid": data}
        # If "for" in the begining
        index = orig_string.find("for")
        if (index < 100 and index > 10):
            data = parseUntilFor(orig_string, index)
            return {"certid": data}
        # report number
        index = orig_string.find("Report number:")
        if (index < 2000 and index > 10):
            data = parseUntilReportNumber(orig_string, index)
            return {"certid": data}
        # if "Document Information" almost at the beginning
        index = orig_string.find("Document Information")
        if (index < 600 and index > 0):
            data = parseDocumentInformation(orig_string, index)
            return {"certid": data}

    return {}
