import psycopg2


def node(node_id,lat, lon, description, cur):
    string = """INSERT INTO Nodes(node_id, node_lat, node_lon, node_location, description) VALUES ('%s', %s, %s, ST_GeographyFromText('SRID=4326;POINT(%s %s)') , '%s');""" %(str(node_id), lon, lat, lon, lat, description)
    cur.execute(string)

def catalog(version, nodes, cur):
    array = "ARRAY" + str(nodes)
    array_of_nodes = nodes
    length = 0
    for i in range(len(array_of_nodes) - 1):
        query = """SELECT ST_Distance((SELECT  node_location  FROM NODES WHERE node_id = %s),(SELECT  node_location  FROM NODES WHERE node_id = %s), true) """ % (array_of_nodes[i], array_of_nodes[i+1])
        cur.execute(query)
        dist = cur.fetchall()
        length += dist[0][0]
    string = """INSERT INTO Trips(trip_id, list_of_point_id, length) VALUES ('%s', %s, %s);""" %(str(version), array, length)
    cur.execute(string)


def trip(cyclist, date, version, cur):
    string = """INSERT INTO Clients(name) VALUES('%s') ON CONFLICT(name) DO NOTHING""" % (cyclist)
    string_1 = """INSERT INTO Reservations(name, start_date, trip_id) VALUES ('%s', '%s', %d);""" %(cyclist, date, version) 
    cur.execute(string)
    cur.execute(string_1)
    query = """SELECT length FROM Trips WHERE trip_id = %d""" %(version)
    cur.execute(query)
    length = cur.fetchall()[0][0]
    query = """UPDATE Clients SET length = length + %f WHERE name = '%s' """ %(length, cyclist)
    cur.execute(query)
    query = """UPDATE Clients SET reservation_number = reservation_number + 1 WHERE name = '%s' """ %(cyclist)
    cur.execute(query)

    query = """SELECT list_of_point_id FROM  Trips WHERE trip_id = %s""" %(str(version))
    cur.execute(query)
    list_of_nodes = cur.fetchall()[0][0]
    for i in range(len(list_of_nodes) - 2):
        query = """INSERT  INTO Accommodations(date_time, name, node_id) VALUES(TO_DATE('%s', 'YYYY/MM/DD') + INTERVAL '%d day', '%s', %s) """ %(date, i, cyclist, list_of_nodes[i+1])
        cur.execute(query)

def closest_nodes(ilat, ilon, cur):
    string = """ (SELECT ROUND(ST_Distance('SRID=4326;POINT(%s %s)'::geography, node_location, true))  AS dist)""" %(ilon, ilat)
    query = """SELECT node_id,node_lat, node_lon,"""  + string  +  """FROM Nodes ORDER BY dist, node_id LIMIT 3"""
    cur.execute(query)
    nodes = cur.fetchall()
    list_of_nodes = []
    for line in nodes:
        list_of_nodes.append(line)
    return list_of_nodes


def cyclists(limit, cur):
    query = """SELECT name, reservation_number, ROUND(length) FROM Clients ORDER BY length, name LIMIT %s""" %(limit)
    cur.execute(query)
    ranking = cur.fetchall()
    return ranking


def party(cyclist, date, cur):
    node_location_query = """SELECT node_location FROM Nodes WHERE node_id = (SELECT node_id FROM Accommodations WHERE name = '%s' AND date_time = '%s')""" %(cyclist, date)
    cur.execute(node_location_query)
    node_location = cur.fetchall()[0][0]
    same_date = """ SELECT * FROM Accommodations WHERE  date_time = '%s'   """ %(date)
    query = """SELECT name, nodes.node_id, node_location  FROM (%s) AS same_date  JOIN   Nodes AS nodes ON same_date.node_id = nodes.node_id""" %(same_date)
    final_query = """ SELECT name, node_id, ST_DISTANCE((%s), node_location) FROM (%s) AS query WHERE ST_DISTANCE((%s), node_location) < 20000 AND query.name != '%s' """ %(node_location_query, query, node_location_query, cyclist)
    cur.execute(final_query)
    party = cur.fetchall()
    return party



def guests(node, date, cur):
    query = """
    SELECT name FROM Accommodations WHERE node_id = %s AND date_time  = '%s' ORDER BY name""" %(node, date)
    cur.execute(query)
    cyclists = cur.fetchall()
    return cyclists

