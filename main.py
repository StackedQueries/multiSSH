import multiSSH as q
import helpers
import getpass
import sys, glob


try:
    print("-1) Exit\n1) Import Angry IP txt file (sorted by IP)\n2) Enter range manually\nPlease Enter A number")
    choice = int(input(">"))
    if choice == 1:
        dict={}
        for c, p in enumerate(glob.glob('locations\\*.txt')):
            dict[str(c)]=p
            print(c,p)
        ipArr=helpers.getAngry(dict.get(input("Choose Path: ")))
    elif choice == 2:
        ip3 = input("Enter the first 3 octets (###.###.###): ")
        start = int(input("Start of range: "))
        end = int(input("End of range: "))
        ipArr = helpers.createArr(ip3, start, end, 1)
    elif choice == -1:
        raise KeyboardInterrupt
    else:
        raise Exception
    user = input("Username: ")
    pswd = getpass.getpass("Password: ")
    if input("Choose script(s)? (Default is script.txt) (Y/N) \n>").lower() == "y":
        ccs = []
        for c, p in enumerate(glob.glob('scripts\\*.txt')):
            ccs.append(p)
            print(c,p)
        choice = input("Which script(s)? (to choose multiple, type number seperated by space or -1 for all scripts.)\n>")
        if choice == "-1":
            for script in ccs:
                print(script)
                startup = q.ssh(helpers.createlMap(ipArr, [user], [pswd]), path=script)
                startup.startQueue()
        else:
            for script in choice.split(" "):
                startup = q.ssh(helpers.createlMap(ipArr, [user], [pswd]), path=str(glob.glob('scripts\\*.txt')[int(script)]))
                startup.startQueue()
    else:
        startup = q.ssh(helpers.createlMap(ipArr, [user], [pswd]))
        startup.startQueue()

    while True:
        exit = input("")
        if exit == "-1":
            break
except KeyboardInterrupt:
    pass
except:
    print("ERROR: ", sys.exc_info()[0])

