## {{{ http://code.activestate.com/recipes/577540/ (r2)
"""
Binary Search Tree: A sorted collection of values that supports
efficient insertion, deletion, and minimum/maximum value finding.
"""
# Copyright (C) 2008 by Edward Loper
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Modified by Mikko Johansson "(2012) to use with Fortunes's algorithm

# IMPLEMENTATION NOTES:
#
# Internally, we represent tree nodes using Python lists.  These lists
# may either be empty (for empty nodes) or may have length four (for
# non-empty nodes).  The non-empty nodes contain:
#
#     [left_child, right_child, value, sort_key]
#
# Using lists rather than a node class more than doubles the overall
# performance in the benchmarks that I have run.
#
# The sort key is always accessed as node[-1].  This allows us to
# optimize the case where the sort key is identical to the value, by
# encoding such nodes as simply:
#
#     [left_child, right_child, value]
#
# The following constants are used to access the pieces of each search
# node.  If the constant-binding optimization recipe (which can be
# downloaded from <http://code.activestate.com/recipes/277940/>) is
# available, then it is used to replace these constants at
# import-time, increasing the binary search tree efficiency by 3-5%.
import math
from dcel import Hedge

_LEFT = 0
_RIGHT = 1
_PARENT = 2
_VALUE = 3
_SORT_KEY = -1

class BinarySearchTree(object):
    """
    A sorted collection of values that supports efficient insertion,
    deletion, and minimum/maximum value finding.  Values may sorted
    either based on their own value, or based on a key value whose
    value is computed by a key function (specified as an argument to
    the constructor).

    BinarySearchTree allows duplicates -- i.e., a BinarySearchTree may
    contain multiple values that are equal to one another (or multiple
    values with the same key).  The ordering of equal values, or
    values with equal keys, is undefined.
    """
    def __init__(self):
        """
        Create a new empty BST.  If a sort key is specified, then it
        will be used to define the sort order for the BST.  If an
        explicit sort key is not specified, then each value is
        considered its own sort key.
        """
        self._root = [] # = empty node
        self._sort_key = self._get_breakpoint
        self._len = 0 # keep track of how many items we contain.

    #/////////////////////////////////////////////////////////////////
    # Public Methods
    #/////////////////////////////////////////////////////////////////

    def insert(self, item, pq, edge_list):
        """
        Insert the specified item into the BST.
        """
        print ("insert")
        new_value = {'point': item, 'break_point': None, 'pointer': None}
        #print (value['point'])
        #We are only comparing the x value of the site to the breakpoint
        site_x = new_value['point'][0]
        site_y = new_value['point'][1]
        print (site_x)
        # Get the sort key for this value.
        #if self._sort_key is None:
        #    sort_key = value
        #else:
        #    sort_key = self._sort_key(value)
        # Walk down the tree until we find an empty node.
        node = self._root
        traversed = []
        while node and node[_VALUE]['break_point'] is not None:
            #print node
            # Save parent node
            #parent = node
            traversed.append(node)
            #print("breakTEST: " + str(site_x < node[_SORT_KEY](node[_VALUE], site_y)))
            if site_x < node[_SORT_KEY](node[_VALUE], site_y):
                print("left: "),
                print (site_x < node[_SORT_KEY](node[_VALUE], site_y))
                node = node[_LEFT]
            else:
                print("rightright")
                node = node[_RIGHT]
        #split the node
        if node == []:
            print ("root")
            node[:] = [[], [], None, new_value, self._sort_key]
            return
        else:
            traversed.append(node)
        print (" split node")
        #print node
        #delete circle event from queue
        if node[_VALUE]['pointer'] is not None:
            pq.delete(node[_VALUE]['pointer'])
            node[_VALUE]['pointer'] = None
        left_value = node[_VALUE]
#        print ("left_value: " + str(left_value))
        hedge1 = Hedge()
        hedge2 = Hedge()
        hedge1.twin = hedge2
        hedge2.twin = hedge1
        edge_list.hedges.append(hedge1)
        edge_list.hedges.append(hedge2)
#        face1 = Face()
#        face1.wedge = hedge1
        #grand_parent = parent
        node[_VALUE] = {'point': None, 'break_point' : (left_value['point'], item), 'hedge': hedge1}
        print ("left_value: " + str(left_value))
        parent = node
        node = node[_LEFT]
        node[:] = [[], [], parent, left_value, self._sort_key]
        # Save node for circle event check
        left1 = left_value['point']
        left_node = node
#        print ("left_value1: " + str(left1[_VALUE]))
#        print ("left_value1: " + str(left1[_VALUE]['break_point'][0]))
#        print ("left_value1: " + str(left1))
        print ("parent_value: " + str(parent[_VALUE]))

        node = parent[_RIGHT]
        node[:] = [[], [], parent, {'point': None, 'break_point' : (item, left_value['point']), 'hedge': hedge2}, self._sort_key]
        parent = node
#        print ("left_value: " + str(left_value))

        node = node[_LEFT]
        node[:] = [[], [], parent, new_value, self._sort_key]
        # Save node for circle event check
        new_node = node
        node = parent[_RIGHT]
        node[:] = [[], [], parent, left_value, self._sort_key]
        # Save node for circle event check
        right1 = left1
        right_node = node

        # Check for new circle events
        # there has to be a better way to find the triplet
        traversed_right = traversed[:]
        # find the leftmost arc of the triplet
        #print traversed
        n = traversed.pop()
#       print ("left_value1: " + str(left1))
#       print ("new_node: " + str(new_node[_VALUE]['point']))
        print ("before left")
        print (n[_VALUE]['break_point'][0])
        print (left_value['point'])
        while traversed and n[_VALUE]['break_point'][0] == left1:
            #print (n[_VALUE]['break_point'][0])
            print("pop LEFT")
            n = traversed.pop()
            #pass
        if traversed:
            left2 = n[_VALUE]['break_point'][0]
            print ("left_value2: " + str(left2))
            print ("left_value1: " + str(left1))
            print ("new_node: " + str(new_node[_VALUE]['point']))
            circle_event = self._get_circle_event(left2, left1, new_node[_VALUE]['point'], site_y)
            if circle_event is not None:
                circle_event_site = (circle_event[0], (left_node))
                left_node[_VALUE]['radius'] = circle_event[1]
                #print(type(circle_event_site))
                #print (circle_event_site)
                left_node[_VALUE]['pointer'] = circle_event_site
                pq.add(circle_event_site)

        # find the rightmost arc of the triplet
        n = traversed_right.pop()
        # Get rid of the original splitted node
        if traversed_right:
            n = traversed_right.pop()
        print ("before right")
        print (n[_VALUE]['break_point'][1])
        print (left_value['point'])
        while traversed_right and n[_VALUE]['break_point'][1] == right1:
            n = traversed_right.pop()
            #pass
        #if traversed_right:
        if True:
            right2 = n[_VALUE]['break_point'][1]
            print ("right_value2: " + str(right2))
            print ("right_value1: " + str(right1))
            print ("new_node: " + str(new_node[_VALUE]['point']))
#            circle_event = self._get_circle_event(right2, right1, new_node)
            circle_event = self._get_circle_event(new_node[_VALUE]['point'], right1, right2, site_y)
            if circle_event is not None:
                circle_event_site = (circle_event[0], right_node)
                right_node[_VALUE]['radius'] = circle_event[1]
                #print(type(circle_event_site))
                right_node[_VALUE]['pointer'] = circle_event_site
                pq.add(circle_event_site)

        #if(self._get_circle_event(left2, left1, new_node)) is not None:




        #print parent
        # Put the value in the empty node.

#        if site_x is value:
#            node[:] = [[], [], value]
#        else:
#            node[:] = [[], [], value, self._sort_key]
        #self._len += 1
    def pred(self, node):
        print("pred" +str(node[_VALUE]['point']))
        print(node[_PARENT][_VALUE]['break_point'])
        print(node[_PARENT][_VALUE]['point'])
        print(node[_PARENT][_VALUE]['hedge'])
        site = node[_VALUE]['point']
        #print(node[_VALUE]['point'] == node[_PARENT][_VALUE]['break_point'][0])
        #node = node[_PARENT]
        #print(node[_VALUE]['point'] == node[_PARENT][_VALUE]['point'])
        while node[_PARENT][_VALUE]['break_point'][0] == site:
            print("go up" + str(node[_PARENT][_VALUE]['break_point']))
            node = node[_PARENT]
        print("insert" + str(node[_VALUE]['break_point']))
        print("insert" + str(node[_VALUE]['point']))
        node = node[_PARENT][_LEFT]
        #print(node)
        while node[_VALUE]['break_point'] is not None:
            print("go_down" + str(node[_PARENT][_VALUE]['break_point']))
            node = node[_RIGHT]
        #print node[_VALUE]['point']
        print ("return" + str(node[_VALUE]['point']))
        print(node[_PARENT][_VALUE]['break_point'])
        return node

    def succ(self, node):
        print("succ" +str(node[_VALUE]['point']))
        print(node[_PARENT][_VALUE]['break_point'])
        site = node[_VALUE]['point']
        #node = node[_PARENT]
        while node[_PARENT][_VALUE]['break_point'][1] == site:
            print("go up" + str(node[_PARENT][_VALUE]['break_point']))
            node = node[_PARENT]
        node = node[_PARENT][_RIGHT]
        while node[_VALUE]['break_point'] is not None:
            print("go_down" + str(node[_PARENT][_VALUE]['break_point']))
            node = node[_LEFT]
        print ("return" + str(node[_VALUE]['point']))
        return node

    def minimum(self):
        """
        Return the value with the minimum sort key.  If multiple
        values have the same (minimum) sort key, then it is undefined
        which one will be returned.
        """
        return self._extreme_node(_LEFT)[_VALUE]

    def maximum(self):
        """
        Return the value with the maximum sort key.  If multiple values
        have the same (maximum) sort key, then it is undefined which one
        will be returned.
        """
        return self._extreme_node(_RIGHT)[_VALUE]

    def find(self, sort_key):
        """
        Find a value with the given sort key, and return it.  If no such
        value is found, then raise a KeyError.
        """
        return self._find(sort_key)[_VALUE]

    def pop_min(self):
        """
        Return the value with the minimum sort key, and remove that value
        from the BST.  If multiple values have the same (minimum) sort key,
        then it is undefined which one will be returned.
        """
        return self._pop_node(self._extreme_node(_LEFT))

    def pop_max(self):
        """
        Return the value with the maximum sort key, and remove that value
        from the BST.  If multiple values have the same (maximum) sort key,
        then it is undefined which one will be returned.
        """
        return self._pop_node(self._extreme_node(_RIGHT))

    def pop(self, sort_key):
        """
        Find a value with the given sort key, remove it from the BST, and
        return it.  If multiple values have the same sort key, then it is
        undefined which one will be returned.  If no value has the
        specified sort key, then raise a KeyError.
        """
        return self._pop_node(self._find(sort_key))

    def values(self, reverse=False):
        """Generate the values in this BST in sorted order."""
        if reverse:
            return self._iter(_RIGHT, _LEFT)
        else:
            return self._iter(_LEFT, _RIGHT)
    __iter__ = values

    def __len__(self):
        """Return the number of items in this BST"""
        return self._len

    def __nonzero__(self):
        """Return true if this BST is not empty"""
        return self._len>0

    def __repr__(self):
        return '<BST: (%s)>' % ', '.join('%r' % v for v in self)

    def __str__(self):
        return self.pprint()

    def pprint(self, max_depth=10, frame=True, show_key=True):
        """
        Return a pretty-printed string representation of this binary
        search tree.
        """
        t,m,b = self._pprint(self._root, max_depth, show_key)
        lines = t+[m]+b
        if frame:
            width = max(40, max(len(line) for line in lines))
            s = '+-'+'MIN'.rjust(width, '-')+'-+\n'
            s += ''.join('| %s |\n' % line.ljust(width) for line in lines)
            s += '+-'+'MAX'.rjust(width, '-')+'-+\n'
            return s
        else:
            return '\n'.join(lines)

    #/////////////////////////////////////////////////////////////////
    # Private Helper Methods
    #/////////////////////////////////////////////////////////////////

    def _extreme_node(self, side):
        """
        Return the leaf node found by descending the given side of the
        BST (either _LEFT or _RIGHT).
        """
        if not self._root:
            raise IndexError('Empty Binary Search Tree!')
        node = self._root
        # Walk down the specified side of the tree.
        while node[side]:
            node = node[side]
        return node

    def _find(self, sort_key):
        """
        Return a node with the given sort key, or raise KeyError if not found.
        """
        node = self._root
        while node:
            node_key = node[_SORT_KEY]
            if sort_key < node_key:
                node = node[_LEFT]
            elif sort_key > node_key:
                node = node[_RIGHT]
            else:
                return node
        raise KeyError("Key %r not found in BST" % sort_key)

    def _pop_node(self, node):
        """
        Delete the given node, and return its value.
        """
        value = node[_VALUE]
        if node[_LEFT]:
            if node[_RIGHT]:
                # This node has a left child and a right child; find
                # the node's successor, and replace the node's value
                # with its successor's value.  Then replace the
                # sucessor with its right child (the sucessor is
                # guaranteed not to have a left child).  Note: node
                # and successor may not be the same length (3 vs 4)
                # because of the key-equal-to-value optimization; so
                # we have to be a little careful here.
                successor = node[_RIGHT]
                while successor[_LEFT]: successor = successor[_LEFT]
                node[2:] = successor[2:] # copy value & key
                successor[:] = successor[_RIGHT]
            else:
                # This node has a left child only; replace it with
                # that child.
                node[:] = node[_LEFT]
        else:
            if node[_RIGHT]:
                # This node has a right child only; replace it with
                # that child.
                node[:] = node[_RIGHT]
            else:
                # This node has no children; make it empty.
                del node[:]
        self._len -= 1
        return value

    def _iter(self, pre, post):
        # Helper for sorted iterators.
        #   - If (pre,post) = (_LEFT,_RIGHT), then this will generate items
        #     in sorted order.
        #   - If (pre,post) = (_RIGHT,_LEFT), then this will generate items
        #     in reverse-sorted order.
        # We use an iterative implemenation (rather than the recursive one)
        # for efficiency.
        stack = []
        node = self._root
        while stack or node:
            if node: # descending the tree
                stack.append(node)
                node = node[pre]
            else: # ascending the tree
                node = stack.pop()
                yield node[_VALUE]
                node = node[post]

    def _pprint(self, node, max_depth, show_key, spacer=2):
        """
        Returns a (top_lines, mid_line, bot_lines) tuple,
        """
        if max_depth == 0:
            return ([], '- ...', [])
        elif not node:
            return ([], '- EMPTY', [])
        else:
            top_lines = []
            bot_lines = []
            mid_line = '-%r' % node[_VALUE]
            if len(node) > 3: mid_line += ' (key=%r)' % node[_SORT_KEY]
            if node[_LEFT]:
                t,m,b = self._pprint(node[_LEFT], max_depth-1,
                                     show_key, spacer)
                indent = ' '*(len(b)+spacer)
                top_lines += [indent+' '+line for line in t]
                top_lines.append(indent+'/'+m)
                top_lines += [' '*(len(b)-i+spacer-1)+'/'+' '*(i+1)+line
                              for (i, line) in enumerate(b)]
            if node[_RIGHT]:
                t,m,b = self._pprint(node[_RIGHT], max_depth-1,
                                     show_key, spacer)
                indent = ' '*(len(t)+spacer)
                bot_lines += [' '*(i+spacer)+'\\'+' '*(len(t)-i)+line
                              for (i, line) in enumerate(t)]
                bot_lines.append(indent+'\\'+m)
                bot_lines += [indent+' '+line for line in b]
            return (top_lines, mid_line, bot_lines)

    def _get_breakpoint(self, inner_node, yl):
        #debug
        print("_get_breakpoint")
        #print(inner_node)
        #print(inner_node['break_point'][0][0])
        #print(inner_node['break_point'][1][0])
        x1 = inner_node['break_point'][0][0]
        y1 = inner_node['break_point'][0][1]
        x2 = inner_node['break_point'][1][0]
        y2 = inner_node['break_point'][1][1]
#        print (x1)
#        print (y1)
#        print (x2)
#        print (y2)
        # check if y coordinates are equal, then breakpoint in the middle
        if y1 == y2:
            return (x1+x2)/2.0

#        k1 = (y1+yl)/2.0
#        p1 = (y1-yl)/2.0
#        k2 = (y2+yl)/2.0
#        p2 = (y2-yl)/2.0
#        print(type(k1))
#        print (k1)
#        print (p1)
#        print (k2)
#        print (p2)

#        at = p2-p1
#        bt = (2*p1*x2*x2) - (2*p2*x1*x1)
#        ct = (4*p1*p2)*((k1 - k2))
        a = (y2-y1)/2.0
        b = ((x2)*(y1-yl)) - ((x1)*(y2-yl))
        c = ((y1*y1*y2)-(y2*yl*yl)-(y1*y1*yl)-(y2*y2*y1)+(y1*yl*yl)+(y2*y2*yl)+(y2*x1*x1)-(yl*x1*x1)-(y1*x2*x2)+(yl*x2*x2))/2.0
#        print (a)
#        print (b)
#        print (c)
#        print (at)
#        print (bt)
#        print (ct)
        # This is wrong
        #a1 = y1 - yl
        #b1 = 2*x2*a1
        #c1 = a1*(x2*x2 + y2*y2 - yl*yl)
        #a2 = y2 - yl
        #b2 = 2*x1*a2
        #c2 = a2*(x1*x1 + y1*y1 - yl*yl)
        #a = a2-a1
        #b = b1-b2
        #c = c2-c1
        determinant = b*b - 4 *a*c
        bp1 = (-b + math.sqrt(determinant))/(2*a)
        bp2 = (-b - math.sqrt(determinant))/(2*a)
#       determinantt = bt*bt - 4 *at*ct
#       bp1t = (-bt + math.sqrt(determinantt))/(2*at)
#       bp2t = (-bt - math.sqrt(determinantt))/(2*at)
#       print (bp1)
#       print (bp2)
#       print (bp1t)
#       print (bp2t)
        #print(max(bp1,bp2))
        if y1 < y2:
            print("max" + str(max(bp1,bp2)))
            return max(bp1, bp2)
        else:
            print("min: " + str(min(bp1,bp2)))
            return min(bp1,bp2)
#        return ((inner_node['break_point'][0][0] - inner_node['break_point'][1][0])/2)

    #Calculate possible circle event, if found return lowest point else None
    def _get_circle_event(self, site1, site2, site3, ly):
#        x1 = site1['point'][0][0]
#        y1 = site1['point'][0][1]
#        x2 = site2['point'][0][0]
#        y2 = site2['point'][0][1]
#        x3 = site3['point'][0][0]
#        y3 = site3['point'][0][1]
#        print site1
        print site2[0]
        print site3[0]
        print site1[0]
        x1 = site1[0]
        y1 = site1[1]
        x2 = site2[0]
        y2 = site2[1]
        x3 = site3[0]
        y3 = site3[1]
        if x1 == x2 and x2 == x3:
            return None
        if y1 == y2 and y2 == y3:
            return None
        a = x2*x2 - x1*x1 + y2*y2 - y1*y1
        b = x3*x3 - x2*x2 + y3*y3 - y2*y2
        print ("CIRCLE: a:" + str(a) + ": b: " + str(b))
        dx1 = x1 - x2
        dx2 = x3 - x2
        dy1 = y2 - y1
        dy2 = y3 - y2
        print ("dx1: " + str(dx1) + " dx2: " + str(dx2) + " dy1: " + str(dy1) + " dy2: " + str(dy2))

        k = (a + ((2*dx1*b)/(2*dx2))) * (1/(2*dy1) - ((2*dx2)/(4*dx1*dy2)))
        h = (b + 2*dy2*k)/(2*dx2)
        r = math.sqrt((math.pow(x1-h, 2) + math.pow(y1-k, 2)))
        print ("k: " + str(k) + " h: " + str(h) + " r: " + str(r) + " h-r: " + str(h-r))
        # Check converge (www.mail-archive.com/algogeeks@googlegroups.com/msg02478.html)
        if ((x2-x1)*(y3-y1)) - ((x3-x1)*(y2-y1)) > 0 and ly > h-r:
            print ("converge: " + str(k) + ", " + str(h-r))
            return ((k, h-r), r)
        else:
            return None



        pass
try:
    # Try to use the python recipe:
    # <http://code.activestate.com/recipes/277940/>
    # This will only work if that recipe has been saved a
    # "optimize_constants.py".
    from optimize_constants import bind_all
    bind_all(BinarySearchTree)
except:
    pass
## end of http://code.activestate.com/recipes/577540/ }}}
