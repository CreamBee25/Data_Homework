"""
图的遍历 — 作业解答
===================
给定一个 5 顶点无向图, 从 A 出发:
- 写出 DFS (深度优先搜索) 遍历序列
- 写出 BFS (广度优先搜索) 遍历序列

图结构:
          A
         / \
        B   C
        |  /|
        | / |
        D---E

提示: 每个顶点的邻接点按字母顺序访问
"""

from collections import deque

# ============================================================
# 图的定义
# ============================================================
vertices = ['A', 'B', 'C', 'D', 'E']
edges = [
    ('A', 'B'),
    ('A', 'C'),
    ('B', 'D'),
    ('C', 'D'),
    ('C', 'E'),
    ('D', 'E'),
]


def build_adjacency_list(vertices, edges):
    """
    构建邻接表, 邻居按字母顺序排序
    时间复杂度: O(n + e log e), 空间复杂度: O(n + e)
    """
    adj = {v: [] for v in vertices}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    # 每个顶点的邻居按字母排序 (符合题目要求)
    for v in vertices:
        adj[v].sort()
    return adj


# ============================================================
# 1. DFS 深度优先搜索
# ============================================================
def dfs(adj, start):
    """
    深度优先搜索 (Depth-First Search)

    核心思想: 从起点出发, 一路走到底, 无路可走时回溯再探索

    实现方式: 递归 (隐式使用系统栈)
    - 时间复杂度: O(n + e)  — 每个顶点和每条边访问一次
    - 空间复杂度: O(n)      — visited 数组 + 递归栈深度

    参数:
        adj:   邻接表
        start: 起始顶点
    返回:
        遍历序列 (list)
    """
    visited = set()   # 记录已访问的顶点
    sequence = []     # 遍历序列

    def _dfs_recursive(v):
        """递归访问顶点 v"""
        visited.add(v)           # 标记当前顶点为已访问
        sequence.append(v)       # 记录访问顺序
        for neighbor in adj[v]:  # 按字母顺序遍历邻居
            if neighbor not in visited:
                _dfs_recursive(neighbor)

    _dfs_recursive(start)
    return sequence


def dfs_iterative(adj, start):
    """
    DFS 迭代实现 (显式使用栈)

    与递归版本的区别:
    - 显式维护一个栈, 模拟递归调用
    - 遍历顺序可能与递归不同 (取决于邻居入栈顺序)
    - 要保证与递归顺序一致, 需要将邻居按字母逆序入栈
      (因为栈是后进先出, 字母序靠后的先入栈,
       字母序靠前的就会先被处理)

    时间复杂度: O(n + e), 空间复杂度: O(n)
    """
    visited = set()
    sequence = []
    # 栈: 存放待访问的顶点
    stack = [start]

    while stack:
        v = stack.pop()                     # 弹出栈顶 (后进先出)
        if v in visited:
            continue
        visited.add(v)
        sequence.append(v)

        # 邻居按字母逆序入栈 (字母靠后的先入栈, 会被后处理)
        # 这样字母靠前的会先出栈, 保证与递归顺序一致
        for neighbor in reversed(adj[v]):
            if neighbor not in visited:
                stack.append(neighbor)

    return sequence


# ============================================================
# 2. BFS 广度优先搜索
# ============================================================
def bfs(adj, start):
    """
    广度优先搜索 (Breadth-First Search)

    核心思想: 层层推进, 先访问起点所有邻居, 再访问邻居的邻居...

    实现方式: 使用队列 (先进先出 FIFO)
    - 时间复杂度: O(n + e)  — 每个顶点和每条边访问一次
    - 空间复杂度: O(n)      — visited 数组 + 队列

    参数:
        adj:   邻接表
        start: 起始顶点
    返回:
        遍历序列 (list)
    """
    visited = set()
    sequence = []
    # 队列: 存放待访问的顶点 (先进先出)
    queue = deque([start])
    visited.add(start)  # 入队时立即标记, 防止重复入队

    while queue:
        v = queue.popleft()               # 弹出队首 (先进先出)
        sequence.append(v)

        for neighbor in adj[v]:           # 按字母顺序遍历邻居
            if neighbor not in visited:
                visited.add(neighbor)     # 入队时标记已访问
                queue.append(neighbor)

    return sequence


# ============================================================
# 3. 可视化遍历过程
# ============================================================
def print_traversal_process(adj, start, traversal_fn, name):
    """逐步打印遍历过程, 方便理解"""
    print(f"\n{'─' * 50}")
    print(f"【{name} 遍历过程】")
    print(f"{'─' * 50}")
    sequence = traversal_fn(adj, start)
    print(f"  序列: {' → '.join(sequence)}")
    return sequence


# ============================================================
# 主程序
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("图的遍历 (DFS & BFS) — 作业解答")
    print("=" * 60)

    # 构建邻接表
    adj = build_adjacency_list(vertices, edges)

    # 打印图结构
    print("\n【图结构】")
    print(f"  顶点: {vertices}  (共 {len(vertices)} 个)")
    print(f"  边:   {', '.join(f'{u}-{v}' for u, v in edges)}  (共 {len(edges)} 条)")
    print(f"  图:")
    print(f"            A         ")
    print(f"           / \\       ")
    print(f"          B   C       ")
    print(f"          |  /|       邻接点按字母顺序访问")
    print(f"          | / |       ")
    print(f"          D---E       ")
    print(f"\n  邻接表:")
    for v in vertices:
        print(f"    {v} → {adj[v]}")

    # ----- DFS -----
    print("\n" + "=" * 60)
    print("1. DFS 深度优先搜索 (从 A 出发)")
    print("=" * 60)

    seq_dfs_rec = print_traversal_process(adj, 'A', dfs, "DFS (递归)")
    seq_dfs_iter = print_traversal_process(adj, 'A', dfs_iterative, "DFS (迭代)")

    # 验证递归和迭代是否一致
    if seq_dfs_rec == seq_dfs_iter:
        print("  [OK] 递归与迭代版本遍历顺序一致")

    # ----- BFS -----
    print("\n" + "=" * 60)
    print("2. BFS 广度优先搜索 (从 A 出发)")
    print("=" * 60)

    seq_bfs = print_traversal_process(adj, 'A', bfs, "BFS")

    # ----- 对比总结 -----
    print("\n" + "=" * 60)
    print("3. 结果汇总")
    print("=" * 60)
    print(f"""
    遍历方式    | 序列                | 数据结构 | 特点
    ────────────┼─────────────────────┼──────────┼────────────────
    DFS (递归)  | {' → '.join(seq_dfs_rec):19s} | 递归栈   | 一路走到底, 回溯探索
    DFS (迭代)  | {' → '.join(seq_dfs_iter):19s} | 显式栈   | 手动模拟递归
    BFS         | {' → '.join(seq_bfs):19s} | 队列     | 层层推进, 最短路径
    """)

    # ----- 遍历树 -----
    print("=" * 60)
    print("4. 遍历树 (Traversal Tree)")
    print("=" * 60)
    print(f"""
    DFS 遍历树 (深度优先生成树):        BFS 遍历树 (广度优先生成树):

          A (0)                              A (0)
         /   \\                              /   \\
        B (1) C (3)                        B (1) C (2)
        |       |                          |     / \\
        D (2)   E (4)                      D (3)   E (4)

    括号内为访问次序编号                    BFS 按层访问, 先访问完一层再下一层
    DFS 优先深入子树
    """)

    # ----- 补充：连通分量 -----
    print("=" * 60)
    print("5. 补充：求连通分量 (Connected Components)")
    print("=" * 60)
    print(f"  对该图所有未访问顶点执行 DFS:")

    visited_all = set()
    components = []
    for v in vertices:
        if v not in visited_all:
            # 收集该连通分量的所有顶点
            comp_visited = set()
            stack = [v]
            while stack:
                node = stack.pop()
                if node in comp_visited:
                    continue
                comp_visited.add(node)
                for neighbor in adj[node]:
                    if neighbor not in comp_visited:
                        stack.append(neighbor)
            visited_all.update(comp_visited)
            components.append(sorted(comp_visited))

    print(f"  连通分量数: {len(components)}")
    for i, comp in enumerate(components, 1):
        print(f"    分量 {i}: {comp}")
    if len(components) == 1:
        print("  => 图是连通的, 所有顶点互相可达")

    print("\n" + "=" * 60)
    print("完成!")
    print("=" * 60)
