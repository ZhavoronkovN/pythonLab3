# 2020, all rights reserved

#global variables
routes = dict()
stations = list()
questions = dict()
constants = dict()
variables = list()

def read_routes(filename):
    ''' key : tram_id
        Value : [forth_direction list, back direction list] '''
    with open(filename, encoding='utf-8', mode='r') as f:
        content = [i.split("#") for i in f.read().split("$")]
        for i in content:
            global routes
            routes[i[0].strip()] = [i[1].strip().splitlines(), i[2].strip().splitlines()]

def read_all_stations(filename):
    with open(filename, encoding='utf-8', mode='r') as f:
        global stations
        stations = f.read().splitlines()

def read_questions(filename):
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

    temp = dict()
    with open(filename,'r',encoding = 'UTF-8') as questionsFile:
        for line in questionsFile.readlines():
            qa = line.split('->')
            question = qa[0].strip();
            answers = qa[1].split('&')
            answers = {"+" : answers[0],"-" : answers[1], 'func' : howto_get_to_n}
            add_to_dict(temp,question,answers)
    global questions
    questions = remove_solo('',temp)[1]

def do_all_preparations():
    read_routes("all_trams.txt")
    read_all_stations("all_stops.txt")
    read_questions("question-answer.txt")
    constants['$tram_id'] = routes.keys()
    constants['$station_id'] = stations



#1 query
def count_of_stations_for_tram(tram_id):
    res = set(routes[tram_id][0] + routes[tram_id][1])
    return len(res)

#7 query
def get_trams_for_station(station):
    res = list()
    for i in routes:
        if station in routes[i][1] + routes[i][2]:
            res.append(i)
    return res

#2 query
def count_of_all_routes():
    res = len(routes)
    return res

def get_diff_in_stations(start_station, end_station):
    return list()

def print_route(tram_id):
    return str()

def get_stations_for_tram(tram_id):
    res = routes[tram_id][0] + routes[tram_id][1]
    return res

def get_to_university(station_):
    return list()

def is_possible_to_get(station_id, tram_id):
    return False

def get_route_from_list(direction,start_station,end_station):
    start = listLower(direction).index(start_station.lower())
    end = listLower(direction).index(end_station.lower())
    reverse = False
    if start > end:
        temp = start
        start = end
        end = temp
        reverse = True
    res = direction[start:end+1]
    if reverse:
        res.reverse()
    return res

def listLower(lst):
    return [x.lower() for x in lst]

def howto_get_to_n(start_station,end_station):
    # with no redirections
    for k in routes:
        for direction in routes[k]:
            if start_station.lower() in listLower(direction) and end_station.lower() in listLower(direction):
                return (k,get_route_from_list(direction, start_station, end_station))
    # with one redirection 
    for t1 in routes:
        direction1 = list()
        known_station = object()
        unknown_station = object()

        for direction in routes[t1]:
            if start_station.lower() in listLower(direction):
                known_station = start_station.lower()
                unknown_station = end_station.lower()
                direction1 = direction
                break
            elif end_station.lower() in listLower(direction):
                known_station = end_station.lower()
                unknown_station = start_station.lower()
                direction1 = direction
                break

        if len(direction1) == 0:
            continue

        for t2 in routes:
            if t1 == t2:
                continue
            for direction2 in routes[t2]:
                if unknown_station in listLower(direction2):
                    common_stations = list(set(direction1) & set(direction2))
                    if len(common_stations) != 0:
                        common_station = common_stations[0]
                        return [(t1,get_route_from_list(direction1, known_station, common_station)), (t2,get_route_from_list(direction2, common_station, unknown_station))]
    # more than one redirection
    return list()

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
        if string.strip().startswith('"'):
            toFind = string[string.find('"'):]
            toFind = toFind[:toFind[1:].find('"')+2]
        else:
            toFind = string.strip().split(' ')[0]
        if toFind.lower().strip().replace('"','') in [x.lower().strip() for x in constants[key.replace('?','')]]:
            variables.append(toFind.lower().replace('"',''))
            if '?' in key:
                return (True,list(dictionary.values())[0])
            return navigate_user(list(dictionary.values())[0],string[string.find(toFind)+len(toFind):],prev + toFind.strip())
        else:
            print('Не вдалося знайти {} {}'.format(key.replace('$','').replace('?',''),toFind))
            print('Можливі значення '+key.replace('$','').replace('?','') + ':')
            print('\t'.join(constants[key.replace('?','')]))
            return (False,{})

    if string != '':
        for k in dictionary.keys():
            if k.lower().startswith(string.lower()) or string.lower().startswith(k.lower()):
                found = True
                if k.endswith('?'):
                    return (True,dictionary[k])
                else:
                    return navigate_user(dictionary[k],string[len(k):],prev + k)

    if not found:
        for word in string.split(' '):
            found_two = False
            for k in dictionary.keys():
                if word.lower() in k.lower():
                    found_two = True
            if not found_two:
                print("Unknown word : " + word)
        for k in dictionary.keys():
            if k.endswith('?'):
                print(prev + k)
            else:
                print(prev + k + '...')
    return (False,{})

do_all_preparations()
print('Введіть питання, початок питання чи просто натисніть "Enter" : ')
while(True):
    variables = list()
    (questionFull,handler) = navigate_user(questions,input(),'')
    if questionFull:
        handler = handler['']
        print(variables)
        print(handler['func'](*variables))