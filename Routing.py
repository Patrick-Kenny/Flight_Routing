# Flight Routing
# By Patrick Kenny

import sys
import networkx as nx
from itertools import islice


MAX_ROUTES = 5 # Max number of routes to display in query


# Adds or updates given route in the graph

def Add_Route(rMap, args):

    args = args.split(',')

    if len(args) != 4: # Verifies appropriate number of arguments
        Error(["ADD"] + args)
        return

    origin = str(args[0]).strip()
    destination = str(args[1]).strip()
    try:    # Ensures that distance and duration are numbers
        distance = float(args[2])
        duration = float(args[3])
        value = round(((distance * 15) + (duration * 30)),2)
    except:
        Error(["ADD"] + args)
        return

    # Add origin node if doesn't exist
    if not rMap.has_node(origin):
        rMap.add_node(origin)

    # Add destination node if doesn't exist
    if not rMap.has_node(destination):
        rMap.add_node(destination)

    # Update route if it exists, otherwise create route
    try:
        rMap[origin][destination]['dist'] = distance
        rMap[origin][destination]['dur'] = duration
        rMap[origin][destination]['cost'] = value
    except:
        rMap.add_edge(origin, destination, dist = distance, dur = duration, cost = value)

    print("EDGE " + ",".join(args), file = sys.stdout)

    return


# Queries graph to find path between origin and destination

def Query_Route(rMap, args):
    
    args = args.split(',')
    
    if len(args) != 2: # Verifies appropriate number of arguments
        Error(["QUERY"] + args)
        return

    origin = str(args[0]).strip()
    destination = str(args[1]).strip()

    # Check Locations as valid, reachable nodes
    if not Check_Route(rMap, origin, destination):
        Error(["QUERY"] + args)
        return

    # Find all paths from origin to destination
    paths = list(islice(nx.shortest_simple_paths(rMap, origin, destination, weight = 'cost'), MAX_ROUTES))

    print("QUERY " + origin + "," + destination, file = sys.stdout)

    for leg in paths:
        cost = Get_Cost(rMap, leg)
        print("PATH {:.2f},".format(cost) + ",".join(leg), file = sys.stdout)   

    return


# Describes command as malformed if issue is detected

def Error(line):
    print("MALFORMED " + ','.join(line).strip(), file = sys.stderr)


# Checks to ensure that both origin and destination are in the graph
# and that the destination is reachable from the origin

def Check_Route(rMap, o, d):
    return o in rMap and d in rMap and d in nx.descendants(rMap, o)


# Calculates the cost of a given path

def Get_Cost(rMap, path):
    
    cost = 0
    for i in range(len(path)-1):
        cost += rMap[path[i]][path[i+1]]['cost']

    return cost


if __name__ == '__main__':
    routeMap = nx.DiGraph()
    for line in sys.stdin:
        args = line.split(' ', 1)

        if len(args) != 2:
            Error(args)
            continue
        
        command = args[0]
        arg = args[1].rstrip()

        if command == "ADD": # e.g. ADD Las Vegas,New York,2248,300
            Add_Route(routeMap, arg)
        elif command == "QUERY": # e.g. QUERY Las Vegas, New York
            Query_Route(routeMap, arg)
        else:
            Error(args)