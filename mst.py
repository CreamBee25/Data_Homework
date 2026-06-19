"""
最小生成树（Minimum Spanning Tree）— Prim & Kruskal 实现
图例：6 个顶点 A(0)..F(5) 的无向带权图
"""

from __future__ import annotations
import heapq
import sys
from typing import List, Tuple

INF = float('inf')
V = 6  # 顶点数

# ========================= 图的邻接表表示 =========================
# 顶点编号：A=0, B=1, C=2, D=3, E=4, F=5
graph: List[List[Tuple[int, int]]] = [
    # A=0
    [(1, 2), (3, 3)],
    # B=1
    [(0, 2), (2, 4), (4, 1)],
    # C=2
    [(1, 4), (5, 5)],
    # D=3
    [(0, 3), (4, 6)],
    # E=4
    [(1, 1), (3, 6), (5, 2)],
    # F=5
    [(2, 5), (4, 2)],
]

# 边列表（用于 Kruskal）
edges: List[Tuple[int, int, int]] = [
    (2, 0, 1),   # A-B
    (4, 1, 2),   # B-C
    (3, 0, 3),   # A-D
    (1, 1, 4),   # B-E
    (5, 2, 5),   # C-F
    (6, 3, 4),   # D-E
    (2, 4, 5),   # E-F
]

NAME = ['A', 'B', 'C', 'D', 'E', 'F']


# ========================= Prim 算法 =========================
def prim(start: int = 0) -> Tuple[int, List[Tuple[int, int, int]]]:
    """
    Prim 堆优化版  O((V+E) log V)
    返回: (总权值, [(u, v, w), ...])  MST 边列表（按选边顺序）
    """
    dist = [INF] * V
    used = [False] * V
    pq: List[Tuple[float, int, int, int]] = []  # (dist, v, parent, weight)

    dist[start] = 0
    heapq.heappush(pq, (0, start, -1, 0))

    total = 0
    mst_edges: List[Tuple[int, int, int]] = []

    while pq:
        d, u, parent_u, edge_w = heapq.heappop(pq)
        if used[u]:
            continue
        used[u] = True
        total += d

        if parent_u != -1:
            mst_edges.append((parent_u, u, edge_w))

        for v, w in graph[u]:
            if not used[v] and w < dist[v]:
                dist[v] = w
                heapq.heappush(pq, (dist[v], v, u, w))

    return total, mst_edges


# ========================= 并查集 =========================
class UnionFind:
    """带路径压缩 + 按大小合并的并查集"""

    def __init__(self, n: int):
        self.fa = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        if self.fa[x] != x:
            self.fa[x] = self.find(self.fa[x])  # 路径压缩
        return self.fa[x]

    def unite(self, x: int, y: int) -> bool:
        """合并成功返回 True，已在同一集合返回 False"""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        # 按大小合并：小树挂到大树上
        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx
        self.fa[ry] = rx
        self.size[rx] += self.size[ry]
        return True


# ========================= Kruskal 算法 =========================
def kruskal() -> Tuple[int, List[Tuple[int, int, int]]]:
    """
    Kruskal  O(E log E)
    返回: (总权值, [(u, v, w), ...])  MST 边列表
    """
    uf = UnionFind(V)
    sorted_edges = sorted(edges)  # 按权值升序
    total = 0
    mst_edges: List[Tuple[int, int, int]] = []

    for w, u, v in sorted_edges:
        if uf.unite(u, v):
            total += w
            mst_edges.append((u, v, w))
            if len(mst_edges) == V - 1:
                break

    return total, mst_edges


# ========================= 输出辅助 =========================
def edge_str(u: int, v: int, w: int) -> str:
    return f"{NAME[u]}-{NAME[v]}({w})"


def format_mst(name: str, total: int, edges: List[Tuple[int, int, int]]):
    parts = [edge_str(u, v, w) for u, v, w in edges]
    print(f"  MST 总权值 : {total}")
    print(f"  MST 边     : {{{', '.join(parts)}}}")
    print(f"  选边顺序   : {' → '.join(parts)}")


# ========================= main =========================
if __name__ == '__main__':
    # 确保中文能在 Windows 终端正常输出
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("=" * 60)
    print("  最小生成树 — Prim & Kruskal")
    print("  图: A─2─B─4─C")
    print("      |     |     |")
    print("      3     1     5")
    print("      |     |     |")
    print("      D─6─E─2─F")
    print("=" * 60)

    # ----- Prim -----
    print("\n[Prim] Prim 算法（从 A 出发）")
    print("-" * 40)
    total_p, edges_p = prim(0)
    format_mst("Prim", total_p, edges_p)

    # ----- Kruskal -----
    print("\n[Kruskal] Kruskal 算法")
    print("-" * 40)
    total_k, edges_k = kruskal()
    format_mst("Kruskal", total_k, edges_k)

    # ----- 结论 -----
    print("\n" + "=" * 60)
    print("  结论：两种算法得到相同 MST，总权值 =", total_p)
    print("=" * 60)

    # 错误退出码（unittest 友好）
    if total_p != 12 or total_k != 12:
        print("\n[ERROR] 错误：预期 MST 总权值为 12", file=sys.stderr)
        sys.exit(1)
    else:
        print("\n[OK] 验证通过！")
