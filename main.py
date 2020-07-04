import func, json, sys, psycopg2

conn = None
if len(sys.argv) > 1:
    if sys.argv[1] == "--init":
        conn = psycopg2.connect(user = "app", password = "qwerty", host = "localhost", database = "student")
        cur = conn.cursor()
        cur.execute(open("init.sql", "r").read())
        print({"status": "OK"})
        conn.commit()
        cur.close()

conn = psycopg2.connect(dbname="student", user="app", password="qwerty")
cur = conn.cursor()
print()
for line in sys.stdin:
    if line ==  "\n":
        break
    command = json.loads(line)
    if command["function"] == "node":
        func.node(command["body"]["node"],command["body"]["lat"], command["body"]["lon"], command["body"]["description"], cur)
        print({"status": "OK"})

    elif command["function"] == "catalog":
        func.catalog(command["body"]["version"],command["body"]["nodes"], cur)
        print({"status": "OK"})

    elif command["function"] == "trip":
        func.trip(command["body"]["cyclist"],command["body"]["date"], command["body"]["version"], cur)
        print({"status": "OK"})

    elif command["function"] == "closest_nodes":
        data = func.closest_nodes(command["body"]["ilat"], command["body"]["ilon"], cur)
        output = []
        for i in range(len(data)):
            node = data[i][0]
            olat = data[i][2]
            olon = data[i][1]
            distance = data[i][3]
            output.append({"node":node, "olat":olat, "olon":olon, "distance":round(distance)})
        print({"status": "OK", "data": output})   

    elif command["function"] == "guests":
        data = func.guests(command["body"]["node"],command["body"]["date"], cur)
        output = []
        for i in range(len(data)):
            icyclist = data[i][0]
            output.append({"cyclist":icyclist})
        print({"status": "OK", "data": output})  

    elif command["function"] == "cyclists":
        data = func.cyclists(command["body"]["limit"], cur)
        output = []
        for i in range(len(data)):
            cyclist = data[i][0]
            number = data[i][1]
            dist = data[i][2]
            output.append({"cyclist":cyclist, "no_trips":number, "distance":round(dist)})
        print({"status": "OK", "data": output})   

    elif command["function"] == "party":
        data = func.party(command["body"]["icyclist"], command["body"]["date"], cur)
        output = []
        for i in range(len(data)):
            ocyclist = data[i][0]
            number = data[i][1]
            dist = data[i][2]
            output.append({"ocyclist":ocyclist, "node":number, "distance":round(dist)})
        print({"status": "OK", "data": output})
    conn.commit()   

conn.commit()
cur.close()
conn.close()



