#!/usr/bin/python
import calendar
import datetime

tab = "\t"
nextLine = "\n"
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


def writeRow(fileName, date, row):
    # date and time; sensor1, temperature1, humidity1, sensor2, temperature2, humidity2
    # Open a file
    outputFile = open(fileName, "a")
    outputFile.write(dateToStrDate(date))
    outputFile.write(tab)
    outputFile.write(str(dateToMSeconds(date)))

    for entry in row:
        outputFile.write(tab)
        outputFile.write(str(entry))

    outputFile.write(nextLine)
    # Close opened file
    outputFile.close()


def strDateToDateF(strDate, dateFormat):
    return datetime.datetime.strptime(strDate, dateFormat)


def strDateToDate(strDate):
    return strDateToDateF(strDate, DATE_TIME_FORMAT)


def strDateToMSeconds(strDate):
    return calendar.timegm(datetime.datetime.strptime(strDate, DATE_TIME_FORMAT).timetuple()) * 1000


def dateToStrDateF(date, dateFormat):
    return date.strftime(dateFormat)


def dateToStrDate(date):
    return dateToStrDateF(date, DATE_TIME_FORMAT)


def dateToMSeconds(date):
    return calendar.timegm(date.timetuple()) * 1000


def readData(fileName):
    result = []
    with open(fileName, 'r') as fi:
        data = fi.readlines()
        for line in data:
            result.append(line.replace(nextLine, "").split(tab))

    return result


def readDataRange(fileName, dateFrom, dateTo):
    tmp = strDateToDateF(dateTo, DATE_FORMAT)
    dateToPlusOne = dateToStrDateF(tmp.replace(day=tmp.day + 1), DATE_FORMAT)
    file = open(fileName, 'r')
    start = False
    result = []
    for line in file:
        #print line
        if not start and line.startswith(dateFrom):
            start = True

        if start and line.startswith(dateToPlusOne):
            break

        if start:
            result.append(line.replace(nextLine, "").split(tab))

    file.close()
    return result


def readAndConvertDataRang(fileName, dateFrom, dateTo):
    tmp = strDateToDateF(dateTo, DATE_FORMAT)
    dateToPlusOne = dateToStrDateF(tmp.replace(day=tmp.day + 1), DATE_FORMAT)
    file = open(fileName, 'r')
    start = False
    result = []
    for line in file:
        if not start and line.startswith(dateFrom):
            start = True

        if start and line.startswith(dateToPlusOne):
            break

        if start:
            row = line.replace(nextLine, "").split(tab)
            result.append([long(row[1]), float(row[3]), float(row[4]), float(row[6]), float(row[7])])

    file.close()
    return result

#fName = "data.csv"
#writeRow(fName, datetime.datetime.now(), "1", "2", "20", "20", "60", "60")
#print(readData(fName))

#convert
#oldData = readData(fName)
#for row in oldData:
#print row[0].split('.')[0]
#writeRow("newdata.csv", strDateToDate(row[0].split('.')[0]), row[2], row[3], row[4], row[5], row[6], row[7])
