from math import floor, log2
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt  # Add this import
nx_args={'with_labels':True, 'node_color':"white", 'edgecolors':"black", 'node_size':400}

class Heap:
    def __init__(self, A):
        if isinstance(A, list):
            if A[0] == None:
                self.H = A
                self.n = len(A)-1
            else:
                self.H = [None].extend(A)
                self.n = len(A)
        else:
            self.H = [None, A]
            self.n = 1

    def max(self):
        return self.H[1]

    def ExtractMax(self):
        r = self.H[1]
        self.H[1] = self.H[self.n]
        self.n -= 1
        self.BubbleDown(1)
        return r

    def Insert(self, x):
        self.n=self.n+1
        if self.n >= len(self.H):
            self.H.append(x)
        else:
            self.H[self.n] = x
        self.BubbleUp(self.n)

    def __iadd__(self, number):
        self.Insert(number)
        return self

    def __add__(self, number):
        temp = Heap(self.H.copy())
        temp.Insert(number)
        return temp

    def ChangeKey(self, x, k):
        isBigger = self.H[x] <= k
        
        self.H[x] = k
        if isBigger:
            self.BubbleUp(x)
        else:
            self.BubbleDown(x)

    def __setitem__(self, index, value):
        self.ChangeKey(index, value)

    def IncreaseKey(self, x,k):
        self.ChangeKey(x, k)
    

    def BubbleUp(self, x):
        if x == 1:
            return
        if self.H[x] > self.H[self.parent(x)]:
            temp = self.H[self.parent(x)]
            self.H[self.parent(x)] = self.H[x]
            self.H[x] = temp
            self.BubbleUp(self.parent(x))

    def BubbleDown(self, x):
        if self.left(x) > self.n:
            return
        biggestChild = self.H[self.left(x)]
        biggestChildIndex = self.left(x)
        if self.right(x) <= self.n and self.H[self.right(x)] > self.H[self.left(x)]:
            biggestChild = self.H[self.right(x)]
            biggestChildIndex = self.right(x)
        
        if self.H[x] < biggestChild:
            self.H[biggestChildIndex] = self.H[x]
            self.H[x] = biggestChild
            self.BubbleDown(biggestChildIndex)

    def left(self, x):
        return 2*x

    def right(self, x):
        return 2*x+1

    def parent(self, x):
        return floor(x/2)
    

    def __str__(self):
        result = ""
        count = 1
        while count <= self.n:
            if log2(count) % 1 == 0 and count != 1:
                result+="\n"
            elif count % 2 == 0:
                    result += "| "
            result += f"{self.H[count]}"
            count+=1
        
        result+="\n"
        return result
    

    def print_raw(self):
        print(self.H)

    def is_heap(self):
        for i in range(2, len(self.H)):
            if self.H[i] > self.H[self.parent(i)]:
                return False
        return True

    def __bool__(self):
        return self.is_heap()
    
    

    def __getitem__(self, index):
        return self.H[index]
    

    def __iter__(self):
        temp = self.H.copy()
        temp.remove(None)
        return iter(temp)
    

    def __contains__(self, value):
        return value in self.H

class UnionFind:    

    def __init__(self, n):
        self.sets = [{i} for i in range(n)]
  

    def Union(self, i,j):
        combination = set()
        sets = self.sets.copy()
        for _set in self.sets:
            if i in _set:
                sets.remove(_set)
                combination.update(_set)
            if j in _set:
                sets.remove(_set)
                combination.update(_set)
        sets.append(combination)
        self.sets = sets
  

    def Find(self, i):
        for _set in self.sets:
            if i in _set:
                return _set

    def __repr__(self):
        return self.sets.__repr__()

class QuickUnion():

    def __init__(self, n):
        self.p = []
        for k in range(n):
            self.p.append(k)

    def Union(self, i, j):
        r_i = self.Find(i)
        r_j = self.Find(j)
        if (r_i != r_j):
            self.p[r_i] = r_j

    def dUnion(self, i, j):
        r_i = self.Find(i)
        r_j = self.Find(j)
        if (r_i != r_j):
            self.p[r_i] = r_j
        self.display(text=f"Union ({i}, {j})")

    def Find(self, i):
        while (i != self.p[i]):
            i = self.p[i]
        return i

    def path_compression(self, i):
        path = []
        while (i != self.p[i]):
            path.append(i)
            i = self.p[i]
        for node in path:
            self.p[node] = i
        
        return i

    def dPath_compression(self, i):
        self.path_compression(i)
        self.display(text=f"Path compression ({i})")

    def __repr__(self):
        return self.p.__repr__()

    def display(self, text = ""):
        V = {i for i in range(len(self.p))}
        E = {(i, j) for j,i in enumerate(self.p) if j != i}
        W = nx.DiGraph()
        W.add_nodes_from(V, color="white")
        W.add_edges_from(E)
        plt.clf()
        plt.figure(figsize=(7, 5))  # Adjust the size as needed
        if (text):
            plt.text(0.5, 1.05, text, fontsize=12, horizontalalignment="center", transform=plt.gca().transAxes)
        
        pos = graphviz_layout(W, prog="dot")  # 'dot' is suitable for tree layouts
        nx.draw(W, pos, **nx_args)

class WeightedQuickUnion():

    def __init__(self, n):
        self.p = []
        self.sz = []
        for k in range(n):
            self.p.append(k)
            self.sz.append(1)

    def Union(self, i, j):
        r_i = self.Find(i)
        r_j = self.Find(j)
        if (r_i != r_j):
            if (self.sz[r_i] < self.sz[r_j]):
                self.p[r_i] = r_j
                self.sz[r_j] += self.sz[r_i]
            else:
                self.p[r_j] = r_i
                self.sz[r_i] += self.sz[r_j]
                

    def dUnion(self, i, j):
        self.Union(i, j)
        self.display(text=f"Union ({i}, {j})")

    def Find(self, i):
        while (i != self.p[i]):
            i = self.p[i]
        return i
  

    def __repr__(self):
        return self.p.__repr__()

    def display(self, text = ""):
        V = {i for i in range(len(self.p))}
        E = {(i, j) for j,i in enumerate(self.p) if j != i}
        W = nx.DiGraph()
        W.add_nodes_from(V, color="white")
        W.add_edges_from(E)
        plt.clf()
        plt.figure(figsize=(7, 5))  # Adjust the size as needed
        if (text):
            plt.text(0.5, 1.05, text, fontsize=12, horizontalalignment="center", transform=plt.gca().transAxes)
        
        pos = graphviz_layout(W, prog="dot")  # 'dot' is suitable for tree layouts
        nx.draw(W, pos, **nx_args)

def BFS(adjancency_list : dict, startnode):
    V = set(adjancency_list.keys())
    E = set()
    visitqueue = []
    marked = [startnode]
    
    visitqueue.extend(list((node_to, startnode) for node_to in adjancency_list.get(startnode) if node_to not in marked)) 
    while visitqueue:
        new_node = visitqueue.pop(0)
        to_visit = new_node[0]
        if (to_visit in marked): continue
        from_node = new_node[1]
        E.add((from_node, to_visit))
        visitqueue.extend(list((node_to, to_visit) for node_to in adjancency_list.get(to_visit) if node_to not in marked)) 
        marked.append(to_visit)
    W = nx.DiGraph()
    W.add_nodes_from(V)
    W.add_edges_from(E)
    pos = graphviz_layout(W, prog="dot") # 'dot' is suitable for tree layouts
    nx.draw(W, pos, **nx_args)

def DFS(adjancency_list : dict, startnode):
    V = set(adjancency_list.keys())
    E = set()
    visitqueue = []
    marked = [startnode]
    
    visitqueue.extend(list((node_to, startnode) for node_to in reversed(adjancency_list.get(startnode)) if node_to not in marked)) 
    while visitqueue:
        new_node = visitqueue.pop()
        to_visit = new_node[0]
        if (to_visit in marked): continue
        from_node = new_node[1]
        E.add((from_node, to_visit))
        visitqueue.extend(list((node_to, to_visit) for node_to in reversed(adjancency_list.get(to_visit)) if node_to not in marked)) 
        marked.append(to_visit)
    W = nx.DiGraph()
    W.add_nodes_from(V)
    W.add_edges_from(E)
    pos = graphviz_layout(W, prog="dot") # 'dot' is suitable for tree layouts
    nx.draw(W, pos, **nx_args)


class BinarySearchTree():
    def __init__(self):
        self.root = None

    def insert(self, x, v = "root"):
        if not isinstance(x, DoubleLinkedList):
            x = DoubleLinkedList(x)
        if self.root == None:
            self.root = x
            return
        if (v == "root"): v = self.root
            
        if v == None:
            return x
        x.parent = v
        if x.key <= v.key:
            v.left = self.insert(x, v.left)
        else:
            v.right = self.insert(x, v.right)
        return v

    def dInsert(self, x):
        self.insert(x)
        self.draw()

    def preorder_traversal(self):
        visited = []
        current_node = self.root
        while current_node:
            if current_node not in visited:
                visited.append(current_node)
            if current_node.left and current_node.left not in visited:
                current_node = current_node.left
            elif current_node.right and current_node.right not in visited:
                current_node = current_node.right
            else:
                current_node = current_node.parent
        return list(_visited.key for _visited in visited)

    def draw(self):
        V = set()
        E = set()
        visited = []
        current_node = self.root
        while current_node:
            if current_node not in visited:
                visited.append(current_node)
                V.add(current_node)
            if current_node.left and current_node.left not in visited:
                E.add((current_node, current_node.left))
                current_node = current_node.left
            elif current_node.right and current_node.right not in visited:
                E.add((current_node, current_node.right))
                current_node = current_node.right
            else:
                current_node = current_node.parent
        W = nx.DiGraph()
        W.add_nodes_from(V)
        W.add_edges_from(E)
        labels = {node: node.key for node in V}
        pos = graphviz_layout(W, prog="dot")
        nx.draw(W, pos, labels = labels, **nx_args)
        plt.show()
        return visited
class DoubleLinkedList():

    def __init__(self, key):
        self.parent = None
        self.left = None
        self.right = None
        self.key = key