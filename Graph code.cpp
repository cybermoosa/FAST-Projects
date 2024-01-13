#include <iostream>

#define MAX_VERTICES 100 // Maximum number of vertices in the graph

class Graph {
    int V; // Number of vertices
    int adjMatrix[MAX_VERTICES][MAX_VERTICES]; // Adjacency matrix representation
    int adjList[MAX_VERTICES][MAX_VERTICES]; // Adjacency list representation

public:
    Graph(int vertices) {
        V=vertices;
        // Initialize the adjacency matrix and adjacency list with zeros
        for (int i=0; i<V; ++i) {
            for (int j=0; j<V; ++j) {
                adjMatrix[i][j]=0;
                adjList[i][j]=0;
            }
        }
    }

    // Function to add an edge between two vertices
    void addEdge(int v, int w) {
        adjMatrix[v][w]=1;
        adjMatrix[w][v]=1; // For undirected graph, mark edges in both directions

        // Update adjacency list
        if (adjList[v][0]==0) {
            adjList[v][0]=1;
            adjList[v][1]=w;
        } else {
            int i=1;
            while (adjList[v][i]!=0) {
                ++i;
            }
            adjList[v][i]=w;
        }

        if (adjList[w][0]==0) {
            adjList[w][0]=1;
            adjList[w][1]=v;
        } else {
            int i=1;
            while (adjList[w][i]!=0) {
                ++i;
            }
            adjList[w][i]=v;
        }
    }

    // Function to print the adjacency matrix
    void printAdjacencyMatrix() {
        for (int i=0; i<V; ++i) {
            cout<<"Adjacency matrix of vertex "<<i<<": ";
            for (int j=0; j<V; ++j) {
                cout<<adjMatrix[i][j]<<" ";
            }
            cout<<endl;
        }
    }

    // Function to print the adjacency list
    void printAdjacencyList() {
        for (int i=0; i<V; ++i) {
            cout<<"Adjacency list of vertex "<<i<<": ";
            for (int j=1; j<MAX_VERTICES; ++j) {
                if (adjList[i][j]!=0) {
                    cout<<adjList[i][j]<<" ";
                } else {
                    break;
                }
            }
            cout<<endl;
        }
    }
};

int main() {
    // Create a graph with 5 vertices
    Graph graph(5);

    // Add edges
    graph.addEdge(0, 1);
    graph.addEdge(0, 4);
    graph.addEdge(1, 2);
    graph.addEdge(1, 3);
    graph.addEdge(1, 4);
    graph.addEdge(2, 3);
    graph.addEdge(3, 4);

    // Print the adjacency matrix and adjacency list
    graph.printAdjacencyMatrix();
    cout<<endl;
    graph.printAdjacencyList();

    return 0;
}
