import psycopg2
from xml.dom import minidom
xmldoc = minidom.parse('JNTU_MIYAPUR.osm')


# Store Nodes in Database
itemlist = xmldoc.getElementsByTagName('node')
refList = []
try:
    conn = psycopg2.connect("dbname='gis' user='postgres' host='localhost' password='postgres'")
except:
    print "I am unable to connect to the database"
cur = conn.cursor()
cur.execute("TRUNCATE TABLE NODES")
conn.commit()
try:
    for s in itemlist:
        #print 1
        node_id = s.attributes['id'].value
        lat = s.attributes['lat'].value
        lon = s.attributes['lon'].value
        cur.execute("INSERT INTO NODES(NODE_ID,LATITUDE,LONGITUDE) values("+node_id+","+lat+","+lon+")")
except:
    print "Cannot insert into DB!"

conn.commit()
print "Done Inserting"
conn.close()


# Store Ways in Database


ways = xmldoc.getElementsByTagName('way')
refList = []
try:
    conn = psycopg2.connect("dbname='gis' user='postgres' host='localhost' password='postgres'")
except:
    print "I am unable to connect to the database"
cur = conn.cursor()
cur.execute("TRUNCATE TABLE WAYS")
conn.commit()
nodeway = ""
for way in ways:
    nodeway = ""
    wayid = way.attributes['id'].value
    nodes = way.getElementsByTagName("nd")

    for node in nodes:
        id = node.attributes['ref'].value
        print(id)
        nodeway += str(id) + ","


    nodeway = nodeway[0:len(nodeway)-1]
    cur.execute("INSERT INTO WAYS values(" + wayid + ",'" + nodeway +"')")
    conn.commit()

print "Done"



try:
    conn = psycopg2.connect("dbname='gis' user='postgres' host='localhost' password='postgres'")
except:
    print "I am unable to connect to the database"
cur = conn.cursor()
cur.execute("TRUNCATE TABLE NODE_NEIGHBOURS")
conn.commit()
cur.execute("SELECT PATH FROM WAYS WHERE WAY_ID=234286750;");
rows = cur.fetchall()
for row in rows:
    print row[0]


def returnNodes(ID):
    try:
        conn = psycopg2.connect("dbname='gis' user='postgres' host='localhost' password='postgres'")
    except:
        print "I am unable to connect to the database"
    cur = conn.cursor()
    cur.execute("SELECT PATH FROM WAYS WHERE WAY_ID="+ID+";");
    rows = cur.fetchall()
    conn.close()
    return rows

def addNeighbour(srcNode,Neighbour):
    try:
        conn = psycopg2.connect("dbname='gis' user='postgres' host='localhost' password='postgres'")
    except:
        print "I am unable to connect to the database"
    cur = conn.cursor()
    cur.execute("SELECT NEIGHBOURS FROM NODE_NEIGHBOURS WHERE NODE_ID="+srcNode+";")
    rows = cur.fetchall()
    if len(rows) == 0:
        cur.execute("INSERT INTO NODE_NEIGHBOURS values(" + srcNode + ",'" + Neighbour + "')")
        conn.commit()
    else:
        for row in rows:
            result = row[0] + str(":") + str(Neighbour)
            cur.execute("UPDATE NODE_NEIGHBOURS SET NEIGHBOURS='"+result+"' WHERE NODE_ID="+srcNode+";")
            conn.commit()
            break
    conn.close()


# Store Relations in table
relations = xmldoc.getElementsByTagName('relation')
for relation in relations:
    members = relation.getElementsByTagName("member")
    #print relation.attributes['id'].value
    #print "++"
    nodeList = []
    for member in members:
        id = member.attributes['ref'].value
        if member.attributes['type'].value == "way":
            rows = returnNodes(id)
            if len(rows) != 0:
                for row in rows:
                    Nodes = row[0].split(',');
                    for node in Nodes:
                        nodeList.append(node)
                    break
        if member.attributes['type'].value == "node":
            nodeList.append(id)
    #print "---------------------------------"
    for i in range(0,len(nodeList)-1):
        print nodeList[i]
        addNeighbour(nodeList[i],nodeList[i+1])
    #break
