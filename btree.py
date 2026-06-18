"""
3阶 B-Tree (m=3) 实现 — 先插入后分裂（自底向上）
键值序列: [10, 20, 5, 6, 12, 30, 25]

B-Tree 性质 (m=3):
  1. 每个结点最多有 m-1 = 2 个键值
  2. 每个结点最多有 m = 3 个子结点
  3. 根结点至少有 1 个键值（若非空）
  4. 每个非根结点至少有 ⌈m/2⌉ - 1 = 1 个键值
  5. 每个内部结点（非叶）若有 k 个键值，则有 k+1 个子结点
  6. 所有叶结点在同一层
  7. 结点内键值有序排列
  8. (BST性质) 第 i 个子树的所有键值在父结点键值 keys[i-1] 和 keys[i] 之间
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import os
import sys

# 确保 Windows 下正确输出 Unicode
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ─── B-Tree 数据结构 ───────────────────────────────────────────

@dataclass
class BTreeNode:
    """B-Tree 结点"""
    keys: List[int] = field(default_factory=list)
    children: List['BTreeNode'] = field(default_factory=list)
    is_leaf: bool = True

    @property
    def num_keys(self) -> int:
        return len(self.keys)

    @property
    def num_children(self) -> int:
        return len(self.children)


class BTree:
    """3阶 B-Tree (m=3)
    采用「先插入再自底向上分裂」策略：
      1. 找到叶结点，插入键值（允许临时溢出到 max_keys+1 个键）
      2. 若溢出，从中间键分裂：左右各分一半，中间键提升到父结点
      3. 若根也溢出，创建新根
    """

    def __init__(self, m: int = 3):
        self.m = m
        self.root: Optional[BTreeNode] = None
        self.max_keys = m - 1                # 2
        self.min_keys = (m + 1) // 2 - 1     # ⌈m/2⌉ - 1 = 1

    # ── 工具 ────────────────────────────────────────────

    def _find_pos(self, node: BTreeNode, key: int) -> int:
        """返回 key 在 node.keys 中的插入位置（也是去子结点 node.children[i] 的索引）"""
        for i, k in enumerate(node.keys):
            if key < k:
                return i
        return len(node.keys)

    # ── 插入（自底向上分裂） ──────────────────────────

    def insert(self, key: int) -> None:
        """插入一个键值"""
        if self.root is None:
            self.root = BTreeNode(keys=[key], is_leaf=True)
            return

        split_result = self._insert_recursive(self.root, key)
        if split_result is not None:
            # 根分裂了 — 创建新根
            promoted_key, left, right = split_result
            new_root = BTreeNode(keys=[promoted_key], is_leaf=False)
            new_root.children = [left, right]
            self.root = new_root

    def _insert_recursive(
        self, node: BTreeNode, key: int
    ) -> Optional[Tuple[int, 'BTreeNode', 'BTreeNode']]:
        """
        递归插入。
        返回 None 表示无需分裂；
        返回 (promoted_key, left_child, right_child) 表示该结点需要分裂。
        """
        if node.is_leaf:
            # 叶结点：直接插入
            pos = self._find_pos(node, key)
            node.keys.insert(pos, key)
            if node.num_keys <= self.max_keys:
                return None  # 未溢出
            return self._split_node(node)

        # 内部结点：沿正确子树递归
        pos = self._find_pos(node, key)
        result = self._insert_recursive(node.children[pos], key)

        if result is None:
            return None

        # 子结点分裂了，把提升的键和右孩子整合进来
        promoted_key, left_child, right_child = result
        node.children[pos] = left_child
        node.children.insert(pos + 1, right_child)
        node.keys.insert(pos, promoted_key)

        if node.num_keys <= self.max_keys:
            return None
        return self._split_node(node)

    def _split_node(
        self, node: BTreeNode
    ) -> Tuple[int, 'BTreeNode', 'BTreeNode']:
        """
        分裂一个有 max_keys + 1 个键的结点。
        返回 (promoted_key, left_node, right_node)。
        对于 m=3, 3 个键 [k0, k1, k2] → 左[k0], 提升k1, 右[k2]
        """
        mid = node.num_keys // 2  # 3 // 2 = 1 (中间键索引)

        promoted_key = node.keys[mid]

        left = BTreeNode(
            keys=node.keys[:mid],
            is_leaf=node.is_leaf,
        )
        right = BTreeNode(
            keys=node.keys[mid + 1:],
            is_leaf=node.is_leaf,
        )

        if not node.is_leaf:
            left.children = node.children[:mid + 1]
            right.children = node.children[mid + 1:]

        return promoted_key, left, right

    # ── 批量插入 ──────────────────────────────────────────

    def build(self, keys: List[int]) -> None:
        for key in keys:
            self.insert(key)

    # ── 文本可视化（树形） ──────────────────────────────

    def visualize_text(self) -> str:
        if self.root is None:
            return "(空树)"
        lines = []
        self._build_text(self.root, "", True, lines)
        return "\n".join(lines)

    def _build_text(self, node: BTreeNode, prefix: str, is_last: bool,
                    lines: List[str]) -> None:
        connector = "└── " if is_last else "├── "
        keys_str = ", ".join(str(k) for k in node.keys)
        info = f"  [keys={node.num_keys}, children={node.num_children}]"
        tag = " LEAF" if node.is_leaf else " INTERNAL"
        lines.append(f"{prefix}{connector}[{keys_str}]{info}{tag}")

        child_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(node.children):
            self._build_text(child, child_prefix,
                             i == len(node.children) - 1, lines)

    def visualize_ascii(self) -> str:
        if self.root is None:
            return "(空树)"
        lines = []
        self._build_ascii(self.root, 0, lines)
        return "\n".join(lines)

    def _build_ascii(self, node: BTreeNode, depth: int,
                     lines: List[str]) -> None:
        indent = "    " * depth
        keys_str = "[" + ", ".join(str(k) for k in node.keys) + "]"
        info = f"(keys={node.num_keys}, children={node.num_children})"
        tag = "[LEAF]" if node.is_leaf else "[INTERNAL]"
        lines.append(f"{indent}{keys_str} {tag} {info}")
        for child in node.children:
            self._build_ascii(child, depth + 1, lines)

    # ── 属性验证 ──────────────────────────────────────────

    def verify(self) -> Tuple[bool, List[str]]:
        results = []
        all_ok = True

        if self.root is None:
            results.append("[OK] 空树 — 满足所有性质")
            return True, results

        m = self.m

        # 性质1: 每个结点最多 m-1 个键
        ok = True
        for node, _ in self._traverse(self.root):
            if node.num_keys > m - 1:
                results.append(
                    f"[FAIL] 性质1: 结点 {node.keys} 有 {node.num_keys} 键 (max={m-1})")
                ok = False
        results.append(
            f"[{'OK' if ok else 'FAIL'}] 性质1: 每个结点最多 {m-1} 个键")
        if not ok: all_ok = False

        # 性质2: 每个结点最多 m 个子结点
        ok = True
        for node, _ in self._traverse(self.root):
            if node.num_children > m:
                results.append(
                    f"[FAIL] 性质2: 结点 {node.keys} 有 {node.num_children} 孩子 (max={m})")
                ok = False
        results.append(
            f"[{'OK' if ok else 'FAIL'}] 性质2: 每个结点最多 {m} 个子结点")
        if not ok: all_ok = False

        # 性质3: 根至少有 1 个键
        if self.root.num_keys >= 1:
            results.append(
                f"[OK] 性质3: 根结点至少有 1 个键 (实际={self.root.num_keys})")
        else:
            results.append(
                f"[FAIL] 性质3: 根结点只有 {self.root.num_keys} 个键")
            all_ok = False

        # 性质4: 非根结点至少有 ⌈m/2⌉-1 个键
        min_keys = (m + 1) // 2 - 1
        ok = True
        for node, _ in self._traverse(self.root):
            if node is self.root:
                continue
            if node.num_keys < min_keys:
                results.append(
                    f"[FAIL] 性质4: 结点 {node.keys} 有 {node.num_keys} 键 (min={min_keys})")
                ok = False
        results.append(
            f"[{'OK' if ok else 'FAIL'}] 性质4: 每个非根结点至少 {min_keys} 个键")
        if not ok: all_ok = False

        # 性质5: k 个键的内部结点有 k+1 个子结点
        ok = True
        for node, _ in self._traverse(self.root):
            if not node.is_leaf and node.num_children != node.num_keys + 1:
                results.append(
                    f"[FAIL] 性质5: 结点 {node.keys} 有 {node.num_keys} 键 "
                    f"但 {node.num_children} 孩子 (应为 {node.num_keys + 1})")
                ok = False
        results.append(
            f"[{'OK' if ok else 'FAIL'}] 性质5: k 键内部结点有 k+1 个子结点")
        if not ok: all_ok = False

        # 性质6: 所有叶结点在同一层
        leaf_depths = []
        self._collect_leaf_depths(self.root, 0, leaf_depths)
        if len(set(leaf_depths)) == 1:
            results.append(
                f"[OK] 性质6: 所有叶结点在同一层 (depth={leaf_depths[0]})")
        else:
            results.append(
                f"[FAIL] 性质6: 叶结点深度不一致 {leaf_depths}")
            all_ok = False

        # 性质7: 结点内键值有序
        ok = True
        for node, _ in self._traverse(self.root):
            for i in range(len(node.keys) - 1):
                if node.keys[i] >= node.keys[i + 1]:
                    results.append(
                        f"[FAIL] 性质7: 结点 {node.keys} 键值无序")
                    ok = False
                    break
        results.append(
            f"[{'OK' if ok else 'FAIL'}] 性质7: 结点内键值有序排列")
        if not ok: all_ok = False

        # 性质8 (BST): 子结点键值在正确范围
        violations = self._check_bst(self.root, float('-inf'), float('inf'))
        if violations:
            for v in violations:
                results.append(f"[FAIL] 性质8: {v}")
            all_ok = False
        else:
            results.append(
                f"[OK] 性质8 (BST): 所有子结点键值在正确范围内")

        return all_ok, results

    def _traverse(self, node: BTreeNode, depth: int = 0):
        yield node, depth
        for child in node.children:
            yield from self._traverse(child, depth + 1)

    def _collect_leaf_depths(self, node: BTreeNode, depth: int,
                             depths: List[int]) -> None:
        if node.is_leaf:
            depths.append(depth)
        else:
            for child in node.children:
                self._collect_leaf_depths(child, depth + 1, depths)

    def _check_bst(self, node: BTreeNode, low: float, high: float) -> List[str]:
        violations = []
        for key in node.keys:
            if not (low < key < high):
                violations.append(
                    f"键 {key} 超出范围 ({low}, {high})")
        if not node.is_leaf:
            bounds = [low] + node.keys + [high]
            for i, child in enumerate(node.children):
                violations.extend(
                    self._check_bst(child, bounds[i], bounds[i + 1]))
        return violations

    # ── 逐步插入记录 ──────────────────────────────────────

    def build_with_log(self, keys: List[int]) -> List[str]:
        log = []
        self.__init__(self.m)
        for key in keys:
            self.insert(key)
            log.append(f"\n{'─' * 50}")
            log.append(f"插入 {key}:")
            log.append(f"{'─' * 50}")
            log.append(self.visualize_text())
        return log


# ─── 手动推演（用于对照验证） ───────────────────────────────

MANUAL_TRACE = r"""
╔══════════════════════════════════════════════════════════════╗
║           3阶 B-Tree 手动推演 (m=3, max=2键)                ║
╠══════════════════════════════════════════════════════════════╣

  插入 10:   [10]                           (根,1键,叶)
  插入 20:   [10, 20]                       (根,2键,叶) ← 已满

  插入 5:    根已满 → 临时[5,10,20] → 分裂!
             提升 10 为新根:
                   [10]
                  /    \
                [5]   [20]                  (10提升,子树各1键)

  插入 6:    6<10, 去左子[5] → [5,6]
                   [10]
                  /    \
              [5,6]   [20]                 (左叶2键)

  插入 12:   12>10, 去右子[20] → [12,20]
                   [10]
                  /    \
              [5,6]   [12,20]              (右叶2键)

  插入 30:   30>10, 去右子[12,20] → 临时[12,20,30] → 分裂!
             提升 20 到根:
                [10, 20]
               /    |    \
           [5,6]  [12]  [30]              (根2键,3孩子)

  插入 25:   25>20, 去右子[30] → [25,30]
                [10, 20]
               /    |    \
           [5,6]  [12]  [25,30]           ← 最终结构!

╚══════════════════════════════════════════════════════════════╝
"""

FINAL_DIAGRAM = r"""
              ┌──────────────┐
              │   10 , 20    │  ← 根结点 (内部)
              │  keys=2      │
              │  children=3  │
              └──────────────┘
               /      |      \
              /       |       \
    ┌─────────┐  ┌────────┐  ┌──────────┐
    │  5, 6   │  │   12   │  │  25, 30  │  ← 叶结点层
    │ keys=2  │  │ keys=1 │  │  keys=2  │     (全部同一深度)
    │ child=0 │  │ child=0│  │  child=0 │
    └─────────┘  └────────┘  └──────────┘
"""


# ─── 主程序 ──────────────────────────────────────────────────

def main():
    keys = [10, 20, 5, 6, 12, 30, 25]
    m = 3
    output_dir = os.path.dirname(os.path.abspath(__file__))

    # ── 构建 B-Tree ─────────────────────────────────────
    tree = BTree(m=m)
    step_log = tree.build_with_log(keys)

    # ── 验证 ────────────────────────────────────────────
    passed, checks = tree.verify()

    # ══════════════════════════════════════════════════════
    #  输出文件1: btree_report.txt — 完整报告
    # ══════════════════════════════════════════════════════
    report_path = os.path.join(output_dir, "btree_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("  3阶 B-Tree (m=3) 构建报告\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"键值序列: {keys}\n")
        f.write(f"B-Tree 阶数: m = {m}\n")
        f.write(f"最大键数/结点: m-1 = {m-1}\n")
        f.write(f"最小键数/结点 (非根): ceil(m/2)-1 = {(m+1)//2 - 1}\n")

        f.write("\n" + "=" * 60 + "\n")
        f.write("  手动推演过程\n")
        f.write("=" * 60 + "\n")
        f.write(MANUAL_TRACE)

        f.write("\n" + "=" * 60 + "\n")
        f.write("  程序逐步插入过程\n")
        f.write("=" * 60 + "\n")
        for step in step_log:
            f.write(step + "\n")

        f.write("\n\n" + "=" * 60 + "\n")
        f.write("  最终树形结构\n")
        f.write("=" * 60 + "\n")
        f.write(FINAL_DIAGRAM)
        f.write("\n\n─── 程序生成 (文本树) ───\n\n")
        f.write(tree.visualize_text())
        f.write("\n\n─── ASCII 紧凑视图 ───\n\n")
        f.write(tree.visualize_ascii())

        f.write("\n\n" + "=" * 60 + "\n")
        f.write("  B-Tree 性质验证\n")
        f.write("=" * 60 + "\n\n")
        for check in checks:
            f.write(check + "\n")
        f.write(f"\n{'[RESULT] All properties satisfied!' if passed else '[RESULT] Some properties violated!'}\n")

        f.write("\n" + "=" * 60 + "\n")
        f.write("  各结点明细\n")
        f.write("=" * 60 + "\n\n")
        for idx, (node, depth) in enumerate(tree._traverse(tree.root)):
            f.write(f"Node #{idx} (depth={depth}):\n")
            f.write(f"  keys      = {node.keys}\n")
            f.write(f"  num_keys  = {node.num_keys}\n")
            f.write(f"  children  = {node.num_children}\n")
            f.write(f"  type      = {'LEAF' if node.is_leaf else 'INTERNAL'}\n")
            if node.children:
                child_info = ", ".join(
                    f"child[{i}].keys={c.keys}" for i, c in enumerate(node.children))
                f.write(f"  children  = {child_info}\n")
            f.write("\n")

    print(f"[OK] btree_report.txt")

    # ══════════════════════════════════════════════════════
    #  输出文件2: btree_structure.txt — 纯结构图
    # ══════════════════════════════════════════════════════
    tree_path = os.path.join(output_dir, "btree_structure.txt")
    with open(tree_path, "w", encoding="utf-8") as f:
        f.write("3阶 B-Tree 最终结构\n")
        f.write(f"键值序列: {keys}\n")
        f.write("m = 3 (max 2 keys, max 3 children per node)\n\n")
        f.write(FINAL_DIAGRAM)
        f.write("\n\n程序生成结构:\n\n")
        f.write(tree.visualize_text())
        f.write("\n\n标注说明:\n")
        f.write("  [keys=N, children=M]  该结点有 N 个键值, M 个子结点\n")
        f.write("  LEAF     = 叶结点\n")
        f.write("  INTERNAL = 内部结点\n")
    print(f"[OK] btree_structure.txt")

    # ══════════════════════════════════════════════════════
    #  输出文件3: btree_data.py — 可导入的数据结构
    # ══════════════════════════════════════════════════════
    data_path = os.path.join(output_dir, "btree_data.py")
    with open(data_path, "w", encoding="utf-8") as f:
        f.write('"""B-Tree 数据导出 — 可直接 import 使用"""\n\n')
        f.write(f"M = {m}\n")
        f.write(f"KEYS = {keys}\n\n")
        f.write("# 树结构 (嵌套字典)\n")
        f.write("tree_structure = ")
        f.write(_serialize_tree(tree.root))
        f.write("\n\n")
        f.write("# 验证结果\n")
        f.write("verification_passed = " + str(passed) + "\n")
        f.write("verification_details = " + repr(checks) + "\n")
    print(f"[OK] btree_data.py")

    # ══════════════════════════════════════════════════════
    #  终端输出
    # ══════════════════════════════════════════════════════
    print()
    print(MANUAL_TRACE)
    print(FINAL_DIAGRAM)
    print("=" * 60)
    print("  程序生成结构")
    print("=" * 60)
    print()
    print(tree.visualize_text())
    print()
    print("=" * 60)
    print("  B-Tree 性质验证")
    print("=" * 60)
    for c in checks:
        print(c)
    print()
    if passed:
        print("All B-Tree properties satisfied!")
    else:
        print("Some properties violated!")


def _serialize_tree(node: Optional[BTreeNode]) -> str:
    if node is None:
        return "None"
    children_repr = [_serialize_tree(c) for c in node.children]
    return (
        f"{{'keys': {node.keys}, "
        f"'is_leaf': {node.is_leaf}, "
        f"'num_keys': {node.num_keys}, "
        f"'num_children': {node.num_children}, "
        f"'children': [{', '.join(children_repr)}]}}"
    )


if __name__ == "__main__":
    main()
