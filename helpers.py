import csv

def createArr(ip3, rstart, rstop, rinc=1):
    #Creates list of IPs based on an Range
    ipArr = []
    for i in range(rstart, rstop + 1, rinc):
        ipArr.append("{0}.{1}".format(ip3, i))
    return ipArr

def createlMap(ipArr, uArr, pArr):
    #Location Account Table using ip as the index.
    #uArr as the Username array, pArr as the Password Array
    lMap = {}

    for c, l in enumerate(ipArr):
        lMap[l] = (uArr[c%len(uArr)], pArr[c%len(pArr)])
    return lMap

def joinlMap(lMap1, lMap2):
    #joins location Map
    for item in lMap2:
        lMap1[item] = lMap2.get(item)[0], lMap2.get(item)[1]
    return lMap1

def getCArr(path="scripts\\script.txt"):
    #returns Command Array
    carr = []
    f = open(path, "r")
    f1 = f.readlines()
    for statement in f1:
        carr.append(statement.rstrip("\n"))
    return carr

def getAngry(path):
    #imports AngryIP Scanner text files
    li = []
    f = open(path)
    f1 = f.readlines()
    for c,row in enumerate(f1):
        if c < 7 or row == "":
            continue
        li.append(row[:row.find("  ")])
    return li

def getIpArr(path="locations.csv"):
    li = []
    with open(path, newline='', mode='r') as csvfile:
        info = csv.reader(csvfile, delimiter=',')
        for row in info:
            li.append(row)
    return li

def IPwrite(li, path="locations.csv"):
    #creates file with IP in it
    with open(path, mode='a') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(li)
