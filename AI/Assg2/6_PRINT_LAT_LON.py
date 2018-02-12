
import psycopg2


def getLatAndLog(ID):
    try:
        conn = psycopg2.connect("dbname='gis' user='postgres' host='localhost' password='postgres'")
    except:
        print "I am unable to connect to the database"
    cur = conn.cursor()
    cur.execute("SELECT LATITUDE,LONGITUDE FROM NODES WHERE NODE_ID="+ID+";");
    rows = cur.fetchall()
    return rows

with open("paths.txt", "r") as ins:
    for line in ins:
        rows = getLatAndLog(line)
        for row in rows:
            print str(row[0])+","+str(row[1])

