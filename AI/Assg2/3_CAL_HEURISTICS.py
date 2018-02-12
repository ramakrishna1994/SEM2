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

cur.execute("TRUNCATE TABLE HEURISTICS")
conn.commit()

tarlat = 17.4774960  #Balanagar
tarlon = 78.4209414
nodesList = []
cur.execute("SELECT * FROM NODE_NEIGHBOURS;");
rows = cur.fetchall()
for row in rows:
    nodesList.append(row[0])
    neighbours = row[1].split(":")
    for neighbour in neighbours:
        nodesList.append(neighbour)

uniqueList = set(nodesList)
for l in uniqueList:
    cur.execute("SELECT LATITUDE,LONGITUDE FROM NODES WHERE NODE_ID="+str(l));
    res = cur.fetchall()
    for r in res:
        dis = distance(r[0],r[1],tarlat,tarlon)
        cur.execute("INSERT INTO HEURISTICS VALUES(" + str(l) + "," + str(dis) + ");")
        conn.commit()
        break

