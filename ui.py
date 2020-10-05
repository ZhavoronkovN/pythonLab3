input_helper = dict()
q_a = dict()
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

def navigate_user(dictionary,string,prev):
	found = False
	if string != '':
		for k in dictionary.keys():
			if string.startswith(k.strip()) or string in k:
				found = True
				if k.endswith('?'):
					print(prev + k)
					return (True,dictionary[k])
				else:
					return navigate_user(dictionary[k],string[len(k):],prev + k)

	if not found:
		for k in dictionary.keys():
			if k.endswith('?'):
				print(prev + k)
			else:
				print(prev + k + '...')
	return (False,{})

navigate_user(res,'Ч','')