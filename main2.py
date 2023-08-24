
#
# header comment? Overview, name, etc.
#

import sqlite3
import matplotlib.pyplot as plt


##################################################################
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()

    print("General stats:")

    dbCursor.execute("Select count(*) From Stations;")
    row = dbCursor.fetchone()
    print("  # of stations:", f"{row[0]:,}")

    dbCursor.execute("Select count(*) From Stops;")
    row = dbCursor.fetchone()
    print("  # of stops:", f"{row[0]:,}")

    dbCursor.execute("Select count(*) From Ridership;")
    row = dbCursor.fetchone()
    print("  # of ride entries:", f"{row[0]:,}")

    dbCursor.execute(
        "Select min(date(Ride_Date)), max(date(Ride_Date)) From Ridership;"
    )
    row = dbCursor.fetchone()
    print("  date range:", row[0], "-", row[1])

    dbCursor.execute("Select sum(num_Riders) From Ridership;")
    row = dbCursor.fetchone()
    total_riders = row[0]
    print("  Total ridership:", f"{row[0]:,}")

    dbCursor.execute("Select sum(num_Riders) From Ridership WHERE Type_Of_Day = 'W';")
    row = dbCursor.fetchone()
    p = round((row[0] / total_riders) * 100, 2)
    print("  Weekday ridership:", f"{row[0]:,}", "({}%)".format(p))

    dbCursor.execute("Select sum(num_Riders) From Ridership WHERE Type_Of_Day = 'A';")
    row = dbCursor.fetchone()
    p = round((row[0] / total_riders) * 100, 2)
    print("  Saturday ridership:", f"{row[0]:,}", "({}%)".format(p))

    dbCursor.execute("Select sum(num_Riders) From Ridership WHERE Type_Of_Day = 'U';")
    row = dbCursor.fetchone()
    p = round((row[0] / total_riders) * 100, 2)
    print("  Sunday/holiday ridership:", f"{row[0]:,}", "({}%)".format(p))


##################################################################


def commandOne(dbConn):
    print()
    stationName = input("Enter partial station name (wildcards _ and %): ")
    sql = "SELECT Station_ID, Station_Name FROM Stations WHERE Station_Name LIKE ? ORDER BY Station_Name asc"
    dbCursor = dbConn.cursor()
    rows = dbCursor.execute(sql, [stationName]).fetchall()
    if len(rows) == 0:
        print("**No stations found...\n")
    else:
        for i in rows:
            print(i[0], ":", i[1])


##################################################################


def commandTwo(dbConn):
    print("** ridership all stations **")
    sql = "SELECT Station_Name, sum(Num_Riders) FROM Ridership INNER JOIN Stations ON Ridership.Station_ID = Stations.Station_ID GROUP BY Station_Name ORDER BY Station_Name asc"
    dbCursor = dbConn.cursor()
    rows = dbCursor.execute(sql)
    passengers = 0
    for station, passenger in rows:
        passengers = passengers + passenger

    dbCursor.execute(sql)
    for station, passenger in dbCursor:
        percentage = (passenger / passengers) * 100
        outputtedPassenger = "{:,}".format(passenger)
        outputtedPercentage = "{:.2f}%".format(percentage)
        print("{} : {} ({})".format(station, outputtedPassenger, outputtedPercentage))


##################################################################


def commandThree(dbConn):
    print("** top-10 stations **")
    sql = "SELECT Station_Name, SUM(Num_Riders) FROM Stations LEFT JOIN Ridership ON Stations.Station_ID = Ridership.Station_ID GROUP BY Station_Name"
    dbCursor = dbConn.cursor()
    rows = dbCursor.execute(sql)

    passengers = 0
    for i in rows:
        passengers = passengers + i[1]

    sql = "SELECT Station_Name, SUM(Num_Riders) FROM Stations LEFT JOIN Ridership ON Stations.Station_ID = Ridership.Station_ID GROUP BY Station_Name ORDER BY SUM(Num_Riders) DESC LIMIT 10"
    rows = dbCursor.execute(sql)

    for i in rows:
        percentage = (i[1] / passengers) * 100
        outputtedPassenger = "{:,}".format(i[1])
        print(i[0], ":", outputtedPassenger, "({:.2f}%)".format(percentage))


##################################################################


def commandFour(dbConn):
    print("** least-10 stations **")
    sql = "SELECT Station_Name, SUM(Num_Riders) FROM Stations LEFT JOIN Ridership ON Stations.Station_ID = Ridership.Station_ID GROUP BY Station_Name"
    dbCursor = dbConn.cursor()
    rows = dbCursor.execute(sql)

    total_passengers = 0
    for i in rows:
        total_passengers = total_passengers + i[1]

    sql = "SELECT Station_Name, SUM(Num_Riders) FROM Stations LEFT JOIN Ridership ON Stations.Station_ID = Ridership.Station_ID GROUP BY Station_Name ORDER BY SUM(Num_Riders) asc LIMIT 10"
    rows = dbCursor.execute(sql)

    for i in rows:
        percentage = (i[1] / total_passengers) * 100
        outputted_riders = "{:,}".format(i[1])
        print(f"{i[0]} : {outputted_riders} ({percentage:.2f}%)")


##################################################################



##################################################################
#
# main
#
print("** Welcome to CTA L analysis app **")
print()

dbConn = sqlite3.connect("CTA2_L_daily_ridership.db")

print_stats(dbConn)

print()

command = ""

while command != "x":

    command = input("Please enter a command (1-9, x to exit): ")

    if (
        (command != "1")
        and (command != "2")
        and (command != "3")
        and (command != "4")
        and (command != "5")
        and (command != "x")
    ):
        print("**Error, unknown command, try again...")

    if command == "1":
        commandOne(dbConn)

    if command == "2":
        commandTwo(dbConn)

    if command == "3":
        commandThree(dbConn)

    if command == "4":
        commandFour(dbConn)

    # if command == "5":
    #     commandFive(dbConn)

dbConn.close()
#
# done
#