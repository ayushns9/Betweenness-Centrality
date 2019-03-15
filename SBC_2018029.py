from copy import deepcopy
import re
import itertools
import math

ROLLNUM_REGEX = "201[0-9]{4}"

class Graph(object):
    name = "AYUSH GOEL"
    email = "ayush18029@iiitd.ac.in"
    roll_num = "2018029"

    def __init__ (self, vertices, edges):
        """
            Contructor for the class graph!
            Constructs the object for the class.
        """

        self.vertices = vertices
        
        ordered_edges = list(map(lambda x: (min(x), max(x)), edges))
        
        self.edges    = ordered_edges
        
        self.validate()

    def validate(self):
        """
            This function checks
            for the validity of
            the inputs.
            It raises an error otherwise.
        """
        if (not isinstance(self.name, str)) or self.name == "":
            st="Name can't be empty"
            raise Exception(st)

        if (not isinstance(self.email, str)) or self.email == "":
            st="Email can't be empty"
            raise Exception(st)

        if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
            st="Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}"
            raise Exception(st.format(self.roll_num))

        if not all([isinstance(node, int) for node in self.vertices]):
            st="All vertices should be integers"
            raise Exception(st)

        elif len(self.vertices) != len(set(self.vertices)):
            duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])
            st="Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}"
            raise Exception(st.format(vertices, duplicate_vertices))

        edge_vertices = list(set(itertools.chain(*self.edges)))

        if not all([node in self.vertices for node in edge_vertices]):
            st="All endpoints of edges must belong in vertices"
            raise Exception(st)

        if len(self.edges) != len(set(self.edges)):
            duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])
            st="Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}"
            raise Exception(st.format(edges, duplicate_edges))

    def isadjto(self,a,b):
        """
            This funtion checks if two nodes are 
            adjacent to 
            each other or not.
            Returns true if they are
            adjacent and false
            otherwise.
        """
        if((a,b) in self.edges or (b,a) in self.edges):
            return True
        else:
            return False

    def allpaths(self,start_node):
        """
            This function takes a start node 
            as an argument and returns
            all the possible paths for all
            the possible end nodes.
            The paths are returned as 
            lists.
        """
        paths=[[start_node]]
        a=len(self.vertices)
        b=len(self.vertices)
        c=len(self.vertices)
        while(a>0):
            for j in self.vertices:
                for i in paths:
                    if(self.isadjto(i[-1],j) and j not in i and i+[j] not in paths):
                        paths.append(i+[j])
            a-=1
        return paths

    def min_dist(self, start_node, end_node):
        """
            This function takes start node 
            and end node as arguments.
            It returns the minimum distance between
            the two nodes using all the paths retrieved
            from the allpaths function.
            The minimum distance is returned as integer.
        """
        l=[]
        for i in self.allpaths(start_node):
            if(i[-1]==end_node):
                l.append(i)
        min1=len(self.vertices)+1
        for i in l:
            if(len(i)<min1):
                min1=len(i)

        return min1-1


    def all_shortest_paths(self,start_node, end_node):
        """
            This function takes start node and
            end node as argumenst and returns a list
            of all the shortest path between
            the two nodes.
        """

        a=self.allpaths(start_node)
        l=[]
        for i in a:
            if(i[-1]==end_node):
                l.append(i)
        min1=len(self.vertices)+1
        for i in l:
            if(len(i)<min1):
                min1=len(i)
        q=[]
        for i in l:
            if(len(i)==min1):
                q.append(i)
        return q

    def betweenness_centrality(self, node):
        """
            This function takes a node as an argument
            and returns the betweeness centrality
            for the given node in the graph.

        """
        li=[]
        for i in self.vertices:
            if(i!=node):
                for j in self.vertices:
                    if(i!=j and j!=node):
                        a=self.all_shortest_paths(i,j)
                        x=len(a)
                        y=0
                        for o in a:
                            for u in o:
                                if(u==node):
                                    y+=1
                        li.append(y/x)
        return sum(li)/2

    def sta(self,node):
        """
            This function takes a node as an argument and
            returns the standard betweeness centrality for the
            node in the graph.
            It also round it to 4 decimal places.
        """
        n=len(self.vertices)
        return round(2*self.betweenness_centrality(node)/((n-1)*(n-2)),4)
        

    def top_k_betweenness_centrality(self):
        """
            This function takes no arguments.
            It returns the nodes having the highest 
            standard betweeness centrality along with
            its bc.
        """

        ans=[]

        yoyo=[]
        for u in self.vertices:
            yoyo.append([self.sta(u),u])
        qwerty=yoyo[0][0]
        for i in yoyo:
            if(qwerty<i[0]):
                qwerty=i[0]

        for i in yoyo:
            if(i[0]==qwerty):
                ans.append(i)

        return ans        


if __name__ == "__main__":
    """
    ***Main function***
    """
    vertices = [1, 2, 3, 4, 5, 6]
    edges    = [(1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (4, 5), (4, 6)]
    graph = Graph(vertices, edges)
    print(graph.top_k_betweenness_centrality())
    