import psycopg2


from math import cos, asin, sqrt
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a)) #2*R*asin...

try:
    conn = psycopg2.connect("dbname='gis' user='postgres' host='localhost' password='postgres'")
except:
    print "I am unable to connect to the database"
cur = conn.cursor()
cur.execute("TRUNCATE TABLE DISTANCES")
conn.commit()
cur.execute("SELECT * FROM NODE_NEIGHBOURS;");
rows = cur.fetchall()
lat1 = 0.0
lat2= 0.0
lon1=0.0
lon2=0.0
for row in rows:
    neighbours = row[1].split(":")
    cur.execute("SELECT LATITUDE,LONGITUDE FROM NODES WHERE NODE_ID=" + str(row[0]) + ";")
    res = cur.fetchall()
    for r in res:
        lat1 = r[0]
        lon1 = r[1]
    for neighbour in neighbours:
        cur.execute("SELECT LATITUDE,LONGITUDE FROM NODES WHERE NODE_ID="+str(neighbour)+";")
        res = cur.fetchall()
        for r in res:
            lat2 = r[0]
            lon2 = r[1]
        dis = distance(lat1,lon1,lat2,lon2)
        cur.execute("INSERT INTO DISTANCES VALUES("+str(row[0])+","+str(neighbour)+","+str(dis)+");")
        conn.commit()


#print distance(17.4967167,78.3616395,17.4967673,78.3623119)

