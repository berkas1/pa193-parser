import re 
#nefunguje, ked pred a po hladanom slove nie je text
#problematicke hodnoty s + alebo medzerou

def parseEal(data):
	result = re.findall(r' EAL4 |EAL4| EAL5 |EAL5| EAL6 |EAL6| EAL\s1 |EAL\s1| EAL\s2 |EAL\s2| EAL\s4 |EAL\s4| EAL\s5 |EAL\s5| EAL\s6 |EAL\s6| EAL2\+ |EAL2\+| EAL4\+ |EAL4\+| EAL5\+ |EAL5\+| EAL6\+ |EAL6\+| EAL\s2\+ |EAL\s2\+| EAL\s4\+ |EAL\s4\+| EAL\s5\+ |EAL\s5\+|EAL\s6\+| EAL\s6\+ ', data)

	return list(dict.fromkeys(result))

def parseSha(data):
	result = re.findall(r'SHA1|SHA2|SHA224|SHA256|SHA384|SHA512|SHA\s256|SHA\s512|SHA-1|SHA-2|SHA-3| SHA-224 |SHA-224| SHA-256 | SHA-384 | SHA-512 |SHA\_224|SHA\_256|SHA\_384|SHA\_512|SHA-3/224|SHA-3/256|SHA-3/384|SHA-3/512', data)
	
	return list(dict.fromkeys(result))

def parseRsa(data):
	result = re.findall(r'RSA\s1024|RSA2048|RSA4096|RSA\s2048|REA\s2048|RSA\s4096|RSA2048/4096|RSA-2048|RSA-CRT|RSASignaturePKCS1|RSASSA-PSS', data)

	return list(dict.fromkeys(result))

def parseDes(data):
	result = re.findall(r'3DES|DES3|TDES|Triple-DES|Triple\sDES|triple-DES|TripleDES|single-des', data)

	return list(dict.fromkeys(result))

def parseEcc(data):
	result = re.findall(r'ECC\s224', data) #nefunguje ECC 224!! Odstranene ECC

	return list(dict.fromkeys(result))

def parseJavaCard(data):
	result = re.findall(r'Java\sCard\s3|Java\sCard\s3.0.5|Java\sCard\s3.0.4', data)

	return list(dict.fromkeys(result)) 

def parseGlobalPlatform(data):
	result = re.findall(r'GlobalPlatform\s2.3|GlobalPlatform\s2.2.1"', data) #nefunguje GlobalPlatform 2.2.1!

	return list(dict.fromkeys(result))

def removeDuplicities(tmp):
	# remove spaces
	tmp = [item.strip(' ') for item in tmp]
	# remove duplcicates
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

	contents_firstLine = 0
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
	if len(rsaList):
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

