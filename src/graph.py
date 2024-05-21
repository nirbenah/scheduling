class IndirectedGraph:
    def __init__(self):
        self.graph = {}
        self.degrees = {}
        self.degree_one_nodes = []

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = set()
            self.degrees[vertex] = 0

    def add_edge(self, vertex1, vertex2):
        self.add_vertex(vertex1)
        self.add_vertex(vertex2)
        self.graph[vertex1].add(vertex2)
        self.graph[vertex2].add(vertex1)
        self.degrees[vertex1] += 1
        self.degrees[vertex2] += 1
        if self.degrees[vertex1] == 1:
            self.degree_one_nodes.append(vertex1)
        elif self.degrees[vertex1] == 2 and vertex1 in self.degree_one_nodes:
            self.degree_one_nodes.remove(vertex1)
        if self.degrees[vertex2] == 1:
            self.degree_one_nodes.append(vertex2)
        elif self.degrees[vertex2] == 2 and vertex2 in self.degree_one_nodes:
            self.degree_one_nodes.remove(vertex2)

    def remove_vertex(self, vertex):
        # problem in updating degree_one_nodes after remove 2 verteces in a row
        #for now we don't fix, because we use only the remove_edge
        if vertex in self.graph:
            if self.degrees[vertex] == 1:
                self.degree_one_nodes.remove(vertex)
            for v in self.graph[vertex]:
                self.graph[v].remove(vertex)
                self.degrees[v] -= 1
                if self.degrees[v] == 1 and v not in self.degree_one_nodes:
                    self.degree_one_nodes.append(v)
            del self.graph[vertex]
            del self.degrees[vertex]

    def remove_edge(self, vertex1, vertex2):
        if vertex1 in self.graph and vertex2 in self.graph[vertex1]:
            self.graph[vertex1].remove(vertex2)
            self.graph[vertex2].remove(vertex1)
            self.degrees[vertex1] -= 1
            self.degrees[vertex2] -= 1
            if self.degrees[vertex1] == 0 and vertex1 in self.degree_one_nodes:
                self.degree_one_nodes.remove(vertex1)
                self.remove_vertex(vertex1)
            elif self.degrees[vertex1] == 1 and vertex1 not in self.degree_one_nodes:
                self.degree_one_nodes.append(vertex1)
            if self.degrees[vertex2] == 0 and vertex2 in self.degree_one_nodes:
                self.degree_one_nodes.remove(vertex2)
                self.remove_vertex(vertex2)
            elif self.degrees[vertex2] == 1 and vertex2 not in self.degree_one_nodes:
                self.degree_one_nodes.append(vertex2)

    def get_neighbors(self, vertex):
        if vertex in self.graph:
            return list(self.graph[vertex])
        else:
            return []

    def get_vertices(self):
        return list(self.graph.keys())

    def get_degree(self, vertex):
        return self.degrees.get(vertex, 0)

    def get_vertices_with_degree_one(self):
        return self.degree_one_nodes

    def printgraph(self):
        output = "IndirectedGraph:\n"
        for vertex in self.graph:
            output += f"{vertex}: "
            output += ", ".join(self.graph[vertex]) + "\n"
        return output
    
    
    def maximum_matching(self):
        matchings = dict()
        if self.graph and not self.degree_one_nodes:
            vertex = next(iter(self.graph))
            vertex_neighbors_set = self.graph[vertex]
            vertex_neighbor = next(iter(vertex_neighbors_set))
            self.remove_edge(vertex, vertex_neighbor)
        while self.degree_one_nodes:
            vertex = self.degree_one_nodes[0]
            #print("****")
            #print(vertex)
            #print(next(iter(self.graph[vertex])))
            vertex_father = next(iter(self.graph[vertex]))
            self.remove_edge(vertex, vertex_father)
            if vertex[0] == 'j':
                matchings[vertex] = vertex_father
            elif vertex_father[0] == 'j':
                matchings[vertex_father] = vertex
            else:
                assert 1==0
                print("---------------Error----------------")
            if self.graph and not self.degree_one_nodes:
                vertex = next(iter(self.graph))
                vertex_neighbors_set = self.graph[vertex]
                vertex_neighbor = next(iter(vertex_neighbors_set))
                self.remove_edge(vertex, vertex_neighbor)
        return matchings