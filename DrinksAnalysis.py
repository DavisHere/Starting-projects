import csv


#####################
# CSV -> Dictionary #
#####################

GST = 1.07
serviceTax = 1.1


# helper functions to make parse_files less messy
def read_csv(csvfilename):
    rows = []
    with open(csvfilename) as csvfile:
        file_reader = csv.reader(csvfile)
        for row in file_reader:
            rows.append(tuple(row))
    return rows

def createDict(rows):
    result = {}
    for row in rows:
        amt = row[0]
        name = row[1]
        amt = float(amt) * (1 * GST * serviceTax)
        if name not in result.keys():
            result[name] = [amt, 1]
        else:
            result[name][0] += amt
            result[name][1] += 1
    for key in result.keys():
        result[key][0] = round(result[key][0], 2)
    return result

# data = read_csv('drinks_receipts.csv')[1:]
# print(data)
# mydict = createDict(data)
# print(mydict)

def parse_files(csv_file):
    rows = read_csv(csv_file)[1:]  
    result = {}
    dateTracker = ""
    counter = 1
    for row in rows:
        date = row[2]
        if date and not dateTracker:
            dateTracker = date          # stores current date of receipt
            start = rows.index(row)     # index where new receipt starts
            counter = 1                 # track number of items in current receipt
            # print(start)
        
        elif date:
            selection = rows[start : start + counter]
            # print(selection)
            result[dateTracker] = createDict(selection)
            dateTracker = date
            counter = 1
            start = rows.index(row)
            # print(start)
            
        else:
            counter += 1

    # print(selection)
    return result

myDict = parse_files('drinks_receipts.csv')
# print(myDict)

# myDict = {'14-Feb': {'Davis': [28.77, 7], 'Ervin': [12.62, 3], 'Wei Hong': [12.51, 3], 'Hilson': [11.81, 3], 'Sze Ken': [11.89, 3], 'Irwin': [8.66, 2], 'Shawn': [3.92, 1], 'Kian Ming': [3.92, 1], 'Tim': [3.92, 1]}, '14-Aug': {'Davis': [22.62, 6], 'Ivan': [18.88, 5]}, '10-Jul': {'Ivan': [26.73, 6], 'Russ': [12.3, 3], 'Perry': [16.22, 3], 'Davis': [29.02, 6], 'Janelle': [15.05, 3]}}


####################
# getter functions #
####################

# all functions check the variable myDict
choices = "dates, money, drinks count, average drinks"
# choiceslst = choices.split(", ")
moneyIndex = 0
drinksCountIndex = 1

def getReceipt(date):
    return myDict[date]
# print(getReceipt("14-Feb"))

def listDates():
    return myDict.keys()

def listNames(date):
    return myDict[date].keys()

def listAllNames():
    temp = {}
    for date in myDict:
        receipt = getReceipt(date)
        for name_key in receipt:
            temp[name_key] = None
    return temp.keys()
# print( listAllNames() )

def getMoney(date, name):
    receipt = getReceipt(date)
    if name == "all":
        for namekey in receipt:
            print(namekey + ": " + str(receipt[namekey][moneyIndex]) )
    else:
        return receipt[name][moneyIndex]
# print(getMoney("14-Feb", "Davis"))
# print(getMoney("14-Feb", "all"))

def getTotalMoney(name):
    result = 0
    for date in myDict:
        result += getMoney(date, name)
    return result
# print( getTotalMoney("Davis") )

def getDrinks(date, name):
    receipt = getReceipt(date)
    if name == "all":
        for namekey in receipt:
            print(namekey + ": " + str(receipt[namekey][drinksCountIndex]) )
    else:
        return receipt[name][drinksCountIndex]
# print(getMoney("14-Feb", "Davis"))
# print(getDrinks("14-Feb", "all"))


def getTotalDrinks(name):
    result = 0
    for date in myDict:
        if name in listNames(date):
            result += getDrinks(date, name)

        else:
            continue
    return result
# print( getTotalDrinks("Davis") )

def getAverageDrinks(name):
    counter = 0
    for date in myDict:
        if name in listNames(date):
            counter += 1
        else:
            continue
    return getTotalDrinks(name) / counter
# print( getAverageDrinks("Davis") )

###############
## Interface ##
###############

greeting = "Sup. "

# find specific person vs all vs break

def askDate():
    print(myDict.keys())
    date = input("Which date? " )
    while date not in myDict.keys():
        date = input("Come again? ")
    return date

def askName(date):
    namelist = listNames(date)
    print( namelist )
    name = input("Anyone in particular? ")
    if name == "all":
        return "all"
    while name not in namelist:
        name = input("Come again? ")
    return name
        


def goTime():
    while True:
        print(greeting + "The options are " + choices)
        x = input("What will it be? ")
        match x:
            case "dates":
                print( listDates() )

            case "money":
                date = askDate()
                name = askName(date)
                print( getMoney(date, name) )
            
            case "drinks count":
                date = askDate()
                name = askName(date)
                print( getDrinks(date, name) )

            case "average drinks":
                print( listAllNames())
                name = input("Anyone in particular? ")
                print( getAverageDrinks(name) )
        
    #     x = input("Anything else? ")
    #     if x == "no":
    #         break


goTime()


# print(myDict.keys())





