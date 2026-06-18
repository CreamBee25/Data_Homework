"""
图的存储 — 作业解答
=====================
给定一个 6 顶点无向图:
- 顶点: A, B, C, D, E, F
- 边:   A-B, B-C, C-D, D-E, E-F, F-A (六边形外圈)
         A-C, B-E (两条对角线)

本程序分别输出:
  1. 邻接矩阵 (Adjacency Matrix) — 用二维数组存储
  2. 邻接表 (Adjacency List)     — 为每个顶点维护邻居列表
"""

# ============================================================
# 图的结构定义
# ============================================================

# 顶点列表, 按 A~F 顺序 (索引 0~5)
vertices = ['A', 'B', 'C', 'D', 'E', 'F']
n = len(vertices)  # 顶点数: 6

# 邻接表: 无向图的边 (每条边存为无序对)
edges = [
    ('A', 'B'),  # 六边形外边
    ('B', 'C'),
    ('C', 'D'),
    ('D', 'E'),
    ('E', 'F'),
    ('F', 'A'),
    ('A', 'C'),  # 对角线
    ('B', 'E'),  # 对角线
]

# ============================================================
# 1. 邻接矩阵 (Adjacency Matrix)
# ============================================================
# 用 n × n 的二维数组表示:
#   matrix[i][j] = 1  表示 i 与 j 之间有边
#   matrix[i][j] = 0  表示 i 与 j 之间无边
# 无向图的邻接矩阵是对称的: matrix[i][j] == matrix[j][i]

def build_adjacency_matrix(vertices, edges):
    """
    根据顶点列表和边列表构建邻接矩阵

    时间复杂度: O(n² + e), n = 顶点数, e = 边数
    空间复杂度: O(n²)
    """
    # 建立顶点名 → 索引的映射
    idx = {v: i for i, v in enumerate(vertices)}

    # 初始化 n×n 全零矩阵
    matrix = [[0] * n for _ in range(n)]

    # 填入边 (无向图: 对称位置同时置 1)
    for u, v in edges:
        i, j = idx[u], idx[v]
        matrix[i][j] = 1
        matrix[j][i] = 1  # 无向图, 对称

    return matrix


def print_adjacency_matrix(matrix, vertices):
    """格式化打印邻接矩阵"""
    n = len(vertices)
    # 列标题
    header = "    " + "  ".join(vertices)
    sep = "   " + "---" * n
    print(header)
    print(sep)
    # 逐行打印
    for i, v in enumerate(vertices):
        row_str = "  ".join(f"{matrix[i][j]:2d}" for j in range(n))
        print(f"{v} | {row_str}")


# ============================================================
# 2. 邻接表 (Adjacency List)
# ============================================================
# 为每个顶点维护一个列表, 存储其所有邻居
# 可用 字典 或 列表的列表 实现

def build_adjacency_list(vertices, edges):
    """
    根据顶点列表和边列表构建邻接表

    时间复杂度: O(n + e), n = 顶点数, e = 边数
    空间复杂度: O(n + e)
    """
    # 初始化: 每个顶点的邻居列表为空
    adj_list = {v: [] for v in vertices}

    # 填入边 (无向图: A-B 意味着 A 的列表加 B, B 的列表加 A)
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)  # 无向图, 双向

    return adj_list


def print_adjacency_list(adj_list):
    """格式化打印邻接表"""
    for v in vertices:  # 按 A~F 顺序输出
        neighbors = adj_list[v]
        # 邻居也按字母顺序排列, 阅读更清晰
        neighbors_sorted = sorted(neighbors)
        print(f"  {v} → [{', '.join(neighbors_sorted)}]")


# ============================================================
# 3. 使用链表实现的邻接表 (邻接链表, 更贴近教材定义)
# ============================================================
class ListNode:
    """邻接链表中的节点"""
    def __init__(self, vertex_idx, weight=None):
        self.vertex = vertex_idx  # 邻居顶点索引
        self.weight = weight      # 权重 (无权图可用 None)
        self.next = None          # 指向下一个邻居


class AdjacencyLinkedList:
    """
    邻接链表 (经典邻接表实现)

    每个顶点维护一条单链表, 链表中的每个节点代表一个邻居。
    这种实现比 Python 列表更贴近 C/C++ 教材中的标准写法。
    """

    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.idx = {v: i for i, v in enumerate(vertices)}
        self.head = [None] * len(vertices)  # 每个顶点的链表头指针

        for u, v in edges:
            i, j = self.idx[u], self.idx[v]
            # 在 i 的链表中插入 j
            node_j = ListNode(v)
            node_j.next = self.head[i]
            self.head[i] = node_j
            # 在 j 的链表中插入 i (无向图)
            node_i = ListNode(u)
            node_i.next = self.head[j]
            self.head[j] = node_i

    def print_list(self):
        """打印邻接链表"""
        for v in self.vertices:
            i = self.idx[v]
            neighbors = []
            cur = self.head[i]
            while cur:
                neighbors.append(cur.vertex)
                cur = cur.next
            # 排序输出, 方便阅读
            print(f"  {v} → [{' -> '.join(sorted(neighbors))} -> NULL]" if neighbors
                  else f"  {v} → [NULL]")


# ============================================================
# 主程序: 输出结果
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("图的存储 — 作业解答")
    print("=" * 60)

    print("\n【图结构】")
    print(f"  顶点数: {n}  顶点: {vertices}")
    print(f"  边数: {len(edges)}  边: {', '.join(f'{u}-{v}' for u, v in edges)}")

    # ----- 邻接矩阵 -----
    print("\n" + "=" * 60)
    print("1. 邻接矩阵 (Adjacency Matrix)")
    print("=" * 60)
    adj_matrix = build_adjacency_matrix(vertices, edges)
    print_adjacency_matrix(adj_matrix, vertices)

    # ----- 邻接表 -----
    print("\n" + "=" * 60)
    print("2. 邻接表 (Adjacency List)")
    print("=" * 60)
    adj_list = build_adjacency_list(vertices, edges)
    print_adjacency_list(adj_list)

    # ----- 邻接链表 (经典教材写法) -----
    print("\n" + "=" * 60)
    print("3. 邻接链表 (经典教材链表实现)")
    print("=" * 60)
    linked = AdjacencyLinkedList(vertices, edges)
    linked.print_list()

    # ----- 两种存储方式对比 -----
    print("\n" + "=" * 60)
    print("4. 复杂度对比")
    print("=" * 60)
    print(f"""
    +------------------+----------------------+----------------------+
    |   操作           |   邻接矩阵            |   邻接表              |
    +------------------+----------------------+----------------------+
    |  空间复杂度       |   O(n^2) = {n*n:3d}       |   O(n+e) = {n+len(edges):3d}        |
    |  判断边 u-v      |   O(1)               |   O(deg(u))          |
    |  遍历所有边       |   O(n^2)             |   O(n+e)             |
    |  遍历顶点邻居     |   O(n)               |   O(deg(v))          |
    +------------------+----------------------+----------------------+

    适用场景:
    - 稠密图 (边数接近 n^2): 邻接矩阵更优
    - 稀疏图 (边数远小于 n^2): 邻接表更优 (节省空间, 遍历更快)
    - 本图边数 {len(edges)} < {n*(n-1)//2} (完全图边数), 属于稀疏图, 邻接表更合适
    """)

    print("=" * 60)
    print("完成!")
    print("=" * 60)
