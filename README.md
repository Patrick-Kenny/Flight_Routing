# Flight_Routing
Program to test out Networkx node traversal via flight routing
By Patrick Kenny

Commands taken from file read into stdin.

ADD:
	Adds new route to graph.
	In the form of "ADD \<origin>,\<destination>,\<distance>,\<duration>".

QUERY:
	Displays possible paths from origin to destination up to the MAX_ROUTES
	In the form of "QUERY \<origin>,\<destination>".
