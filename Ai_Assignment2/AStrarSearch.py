import heapq
from itertools import count

class Node:
    def __init__(self, row, col, g, parent=None):
        self.row = row
        self.col = col
        self.g = g  
        self.parent = parent

def heuristic(x, y, n):
    return abs(x - (n - 1)) + abs(y - (n - 1))

def reconstruct_path(node):
    path = []
    while node:
        path.append([node.row, node.col])
        node = node.parent
    return path[::-1]  

def a_star_search(grid):
    n = len(grid)
    
    if grid[0][0] != 0 or grid[n - 1][n - 1] != 0:
        print("Path: []")
        print("Length: -1")
        return
    
    dirs = [
        [-1,-1], [-1,0], [-1,1],
        [0,-1],          [0,1],
        [1,-1], [1,0],   [1,1]
    ]
    
    pq = []
    counter = count()  
    start = Node(0, 0, 1, None)
    heapq.heappush(pq, (start.g + heuristic(0, 0, n), next(counter), start))
    
    visited = [[False] * n for _ in range(n)]
    visited[0][0] = True
    
    while pq:
        _, _, cur = heapq.heappop(pq)
        
        if cur.row == n - 1 and cur.col == n - 1:
            path = reconstruct_path(cur)
            print("A* Search Path:")
            for p in path:
                print(p, end=" ")
            print("\nLength:", cur.g)
            return
        
        for dr, dc in dirs:
            nr, nc = cur.row + dr, cur.col + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and not visited[nr][nc]:
                visited[nr][nc] = True
                new_node = Node(nr, nc, cur.g + 1, cur)
                f = new_node.g + heuristic(nr, nc, n)
                heapq.heappush(pq, (f, next(counter), new_node))
    
    print("Path: []")
    print("Length: -1")


if __name__ == "__main__":
    grid = [
        [0, 1, 0],
        [0, 0, 0],
        [1, 0, 0]
    ]
    a_star_search(grid)
