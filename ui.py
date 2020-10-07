input_helper = dict()
q_a = dict()
constants = {"$tram_id":['0','1'],'$station_id':['aaaba','b','c']}
variables = list()
def add_to_dict(dictionary,value,key):
	space = value.find(' ')
	firstWord = value[:space+1]
	if space == -1:
		dictionary[value] = key
	elif firstWord in dictionary.keys():
		add_to_dict(dictionary[firstWord],value[space+1:],key)
	else:
		dictionary[firstWord] = dict()
		add_to_dict(dictionary[firstWord],value[space+1:],key)

with open('question-answer.txt','r',encoding = 'UTF-8') as questions:
	for line in questions.readlines():
		qa = line.split('->')
		question = qa[0].strip();
		answers = qa[1].split('&')
		answers = {"+" : answers[0],"-" : answers[1]}
		add_to_dict(input_helper,question,answers)

def remove_solo(key,dictionary):
	if '+' in dictionary.keys() and '-' in dictionary.keys():
		return (key,dictionary);
	res = dict()
	if len(dictionary.keys()) == 1:
		if list(dictionary.keys())[0].startswith('$'):
			(tk,dc) = remove_solo('',list(dictionary.values())[0])
			return  (key,{list(dictionary.keys())[0]:{tk:dc}})
		return remove_solo(key.strip() + " " + list(dictionary.keys())[0],list(dictionary.values())[0])
	else:
		for k in dictionary.keys():
			(tk,dc) = remove_solo(k,dictionary[k])
			res[tk] = dc
		return (key,res)

def print_dict(dictionary,cnt):
	for k in dictionary.keys():
		print('    '*cnt + k)
		if type(dictionary[k]) == dict:
			print_dict(dictionary[k],cnt+1)
		else:
			print('    '*cnt + dictionary[k])

res = remove_solo('',input_helper)[1]
#print_dict(res,0)

def myIn(string,findIn):
	smaller = string if len(string) < len(findIn) else findIn
	bigger = string if smaller == findIn else findIn
	if smaller in bigger:
		return True
	count = 0
	for i in range(len(smaller)):
		if smaller[i] == bigger[i]:
			count += 1
	return (count/(float)(len(smaller)))>=0.5

def myInSet(string, arr):
	if string in arr:
		return (True,string)
	for el in arr:
		if myIn(string,el):
			return (True,el)
	return (False,'')

def navigate_user(dictionary,string,prev):
	found = False
	if list(dictionary.keys())[0].startswith('$'):
		key = list(dictionary.keys())[0].strip()
		if string.strip() == '':
			if '?' in key:
				print(prev + key.replace('$',''))
			else:
				print(prev + key.replace('$','') + ' ...')
			print('Можливі значення '+key.replace('$','').replace('?','') + ':')
			print('\t'.join(constants[key.replace('?','')]))
			return (False,{})
		global variables
		toFind = string.replace('?','')
		if string.find(' ')!=-1:
			toFind = string[:string.find(' ')]
		(inSet, properName) = myInSet(toFind,constants[key.replace('?','')])
		if inSet:
			variables.append(properName)
			if '?' in key:
				return (True,list(dictionary.values())[0])
			if string.find(' ') == -1 or string.find(' ') == len(string):
				return navigate_user(list(dictionary.values())[0],'',prev + properName)
			else:
				return navigate_user(list(dictionary.values())[0],string[string.find(' ')+1:],prev + properName+' ')
		else:
			print('Не вдалося знайти {} {}'.format(key.replace('$','').replace('?',''),toFind))
			print('Можливі значення '+key.replace('$','').replace('?','') + ':')
			print('\t'.join(constants[key.replace('?','')]))
			return (False,{})

	if string != '':
		for k in dictionary.keys():
			if myIn(k.strip(),string.strip()):
				found = True
				if k.endswith('?'):
					return (True,dictionary[k])
				else:
					return navigate_user(dictionary[k],string[len(k):],prev + k)

	if not found:
		for word in string.split(' '):
			found_two = False
			for k in dictionary.keys():
				if word in k:
					found_two = True
			if not found_two:
				print("Unknown word : " + word)
		for k in dictionary.keys():
			if k.endswith('?'):
				print(prev + k)
			else:
				print(prev + k + '...')
	return (False,{})

print(navigate_user(res,'Скільки зупинок між','')[0])