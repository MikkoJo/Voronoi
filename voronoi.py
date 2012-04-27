'''
Created on Apr 18, 2012

@author: Mikko Johansson
'''
import json
import codecs
#from exceptions import KeyError
from priorityqueue import PriorityQueue
from dcel import Dcel
from dcel import Hedge
from dcel import Vertex
from dcel import Face

#from RBTree import RBTree
from binarysearchtree import BinarySearchTree

from binarysearchtree import _LEFT, _RIGHT, _PARENT, _VALUE, _SORT_KEY



sites = {}
edge_list = Dcel()
beach_line = BinarySearchTree()

def parse_input(infile):
    infilep = codecs.open(infile, 'r', 'utf-8')
    geoJson = json.load(infilep)
    infilep.close()
    features = geoJson['features']

    pointArray = []
    for f in features:
        x = f['geometry']['coordinates'][0]
        y = f['geometry']['coordinates'][1]
        pointArray.append(((x,y), None))

    return pointArray

def handle_site(site):
    # insert new site to the beachline
    beach_line.insert(site, sites, edge_list)

def handle_circle(site):
    print ("handle_circle: ")
    point = site[0]
    node = site[1]
    print(point)
    print(node[_VALUE]['break_point'])
    print(node[_VALUE]['point'])
    #remove possible circle events involving this site
    predecessor = beach_line.pred(node)
    successor = beach_line.succ(node)
    print("pre")
    print(predecessor[_VALUE]['point'])
    print(predecessor[_PARENT][_VALUE]['break_point'])
    print("endpre")
    print(successor[_VALUE]['point'])

    if predecessor[_VALUE]['pointer'] is not None:
        print("not None")
        #print(predecessor[_VALUE]['pointer'])
        sites.delete(predecessor[_VALUE]['pointer'])
        predecessor[_VALUE]['pointer'] = None
        print(predecessor[_PARENT][_VALUE]['break_point'])

    if successor[_VALUE]['pointer'] is not None:
        sites.delete(successor[_VALUE]['pointer'])
        successor[_VALUE]['pointer'] = None

    r = node[_VALUE]['radius']
    #Add breakpoint to the vertex list
    ver = Vertex(point[0], point[1] - r)
    edge_list.vertices.append(ver)
    #Update beach_line and add pointers to hedges to new vertex
    parent = node[_PARENT]
    site = node[_VALUE]['point']
    del node[:]

    new_hedge1 = Hedge()
    new_hedge2 = Hedge()
    new_hedge1.origin = ver
    ver.hedgelist.append(new_hedge1)
    new_hedge1.twin = new_hedge2
    new_hedge2.twin = new_hedge1
    edge_list.hedges.append(new_hedge1)
    edge_list.hedges.append(new_hedge2)

    right_hedge = parent[_VALUE]['hedge']
    left_hedge = parent[_PARENT][_VALUE]['hedge']

    if right_hedge.origin is None:
        right_hedge.origin = ver
        ver.hedgelist.append(right_hedge)
    else:
        right_hedge.twin.orig = ver
        ver.hedgelist.append(right_hedge.twin)

    if left_hedge.origin is None:
        left_hedge.origin = ver
        ver.hedgelist.append(left_hedge)
    else:
        left_hedge.twin.orig = ver
        ver.hedgelist.append(left_hedge.twin)

    #We always delete the parent
    node = parent
    parent = node[_PARENT]
    print("before delete" + str(predecessor[_PARENT][_VALUE]['break_point']))
    #Deleted leaf was left child
    if node[_RIGHT]:
        new_right = node[_VALUE]['break_point'][1]
        node[:] = node[_RIGHT]
        node[_PARENT] = parent
        print("was right" + str(predecessor[_PARENT][_VALUE]['break_point']))
        while parent[_VALUE]['break_point'][1] != site:
            parent = parent[_PARENT]
        bp_left = parent[_VALUE]['break_point'][0]
        parent[_VALUE]['break_point'] = (bp_left, new_right)
    else:
        new_left = node[_VALUE]['break_point'][0]
        print("was left" + str(predecessor[_PARENT][_VALUE]['break_point']))
        node[:] = node[_LEFT]
        print("was left" + str(parent[_VALUE]['break_point']))
        print("was left" + str(node[_VALUE]['point']))
        print("was left" + str(node[_PARENT][_VALUE]['point']))
        print("was left" + str(predecessor[_PARENT][_VALUE]['break_point']))
        node[_PARENT] = parent
        predecessor[_PARENT] = parent
        print("was left" + str(node[_PARENT][_VALUE]['break_point']))
        print("was left" + str(predecessor[_PARENT][_VALUE]['break_point']))
        # skip original grandparent
        parent = parent[_PARENT]
        while parent[_VALUE]['break_point'][0] != site:
            parent = parent[_PARENT]
        bp_right = parent[_VALUE]['break_point'][1]
        parent[_VALUE]['break_point'] = (new_left, bp_right)

    #link new hedge to node
    parent[_VALUE]['hedge'] = new_hedge1

    # check new arc triples
    # Former left in the middle
    print("left1" + str(predecessor[_PARENT][_VALUE]['break_point']))

    left1 = beach_line.pred(predecessor)
    right1 = beach_line.succ(predecessor)
    circle_event = beach_line._get_circle_event(left1[_VALUE]['point'],
                                                predecessor[_VALUE]['point'],
                                                right1[_VALUE]['point'],
                                                site[1])
    if circle_event is not None:
        circle_event_site = (circle_event[0], predecessor)
        predecessor[_VALUE]['radius'] = circle_event[1]
        #print(type(circle_event_site))
        predecessor[_VALUE]['pointer'] = circle_event_site
        sites.add(circle_event_site)

    # Former right in the middle
    left2 = beach_line.pred(successor)
    right2 = beach_line.succ(successor)
    circle_event = beach_line._get_circle_event(left2[_VALUE]['point'],
                                                successor[_VALUE]['point'],
                                                right2[_VALUE]['point'],
                                                site[1])
    if circle_event is not None:
        circle_event_site = (circle_event[0], successor)
        successor[_VALUE]['radius'] = circle_event[1]
        #print(type(circle_event_site))
        successor[_VALUE]['pointer'] = circle_event_site
        sites.add(circle_event_site)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print ("Usage: " + sys.argv[0] + " infile outfile\n")
        print ("infile format: GeoJSON featurecollection of points\n")
        print ("outfile: a GeoJSON featurecollection of points and polygons\n")
        exit(0)

    pointList = parse_input(sys.argv[1])

    pointList = []
    import random

    #for a in range(0,200):
    #    pointList.append(((random.randint(0,1000), random.randint(0,1000)), None))

    pointList.append(((8,12), None))
    pointList.append(((16,9), None))
    pointList.append(((3,5), None))
    sites = PriorityQueue(pointList[:200])



    #Test
    counter = 1
    # Go through sites
#    while sites and counter < 20:
    while sites:
#        try:
        s = sites.pop()
        #Check if site event
        if s[1] == None:
            #print (s)
            handle_site(s[0])
        else:
#            node = s[1]
#            print("len_node: " + str(len(node)))
            handle_circle(s)
#        except KeyError as err:
#            print ("error")
#            print err
#            break

        #Test
        if s[1] is None:
            print ("SiteEvent: "),
        else:
            print("CircleEvent: "),
        print (str(counter) + ": x: " + str(s[0][0]) + ": y: " + str(s[0][1]))
        counter += 1

