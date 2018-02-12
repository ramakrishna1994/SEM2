import psycopg2
from operator import itemgetter
from collections import namedtuple


openlist = []
closedlist = []
startstate = '2422989021'
goalstate = '2422989180'
# Declaring namedtuple() for Node Structure
node_structure = namedtuple('NodeStructure', ['node_id', 'latitude', 'longitude','f','g','h','pathlength','parent'])

try:
    conn = psycopg2.connect("dbname='gis' user='postgres' host='localhost' password='postgres'")
except:
    print "I am unable to connect to the database"
cur = conn.cursor()

def getHeuristicDistance(nodeid):
    #print "nodeid="+str(nodeid)
    cur.execute("SELECT DISTANCE FROM HEURISTICS WHERE NODE_ID="+nodeid+";");
    rows = cur.fetchall()
    for row in rows:
        return row[0]

def getNeighboursDataFromDB(nodeid):
    #print "nodeid=" + str(nodeid)
    cur.execute("SELECT NEIGHBOURS FROM NODE_NEIGHBOURS WHERE NODE_ID="+nodeid+";");
    rows = cur.fetchall()
    for row in rows:
        return row[0]

def getDistanceBetweenSourceAndDestination(source_node,destination_node):
    cur.execute("SELECT DISTANCE FROM DISTANCES WHERE SOURCE_NODE='" + source_node + "' AND DESTINATION_NODE='"+destination_node+"'")
    rows = cur.fetchall()
    for row in rows:
        return row[0]

def getNeighboursDataInAList(nodeid):
    neighbours = getNeighboursDataFromDB(nodeid)
    neighboursList = neighbours.split(":")
    return  neighboursList

def buildNeighbourNodesAndSendThemBackAsList(parentnode):
    neigbourNodeStructureList = []
    neighboursList = getNeighboursDataInAList(parentnode.node_id)
    for n in neighboursList:
        print n
        g = parentnode.g + getDistanceBetweenSourceAndDestination(parentnode.node_id,n)
        h = getHeuristicDistance(n)
        f = g + h
        pathlength = parentnode.pathlength + 1
        newNode = node_structure(n,"","",f,g,h,pathlength,parentnode.node_id)
        neigbourNodeStructureList.append(newNode)
    return neigbourNodeStructureList

def isNodeThereInOpenListAndShorter_F(node_to_check):
    for l in openlist:
        #print str(node_to_check.node_id)+" "+str(l.node_id)
        if l.node_id == node_to_check.node_id:
            #print str(l.f) + " " + str(node_to_check.f)
            if l.f <= node_to_check.f and l.pathlength == node_to_check.pathlength:
                return 1;
    return 0

def isNodeThereInClosedListAndShorter_F(node_to_check):
    for l in closedlist:
        #print str(node_to_check.node_id) + " " + str(l.node_id)
        if (l.node_id) == (node_to_check.node_id):
            #print str(l.f) + " " + str(node_to_check.f)
            if l.f <= node_to_check.f and l.pathlength == node_to_check.pathlength:
                return 1;
    return 0

def printList(givenlist,name):
    print 'Printing List : '+name
    for l in givenlist:
        print l


hd = getHeuristicDistance(startstate)
openlist.append(node_structure(startstate,'','',hd,0,hd,0,'none'))

i = 0;

while len(openlist)!=0:
    openlist = sorted(openlist, key=itemgetter(node_structure._fields.index('f')))
    poppednode = openlist.pop(0)
    print 'parent : ' + str(poppednode)
    if poppednode.node_id == goalstate:
        closedlist.append(poppednode)
        break
    neighbourNodeStructureList = buildNeighbourNodesAndSendThemBackAsList(poppednode)
    for n in neighbourNodeStructureList:
        print 'child : ' + str(n)
        isNodeInClosedList = isNodeThereInClosedListAndShorter_F(n)
        isNodeInOpenList   = isNodeThereInOpenListAndShorter_F(n)
        #print str(isNodeInClosedList) + " " + str(isNodeInOpenList) + str(isNodeInClosedList|isNodeInOpenList)
        if not(isNodeInOpenList | isNodeInClosedList):
            openlist.append(n)
    closedlist.append(poppednode)
    printList(openlist,'Open')
    printList(closedlist,'Closed')
    print '---------------------------------------------------------------------------------'

closedlist = sorted(closedlist, key=itemgetter(node_structure._fields.index('f')))

def getparentForANode(node_id):
    for n in closedlist:
        if node_id == n.node_id:
            return n.parent

s = goalstate
while True:
    print str(s)
    s = getparentForANode(s)
    if s=='none':
        break
