import re


def parseEal(data):
    result = re.findall(r'\s*EAL\s\d\+|\s*EAL\d\+|\s*EAL\s\d|\s*EAL\d', data)

    return list(dict.fromkeys(result))


def parseSha(data):
    result = re.findall(r'\s*SHA-\d\/[0-9]+|\s*SHA\\_[0-9]+|\s*SHA-[0-9]+|\s*SHA\s[0-9]+|\s*SHA[0-9]+', data)

    return list(dict.fromkeys(result))


def parseRsa(data):
    result = re.findall(
        r"\s*RSASSA-PSS|\s*RSASignaturePKCS1|\s*RSA-CRT|\s*RSA2048\/4096|\s*RSA-[0-9]+|\s*RSA [0-9]+|\s*RSA\s["
        r"0-9]+|\s*RSA[0-9]+", data)

    return list(dict.fromkeys(result))


def parseDes(data):
    result = re.findall(r'3DES|DES3|TDES|Triple-DES|Triple\sDES|triple-DES|TripleDES|single-des', data)

    return list(dict.fromkeys(result))


def parseEcc(data):
    result = re.findall(r'\s*ECC\s[0-9]+|\s*ECC[0-9]+', data)  # nefunguje ECC 224!! Odstranene ECC

    return list(dict.fromkeys(result))


def parseJavaCard(data):
    result = re.findall(r'\s*Java\sCard\s\d\.\d\.\d|\s*Java\sCard\s\d\s', data)

    return list(dict.fromkeys(result))


def parseGlobalPlatform(data):
    result = re.findall(r'\s*GlobalPlatform\s\d\.\d\.\d|\s*GlobalPlatform\s\d\.\d', data)
    return list(dict.fromkeys(result))


def removeDuplicities(tmp):
    tmp = [item.strip(' ') for item in tmp]

    tmp = list(dict.fromkeys(tmp))
    return tmp


def parse(file):
    data = {}
    ealList = []
    shaList = []
    rsaList = []
    desList = []
    eccList = []
    javaCardList = []
    globalPlatformList = []

    with open(file, encoding="utf8") as fp:
        for i, line in enumerate(fp):
            result = parseEal(line)
            if result:
                for k in result:
                    ealList.append(k)
            result = parseSha(line)

            if result:
                for k in result:
                    shaList.append(k)
            result = parseRsa(line)

            if result:
                for k in result:
                    rsaList.append(k)
            result = parseDes(line)

            if result:
                for k in result:
                    desList.append(k)
            result = parseEcc(line)

            if result:
                for k in result:
                    eccList.append(k)
            result = parseJavaCard(line)

            if result:
                for k in result:
                    javaCardList.append(k)
            result = parseGlobalPlatform(line)

            if result:
                for k in result:
                    globalPlatformList.append(k)

    ealList = removeDuplicities(ealList)
    if len(ealList) != 0:
        data["eal"] = ealList
    shaList = removeDuplicities(shaList)
    if len(shaList) != 0:
        data["sha"] = shaList
    rsaList = removeDuplicities(rsaList)
    if len(rsaList) != 0:
        data["rsa"] = rsaList
    desList = removeDuplicities(desList)
    if len(desList) != 0:
        data["des"] = desList
    eccList = removeDuplicities(eccList)
    if len(eccList) != 0:
        data["ecc"] = eccList
    javaCardList = removeDuplicities(javaCardList)
    if len(javaCardList) != 0:
        data["java_card"] = javaCardList
    globalPlatformList = removeDuplicities(globalPlatformList)
    if len(globalPlatformList) != 0:
        data["global_platform"] = globalPlatformList
    return data
