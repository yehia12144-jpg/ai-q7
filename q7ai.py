from collections import deque
import heapq
import sys

MAZE_TEXT = """
S.#...#...
#.#.#..#.#
....#.#...
.#.#..#.#.
.#...#..#.
..##.#.#..
#..#...#.#
.#...#....
.###..###.
.....#...E
"""

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def parse_maze(text):
    grid = [list(row) for row in text.strip().splitlines()]
    start = end = None
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "S":
                start = (r, c)
            elif ch == "E":
                end = (r, c)
    if start is None or end is None:
        raise ValueError("Maze must contain both S and E")
    return grid, start, end


def get_neighbors(grid, cell):
    rows, cols = len(grid), len(grid[0])
    r, c = cell
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
            yield (nr, nc)


def reconstruct_path(parent, end):
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1]


def bfs(grid, start, end):
    queue = deque([start])
    parent = {start: None}
    nodes_expanded = 0

    while queue:
        current = queue.popleft()
        nodes_expanded += 1

        if current == end:
            return {
                "path": reconstruct_path(parent, end),
                "nodes_expanded": nodes_expanded,
                "visited": len(parent),
            }

        for nb in get_neighbors(grid, current):
            if nb not in parent:
                parent[nb] = current
                queue.append(nb)

    return {"path": None, "nodes_expanded": nodes_expanded, "visited": len(parent)}


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(grid, start, end, heuristic=manhattan):
    counter = 0
    open_heap = [(heuristic(start, end), 0, counter, start)]
    g_cost = {start: 0}
    parent = {start: None}
    closed = set()
    nodes_expanded = 0

    while open_heap:
        f, g, _, current = heapq.heappop(open_heap)

        if current in closed:
            continue
        closed.add(current)
        nodes_expanded += 1

        if current == end:
            return {
                "path": reconstruct_path(parent, end),
                "nodes_expanded": nodes_expanded,
                "visited": len(g_cost),
            }

        for nb in get_neighbors(grid, current):
            new_g = g + 1
            if nb not in g_cost or new_g < g_cost[nb]:
                g_cost[nb] = new_g
                parent[nb] = current
                counter += 1
                heapq.heappush(open_heap, (new_g + heuristic(nb, end), new_g, counter, nb))

    return {"path": None, "nodes_expanded": nodes_expanded, "visited": len(g_cost)}


def print_path(grid, path, title):
    on_path = set(path)
    width = len(grid[0]) * 2
    print(f"{title} ({len(path) - 1} moves)")
    print("  ┌" + "─" * width + "┐")
    for r, row in enumerate(grid):
        line = ""
        for c, ch in enumerate(row):
            if ch == "S":
                line += "S "
            elif ch == "E":
                line += "E "
            elif ch == "#":
                line += "██"
            elif (r, c) in on_path:
                line += "● "
            else:
                line += "  "
        print("  │" + line + "│")
    print("  └" + "─" * width + "┘")
    
    # Print the route walk line wrapped neatly across lines
    steps = [f"({r},{c})" for r, c in path]
    for i in range(0, len(steps), 7):
        prefix = "  Path: " if i == 0 else "        "
        print(prefix + " → ".join(steps[i:i + 7]) + (" →" if i + 7 < len(steps) else ""))
    print()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        
    grid, start, end = parse_maze(MAZE_TEXT)

    bfs_res = bfs(grid, start, end)
    astar_res = a_star(grid, start, end)

    print_path(grid, bfs_res["path"], "BFS Path (Walk Route)")
    print_path(grid, astar_res["path"], "A* Path (Walk Route)")

    col_w1, col_w2, col_w3 = 18, 26, 26
    print("=" * 70)
    print(f"{'':<{col_w1}}{'BFS':<{col_w2}}{'A*':<{col_w3}}")
    print("-" * 70)
    print(f"{'Path length':<{col_w1}}{str(len(bfs_res['path']) - 1) + ' steps':<{col_w2}}{str(len(astar_res['path']) - 1) + ' steps':<{col_w3}}")
    print(f"{'Time complexity':<{col_w1}}{'O(b^d) = O(V + E)':<{col_w2}}{'O(b^d) = O(E log V)':<{col_w3}}")
    print(f"{'  nodes expanded':<{col_w1}}{bfs_res['nodes_expanded']:<{col_w2}}{astar_res['nodes_expanded']:<{col_w3}}")
    print(f"{'Space complexity':<{col_w1}}{'O(b^d) = O(V)':<{col_w2}}{'O(b^d) = O(V)':<{col_w3}}")
    print(f"{'  nodes stored':<{col_w1}}{bfs_res['visited']:<{col_w2}}{astar_res['visited']:<{col_w3}}")
    print("=" * 70)


if __name__ == "__main__":
    main()