'''
Created on Apr 18, 2012

@author: Mikko Johansson
'''
import json
import codecs
#from exceptions import KeyError
from priorityqueue import PriorityQueue


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
    while sites:
        try:
            s = sites.pop()
        except KeyError:
            break
        
        #Test    
        print (str(counter) + ": " + str(s[0][1]))
        counter += 1
    

    