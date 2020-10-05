# 2020, all rights reserved

#global variables
routes = dict()
stations = list()

def read_routes(filename):
    ''' key : tram_id
        Value : [forth_direction list, back direction list] '''

    return routes

def read_all_stations(filename):
    return stations


continue_execution = True

while continue_execution:
    print('# 1 : Exit')
    try:
        state = int(input("Maka a choice pls >>> "))
    except ValueError:
        print("Choose from a list!")
    if state == 1:
        print("Thanks for usage! Really appreciate that!")
        continue_execution = False