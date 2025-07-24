class State:
    def __init__(self, config):
        self.config = config  # List like ['E','E','E','_','W','W','W']

    def __eq__(self, other):
        return self.config == other.config

    def __hash__(self):
        return hash(tuple(self.config))

    def __str__(self):
        return ''.join(self.config)

    def goalTest(self):
        return self.config == ['W', 'W', 'W', '_', 'E', 'E', 'E']

    def moveGen(self):
        children = []
        for i in range(len(self.config)):
            if self.config[i] == '_':
                # Move E from left to right
                if i-1 >= 0 and self.config[i-1] == 'E':
                    new_config = self.config.copy()
                    new_config[i], new_config[i-1] = new_config[i-1], new_config[i]
                    children.append(State(new_config))

                if i-2 >= 0 and self.config[i-2] == 'E' and self.config[i-1] == 'W':
                    new_config = self.config.copy()
                    new_config[i], new_config[i-2] = new_config[i-2], new_config[i]
                    children.append(State(new_config))

                # Move W from right to left
                if i+1 < len(self.config) and self.config[i+1] == 'W':
                    new_config = self.config.copy()
                    new_config[i], new_config[i+1] = new_config[i+1], new_config[i]
                    children.append(State(new_config))

                if i+2 < len(self.config) and self.config[i+2] == 'W' and self.config[i+1] == 'E':
                    new_config = self.config.copy()
                    new_config[i], new_config[i+2] = new_config[i+2], new_config[i]
                    children.append(State(new_config))
        return children


def reconstructPath(goal_node_pair, CLOSED):
    parent_map = {}
    for node, parent in CLOSED:
        parent_map[node] = parent

    path = []
    goal_node, parent = goal_node_pair
    path.append(goal_node)
    while parent is not None:
        path.append(parent)
        parent = parent_map[parent]

    return path


def removeSeen(children, OPEN, CLOSED):
    open_nodes = [node for node, parent in OPEN]
    closed_nodes = [node for node, parent in CLOSED]
    new_nodes = [c for c in children if c not in open_nodes and c not in closed_nodes]
    return new_nodes


def bfs(start):
    OPEN = [(start, None)]
    CLOSED = []
    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair

        if N.goalTest():
            print("Goal is found")
            path = reconstructPath(node_pair, CLOSED)
            path.reverse()
            for node in path:
                print(node)
            return
        else:
            CLOSED.append(node_pair)
            children = N.moveGen()
            new_nodes = removeSeen(children, OPEN, CLOSED)
            new_pairs = [(node, N) for node in new_nodes]
            OPEN += new_pairs
    return []


def dfs(start):
    OPEN = [(start, None)]
    CLOSED = []
    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair

        if N.goalTest():
            print("Goal is found")
            path = reconstructPath(node_pair, CLOSED)
            path.reverse()
            for node in path:
                print(node)
            return
        else:
            CLOSED.append(node_pair)
            children = N.moveGen()
            new_nodes = removeSeen(children, OPEN, CLOSED)
            new_pairs = [(node, N) for node in new_nodes]
            OPEN = new_pairs + OPEN
    return []
    

start_config = ['E', 'E', 'E', '_', 'W', 'W', 'W']
start_state = State(start_config)

print("BFS")
bfs(start_state)

print("\nDFS")
dfs(start_state)
