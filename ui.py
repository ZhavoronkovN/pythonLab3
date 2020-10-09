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