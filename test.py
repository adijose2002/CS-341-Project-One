import sqlite3

def get_stop_names(line_color):
    connection = sqlite3.connect("CTA2_L_daily_ridership.db")
    cursor = connection.cursor()

    query = f"SELECT stop_id, stop_name, direction, ada FROM stops WHERE line_color='{line_color.upper()}' ORDER BY stop_id"
    cursor.execute(query)

    result = cursor.fetchall()
    connection.close()

    return result

def format_output(stops):
    output = []
    for stop in stops:
        accessible = "yes" if stop[3] == 1 else "no"
        output.append(f"{stop[1]} : direction = {stop[2]} (accessible? {accessible})")
    return "\n".join(output)

while True:
    line_color = input("Enter a line color (e.g. Red or Yellow): ")
    if line_color.lower() == "x":
        break

    stops = get_stop_names(line_color)

    if len(stops) == 0:
        print("**No such line...")
    else:
        output = format_output(stops)
        print(output)
