# 2020, all rights reserved

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

def get_trams_for_station():
    return list()

#2 query
def count_of_all_routes():
    res = len(routes)
    return res

def get_diff_in_stations(start_station, end_station):
    return list()

def print_route(tram_id):
    return str()

def get_to_university():
    return list()

def is_possible_to_get(station_id, tram_id):
    return False

def howto_get_to(start_station, end_station):
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
        read_routes(filename)
        print(routes)
        