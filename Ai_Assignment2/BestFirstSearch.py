import heapq
from itertools import count

class Pair:
    def __init__(self, row, col, parent=None):
        self.row = row
        self.col = col
        self.parent = parent

def heuristic(x, y, n):
    return abs(x - (n - 1)) + abs(y - (n - 1))

def reconstruct_path(node):
    path = []
    while node:
        path.append([node.row, node.col])
        node = node.parent
    return path[::-1]  

def best_first_search(grid):
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
    start = Pair(0, 0, None)
    heapq.heappush(pq, (heuristic(0, 0, n), next(counter), start))
    
    visited = [[False] * n for _ in range(n)]
    visited[0][0] = True
    
    while pq:
        _, _, cur = heapq.heappop(pq)
        
        if cur.row == n - 1 and cur.col == n - 1:
            path = reconstruct_path(cur)
            print("Best First Search Path:")
            for p in path:
                print(p, end=" ")
            print("\nLength:", len(path))
            return
        
        for dr, dc in dirs:
            nr, nc = cur.row + dr, cur.col + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and not visited[nr][nc]:
                visited[nr][nc] = True
                heapq.heappush(pq, (heuristic(nr, nc, n), next(counter), Pair(nr, nc, cur)))
    
    print("Path: []")
    print("Length: -1")


if __name__ == "__main__":
    grid = [
        [0, 1, 0],
        [0, 0, 0],
        [1, 0, 0]
    ]
    best_first_search(grid)
