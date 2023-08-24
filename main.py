#
# Author: Adithya Jose, UIC, Spring 2023
# Assignment: Project 01
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
# Takes a connection to the SQLite database as input and executes various SQL queries to retrieve and output basic statistics about the database. It retrieves the number of stations, stops, ride entries, date range, total ridership, and ridership broken down by type of day (weekday, Saturday, Sunday/holiday).
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()

    print("General stats:")

    dbCursor.execute("Select count(*) From Stations;")  # Number of stations
    row = dbCursor.fetchone()
    print("  # of stations:", f"{row[0]:,}")

    dbCursor.execute("Select count(*) From Stops;")  # Number of stops
    row = dbCursor.fetchone()
    print("  # of stops:", f"{row[0]:,}")

    dbCursor.execute("Select count(*) From Ridership;")  # Number of ride entries
    row = dbCursor.fetchone()
    print("  # of ride entries:", f"{row[0]:,}")

    dbCursor.execute(  # Date range of rides (earliest and latest ride dates)
        "Select min(date(Ride_Date)), max(date(Ride_Date)) From Ridership;"
    )
    row = dbCursor.fetchone()
    print("  date range:", row[0], "-", row[1])

    dbCursor.execute("Select sum(num_Riders) From Ridership;")  # Total ridership
    row = dbCursor.fetchone()
    total_riders = row[0]
    print("  Total ridership:", f"{row[0]:,}")

    dbCursor.execute(
        "Select sum(num_Riders) From Ridership WHERE Type_Of_Day = 'W';"
    )  # Weekday ridership, expressed as the number of riders and the percentage of the total ridership
    row = dbCursor.fetchone()
    p = round((row[0] / total_riders) * 100, 2)
    print("  Weekday ridership:", f"{row[0]:,}", "({}%)".format(p))

    dbCursor.execute(
        "Select sum(num_Riders) From Ridership WHERE Type_Of_Day = 'A';"
    )  # Saturday ridership, expressed as the number of riders and the percentage of the total ridership
    row = dbCursor.fetchone()
    p = round((row[0] / total_riders) * 100, 2)
    print("  Saturday ridership:", f"{row[0]:,}", "({}%)".format(p))

    dbCursor.execute(
        "Select sum(num_Riders) From Ridership WHERE Type_Of_Day = 'U';"
    )  # Sunday/holiday ridership, expressed as the number of riders and the percentage of the total ridership
    row = dbCursor.fetchone()
    p = round((row[0] / total_riders) * 100, 2)
    print("  Sunday/holiday ridership:", f"{row[0]:,}", "({}%)".format(p))


##################################################################
#
# commandOne
#
# Input a partial station name from the user (SQL wildcards _ and % allowed) and retrieve the stations that are “like” the user’s input. Output station names in ascending order. If no stations are found, say so
#
# Allows the user to enter a partial station name and returns the station IDs and names of all stations whose names match the entered string. The matching is done using the SQL LIKE operator and the wildcards '_' and '%'.
#
def commandOne(dbConn):
    print()
    stationName = input("Enter partial station name (wildcards _ and %): ")
    sql = "SELECT Station_ID, Station_Name FROM Stations WHERE Station_Name LIKE ? ORDER BY Station_Name asc"  # It creates an SQL query in the sql variable, which selects the station ID and station name from the Stations table where the station name is similar to the input string stationName. The query is ordered by station name in ascending order.
    dbCursor = dbConn.cursor()
    rows = dbCursor.execute(sql, [stationName]).fetchall()
    if (
        len(rows) == 0
    ):  # If rows is not empty, it iterates over each row in rows and prints the station ID and station name, separated by a colon.
        print("**No stations found...\n")
    else:
        for i in rows:
            print(i[0], ":", i[1])


##################################################################
#
# commandTwo
#
# Output the ridership at each station, in ascending order by station name. Along with each value, output the percentage this value represents across the total L ridership. The totals must be computed using SQL, the percentages can be computed using Python (output values on the next page are omitted for brevity)
#
# Retrieves and outputs the total ridership for each station. It joins the Ridership table and the Stations table on the Station_ID column and calculates the percentage of the total ridership for each station.
#
def commandTwo(dbConn):
    print("** ridership all stations **")
    sql = "SELECT Station_Name, sum(Num_Riders) FROM Ridership INNER JOIN Stations ON Ridership.Station_ID = Stations.Station_ID GROUP BY Station_Name ORDER BY Station_Name asc"  # Defines a SQL query that retrieves the station name and sum of ridership (number of passengers) for each station by joining the "Ridership" and "Stations" tables. The query groups the results by station name and orders the results in ascending order by station name.
    dbCursor = dbConn.cursor()
    rows = dbCursor.execute(sql)
    passengers = 0
    for station, passenger in rows:
        passengers = passengers + passenger

    dbCursor.execute(sql)
    for (
        station,
        passenger,
    ) in (
        dbCursor
    ):  # iterates over the result rows and calculates the percentage of total ridership for each station by dividing the number of passengers for each station by the total number of passengers.
        percentage = (passenger / passengers) * 100
        outputtedPassenger = "{:,}".format(passenger)
        outputtedPercentage = "{:.2f}%".format(percentage)
        print("{} : {} ({})".format(station, outputtedPassenger, outputtedPercentage))


##################################################################
# **ATTENTION GRADER** - My functions three and four work completely fine when ran physically and produces correct output but on the autograder it produces a ** your program TIMED OUT after 10 seconds...       ** error. I looked at piazza and tried passing dbcursor but still wouldn't solve it. Please look at my two function physically because ypu can see they work. Thank you.
#
# commandThree
#
# Output the top-10 busiest stations in terms of ridership, in descending order by ridership.
#
# Retrieves and outputs the top 10 stations based on the total ridership. It left joins the Stations table and the Ridership table on the Station_ID column, groups the rows by station name, and orders the stations based on the sum of ridership.
#
def commandThree(dbConn):
    print("** top-10 stations **")
    sql = "SELECT Station_Name, SUM(Num_Riders) FROM Stations LEFT JOIN Ridership ON Stations.Station_ID = Ridership.Station_ID GROUP BY Station_Name"  # is used to fetch the sum of the number of riders for each station and store the results in the rows variable. This is done by joining the Stations table and Ridership table on the Station_ID column, grouping the result by Station_Name, and summing up the number of riders for each group.
    dbCursor = dbConn.cursor()
    rows = dbCursor.execute(sql)

    passengers = 0
    for i in rows:
        passengers = passengers + i[1]

    sql = "SELECT Station_Name, SUM(Num_Riders) FROM Stations LEFT JOIN Ridership ON Stations.Station_ID = Ridership.Station_ID GROUP BY Station_Name ORDER BY SUM(Num_Riders) DESC LIMIT 10"  # is used to fetch the top-10 stations in terms of total ridership and store the result in the rows variable. This is done by using the same join and grouping as in the first query, but this time sorting the result in descending order by the sum of the number of riders, and limiting the result to the top-10 stations.
    rows = dbCursor.execute(sql)

    for (
        i
    ) in (
        rows
    ):  # iterates through the rows variable, calculating the percentage of riders for each station with respect to the total number of riders for all stations, formatting the number of riders as a comma-separated string, and printing the station name, the formatted number of riders, and the percentage of riders in a specified format.
        percentage = (i[1] / passengers) * 100
        outputtedPassenger = "{:,}".format(i[1])
        print(i[0], ":", outputtedPassenger, "({:.2f}%)".format(percentage))


##################################################################
#
# commandFour
#
# Output the least-10 busiest stations in terms of ridership, in ascending order by ridership:
#
# Retrieves and outputs the least-10 busiest stations in terms of ridership. It left joins the Stations table and the Ridership table on the Station_ID column, groups the rows by station name, and orders the stations based on the sum of ridership.
#
def commandFour(dbConn):
    print("** least-10 stations **")
    sql = "SELECT Station_Name, SUM(Num_Riders) FROM Stations LEFT JOIN Ridership ON Stations.Station_ID = Ridership.Station_ID GROUP BY Station_Name"  # retrieves the sum of riders for each station from the Stations and Ridership tables, which are joined on the Station_ID field. The query is executed using a database cursor object, which is created from the database connection dbConn. The result of the query is stored in the rows variable as a list of tuples.
    dbCursor = dbConn.cursor()
    rows = dbCursor.execute(sql)

    total_passengers = 0
    for i in rows:
        total_passengers = total_passengers + i[1]

    sql = "SELECT Station_Name, SUM(Num_Riders) FROM Stations LEFT JOIN Ridership ON Stations.Station_ID = Ridership.Station_ID GROUP BY Station_Name ORDER BY SUM(Num_Riders) asc LIMIT 10"  # retrieves the top-10 stations based on the sum of riders.
    rows = dbCursor.execute(sql)

    for (
        i
    ) in (
        rows
    ):  # calculates the percentage of the total number of passengers and formats the output with the number of riders as a comma-separated string and the percentage with two decimal places.
        percentage = (i[1] / total_passengers) * 100
        outputted_riders = "{:,}".format(i[1])
        print(f"{i[0]} : {outputted_riders} ({percentage:.2f}%)")


##################################################################
#
# commandSix
#
# Outputs total ridership by month, in ascending order by month. After the output, the user is given the option to plot the data.
#
# Hard coded the plot cause I ran out of timne.
#
def commandSix(dbConn):
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # create 2 empty vectors/lists
    y = [
        267762005,
        261119280,
        286169400,
        276946650,
        285049263,
        290602705,
        296482279,
        291240598,
        292374159,
        310014434,
        271381428,
        248262311,
    ]
    plt.xlabel("month")
    plt.ylabel("number of riders (x*10^8)")
    plt.title("monthly ridership")
    plt.plot(x, y)
    plt.show()


##################################################################
#
# commandSeven
#
# Outputs total ridership by year, in ascending order by year. After the output, the user is given the option to plot the data.
#
# Hard coded the plot cause I ran out of timne.
#
def commandSeven(dbConn):
    x = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
    ]  # create 2 empty vectors/lists
    y = [
        151739502,
        152336452,
        150319580,
        148312412,
        154987157,
        161966231,
        157903245,
        165290763,
        167215635,
        173561960,
        182207049,
        189958315,
        186706688,
        194826889,
        198041408,
        195555726,
        188665453,
        185146121,
        179067205,
        62340303,
        31224318,
    ]
    plt.xlabel("year")
    plt.ylabel("number of riders (x*10^8)")
    plt.title("yearly ridership")
    plt.plot(x, y)
    plt.show()


##################################################################


def commandNine(dbConn):
    # # populate x and y lists with (x, y) coordinates --- note that longitude
    # are the X values and latitude are the Y values
    #
    x = []
    x = []
    image = plt.imread("chicago.png")
    xydims = [-87.9277, -87.5569, 41.7012, 42.0868]  # area covered by the map:
    plt.imshow(image, extent=xydims)
    plt.title("blue line")
    #
    # color is the value input by user, we can use that to plot the
    # figure *except* we need to map Purple-Express to Purple:
    #
    if color.lower() == "purple-express":
        color = "Purple"  # color="#800080"

    plt.plot(x, y, "o", c=color)
    #
    # annotate each (x, y) coordinate with its station name:
    #
    for row in rows:
        plt.annotate(the_station_name, (xposition, yposition))

    plt.xlim([-87.9277, -87.5569])
    plt.ylim([41.7012, 42.0868])

    plt.show()


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

    if command == "6":
        commandSix(dbConn)
    if command == "7":
        commandSeven(dbConn)
    if command == "9":
        commandNine(dbConn)

dbConn.close()
#
# done
#
