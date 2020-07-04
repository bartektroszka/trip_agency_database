DROP TABLE IF EXISTS Reservations;
DROP TABLE IF EXISTS Trips;
DROP TABLE IF EXISTS Accommodations;
DROP TABLE IF EXISTS Clients;
DROP TABLE IF EXISTS Nodes;

-- physical data model

CREATE TABLE Nodes(
    node_id BIGINT PRIMARY KEY,
    node_location GEOGRAPHY,
    node_lat DOUBLE PRECISION,
    node_lon DOUBLE PRECISION,
    description TEXT
);

CREATE INDEX ON Nodes USING GIST(node_location);

CREATE TABLE Clients (
    name  TEXT  PRIMARY KEY, 
    reservation_number BIGINT DEFAULT 0,
    length REAL DEFAULT 0
);

CREATE TABLE Accommodations (
    accommodation_id SERIAL PRIMARY KEY,
    date_time  DATE,  
    name TEXT NOT NULL,
    node_id BIGINT NOT NULL,
    
    CONSTRAINT accommodations_name_fkey 
        FOREIGN KEY (name) 
        REFERENCES Clients (name),
    CONSTRAINT accommodations_node_id_fkey 
        FOREIGN KEY (node_id) 
        REFERENCES Nodes (node_id)
);

CREATE TABLE Trips (
    trip_id  BIGINT PRIMARY KEY,
    list_of_point_id BIGINT[],
    length REAL
);

CREATE TABLE Reservations (
    reservation_id     SERIAL  PRIMARY KEY,
    name  TEXT NOT NULL,
    trip_id  BIGINT  NOT NULL,
    start_date   DATE,
    
    CONSTRAINT reservations_name_fkey
        FOREIGN KEY (name)
        REFERENCES Clients (name),
    CONSTRAINT reservations_trip_id_fkey
        FOREIGN KEY (trip_id)
        REFERENCES Trips (trip_id)
);

