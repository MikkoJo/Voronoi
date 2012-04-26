'''
Created on Apr 18, 2012

@author: Mikko Johansson
'''
import json
import codecs
#from exceptions import KeyError
from priorityqueue import PriorityQueue
from dcel import Dcel
from RBTree import RBTree
from binarysearchtree import BinarySearchTree


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

def handleSite(site, sites):
    # insert new site to the beachline
    beach_line.insert(site, sites)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print ("Usage: " + sys.argv[0] + " infile outfile\n")
        print ("infile format: GeoJSON featurecollection of points\n")
        print ("outfile: a GeoJSON featurecollection of points and polygons\n")
        exit(0)

    pointList = parse_input(sys.argv[1])

    sites = PriorityQueue(pointList)



    #Test
    counter = 1
    # Go through sites
    while sites and counter < 20:
        try:
            s = sites.pop()
            #Check if site event
            if s[1] == None:
                #print (s)
                handleSite(s[0], sites)
#           else:
#               handleCircle(item)
        except KeyError:
            print ("error")
            break

        #Test
        print (str(counter) + ": " + str(s[0][1]))
        counter += 1

