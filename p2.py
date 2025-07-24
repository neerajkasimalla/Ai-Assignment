from itertools import combinations

class State:
    def __init__(self, left, right, is_umbrella_left, time):
        self.left = set(left)
        self.right = set(right)
        self.is_umbrella_left = is_umbrella_left
        self.time = time

    def __hash__(self):
        return hash((frozenset(self.left), frozenset(self.right), self.is_umbrella_left, self.time))

    def __eq__(self, other):
        return (self.left == other.left and
                self.right == other.right and
                self.is_umbrella_left == other.is_umbrella_left and
                self.time == other.time)

    def __str__(self):
        return f"L: {sorted(self.left)} | R: {sorted(self.right)} | Umbrella: {'L' if self.is_umbrella_left else 'R'} | Time: {self.time} min"

    def goalTest(self):
        return len(self.left) == 0 and self.time <= 60

    def moveGen(self, times):
        moves = []
        if self.is_umbrella_left:
            # Move 2 people from left to right
            for pair in combinations(self.left, 2):
                time_taken = max(times[pair[0]], times[pair[1]])
                new_left = self.left - set(pair)
                new_right = self.right | set(pair)
                new_time = self.time + time_taken
                new_state = State(new_left, new_right, False, new_time)
                moves.append(new_state)
        else:
            # Return 1 person from right to left
            for person in self.right:
                time_taken = times[person]
                new_left = self.left | {person}
                new_right = self.right - {person}
                new_time = self.time + time_taken
                new_state = State(new_left, new_right, True, new_time)
                moves.append(new_state)
        return moves


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
    open_nodes = [node for node, _ in OPEN]
    closed_nodes = [node for node, _ in CLOSED]
    new_nodes = [c for c in children if c not in open_nodes and c not in closed_nodes]
    return new_nodes


def bfs(start, times):
    OPEN = [(start, None)]
    CLOSED = []
    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair

        if N.goalTest():
            print("Goal found within time limit!")
            path = reconstructPath(node_pair, CLOSED)
            path.reverse()
            for node in path:
                print(node)
            return

        CLOSED.append(node_pair)
        children = N.moveGen(times)
        new_nodes = removeSeen(children, OPEN, CLOSED)
        new_pairs = [(node, N) for node in new_nodes if node.time <= 60]
        OPEN += new_pairs


def dfs(start, times):
    OPEN = [(start, None)]
    CLOSED = []
    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair

        if N.goalTest():
            print("Goal found within time limit!")
            path = reconstructPath(node_pair, CLOSED)
            path.reverse()
            for node in path:
                print(node)
            return

        CLOSED.append(node_pair)
        children = N.moveGen(times)
        new_nodes = removeSeen(children, OPEN, CLOSED)
        new_pairs = [(node, N) for node in new_nodes if node.time <= 60]
        OPEN = new_pairs + OPEN


# Time map
times = {
    "Amogh": 5,
    "Ameya": 10,
    "Grandmother": 20,
    "Grandfather": 25
}

# Initial state
start_state = State(
    left={"Amogh", "Ameya", "Grandmother", "Grandfather"},
    right=set(),
    is_umbrella_left=True,
    time=0
)

print("BFS")
bfs(start_state, times)

print("\nDFS")
dfs(start_state, times)
