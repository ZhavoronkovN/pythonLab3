# 2020, all rights reserved

from collections import namedtuple as tuple

#global variables
routes = dict()
stations = list()

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

def is_before(found_list, start_station, end_station):
    start = found_list.index(start_station)
    end = found_list.index(end_station)
    return start < end

def get_route_from_list(found_list,start_station,end_station):
    start = found_list.index(start_station)
    end = found_list.index(end_station)
    return found_list[start:end+1]

def howto_get_to_n(start_station,end_station):
    found_list = list()
    # with no redirections
    for k in routes:
        if start_station in routes[k][0] and end_station in routes[k][0] and is_before(routes[k][0], start_station, end_station):
            found_list = routes[k][0]
            print("no redirections by " + k)
            return get_route_from_list(found_list, start_station, end_station)
        elif start_station in routes[k][1] and end_station in routes[k][1] and is_before(routes[k][1], start_station, end_station): # in backward
            found_list = routes[k][1]
            print("no redirections by " + k)
            return get_route_from_list(found_list, start_station, end_station)
            
    for t1 in routes:
        print("#" + t1)
        known_station = object()
        unknown_station = object()
        state = True
        if start_station in routes[t1][0] and state:
            known_station = start_station
            unknown_station = end_station
            found_list = routes[t1][0]
            state = False
        elif start_station in routes[t1][1] and state:
            known_station = start_station
            unknown_station = end_station
            found_list = routes[t1][1]
            state = False
        elif end_station in routes[t1][0] and state:
            known_station = end_station
            unknown_station = start_station
            found_list = routes[t1][0]
            state = False
        elif end_station in routes[t1][1] and state:
            known_station = end_station
            unknown_station = start_station
            found_list = routes[t1][1]
            state = False
        for t2 in routes.keys():
            if t1 == t2:
                continue
            if unknown_station in routes[t2][0]:
                common_stations = list(set(found_list).intersection(set(routes[t2][0])))
                if len(common_stations) != 0:
                    common_station = common_stations[0]
                    print("#" + t2)
                    return get_route_from_list(found_list, start_station, common_station) + get_route_from_list(routes[t2][0], common_station, unknown_station)
            elif unknown_station in routes[t2][1]:
                common_stations = list(set(found_list).intersection(routes[t2][1]))
                if len(common_stations) != 0:
                    common_station = common_stations[len(common_stations)-1]
                    print("#" + t2)
                    return get_route_from_list(found_list, known_station, common_station) + get_route_from_list(routes[t2][1], common_station, unknown_station) 
    return list()

            
def write_to_file_dialog(content):
    ''' @param content : list of strings
        introduce console dialog for writrinf to file
        @return void '''

    print("Do u want to save this output to file ?")
    ans = input("[YES or NO] : ")
    if ans.lower() == "yes" or ans.lower() in "yes":
        print("Enter a filename to save data : [with no extension]")
        filename = input(">>> ")
        write_to_file(filename, content)

def write_to_file(filename, content):
    ''' @param filename : name of file to write [with no extenstion]
        @param context : data to be written 
        Create new or rewrite if exists file with content in .txt format
        @return void '''

    with open(filename + ".txt", encoding='utf-8', mode='w') as f:
        for i in content:
            f.write(i)
            f.write("\n")
        f.close()


continue_execution = True

while continue_execution:
    print('# 1 : Exit')
    try:
        state = int(input("Maka a choice pls >>> "))
    except ValueError:
        print("Choose from a list!")
        continue
    if state == 1:
        print("Thanks for usage! Really appreciate that!")
        continue_execution = False
    if state == 2:
        print("All stops file")
        filename = input(">>> ")
        read_all_stations(filename)
        for i in stations:
            print(i)
    if state == 3:
        print("All routes file")
        filename = input(">>> ")
        read_routes("all_trams.txt")
        print(routes)
    if state == 4:
        print("1")
        print(howto_get_to_n("станція Підзамче", "вул. Русових"))