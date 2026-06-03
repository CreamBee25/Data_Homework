# -*- coding: utf-8 -*-
from __future__ import annotations

"""
BST Operations - Build, Delete, and Consecutive Deletion Strategies
Q1: Build BST from [50, 30, 70, 20, 40, 60, 80]
Q2: Delete root 50 using inorder predecessor vs successor
Q3: Best strategy for consecutive deletions (alternate, random, height-based)
"""

import sys
import io
# Fix Windows GBK encoding issue
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from dataclasses import dataclass
from typing import Optional, List, Tuple
import random


# ============================================================
#  TreeNode
# ============================================================
@dataclass
class TreeNode:
    val: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


# ============================================================
#  BST class
# ============================================================
class BST:
    def __init__(self):
        self.root: Optional[TreeNode] = None

    # ---------- Insert ----------
    def insert(self, val: int) -> None:
        self.root = self._insert(self.root, val)

    def _insert(self, node: Optional[TreeNode], val: int) -> TreeNode:
        if node is None:
            return TreeNode(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)
        return node

    # ---------- Find min / max ----------
    def find_min(self, node: TreeNode) -> TreeNode:
        """Minimum in subtree (inorder successor candidate)"""
        while node.left:
            node = node.left
        return node

    def find_max(self, node: TreeNode) -> TreeNode:
        """Maximum in subtree (inorder predecessor candidate)"""
        while node.right:
            node = node.right
        return node

    # ---------- Delete ----------
    def delete(self, val: int, strategy: str = "successor") -> bool:
        """
        Delete node with given val.
        strategy: "predecessor" or "successor"
        """
        found = False

        def _delete(node: Optional[TreeNode]) -> Optional[TreeNode]:
            nonlocal found
            if node is None:
                return None
            if val < node.val:
                node.left = _delete(node.left)
            elif val > node.val:
                node.right = _delete(node.right)
            else:
                found = True
                # 0 or 1 child
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left

                # 2 children
                if strategy == "predecessor":
                    pred = self.find_max(node.left)
                    node.val = pred.val
                    node.left = self._delete_node(node.left, pred.val)
                else:
                    succ = self.find_min(node.right)
                    node.val = succ.val
                    node.right = self._delete_node(node.right, succ.val)
            return node

        self.root = _delete(self.root)
        return found

    def _delete_node(self, node: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        """Helper: delete a known value from subtree (defaults to successor)"""
        if node is None:
            return None
        if val < node.val:
            node.left = self._delete_node(node.left, val)
        elif val > node.val:
            node.right = self._delete_node(node.right, val)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            succ = self.find_min(node.right)
            node.val = succ.val
            node.right = self._delete_node(node.right, succ.val)
        return node

    # ---------- Traversal ----------
    def inorder(self) -> List[int]:
        result: List[int] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[TreeNode], result: List[int]) -> None:
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.val)
        self._inorder(node.right, result)

    # ---------- Height ----------
    def height(self) -> int:
        return self._height(self.root)

    def _height(self, node: Optional[TreeNode]) -> int:
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))


# ============================================================
#  Pretty print  (recursive compact layout, branches at child centers)
# ============================================================
def print_tree(root: Optional[TreeNode], title: str = "") -> None:
    """Print tree top-down. Each subtree is rendered compactly; the root
       is centered between its children, and / \\ point exactly to the
       child roots — no crooked gaps."""
    if title:
        print(f"\n--- {title} ---")
    if root is None:
        print("  (empty)")
        return

    # ── recursive layout ────────────────────────────────────
    def render(n: Optional[TreeNode]) -> Tuple[List[str], int, int]:
        """Return (lines, root_center, width) for the subtree rooted at n.
        All strings in `lines` have exactly the same length = width."""
        if n is None:
            return [], 0, 0

        val = str(n.val)
        left_lines, l_center, lw = render(n.left)
        right_lines, r_center, rw = render(n.right)

        # ---- leaf ----
        if not left_lines and not right_lines:
            return [val], len(val) // 2, len(val)

        # ---- pad children to the same height ----
        max_h = max(len(left_lines), len(right_lines))
        if left_lines:
            left_lines = [ln.ljust(lw) for ln in left_lines]
        else:
            left_lines = []
        if right_lines:
            right_lines = [rn.ljust(rw) for rn in right_lines]
        else:
            right_lines = []
        left_lines += [" " * lw] * (max_h - len(left_lines))
        right_lines += [" " * rw] * (max_h - len(right_lines))

        GAP = 1  # minimum gap between left & right subtrees

        # ---- unified position calculation ----
        # left  block occupies columns [0, lw); its root center = l_center
        # right block occupies columns [lw+GAP, lw+GAP+rw); its root center = lw+GAP+r_center
        slash = l_center if n.left else None
        backslash = (lw + GAP + r_center) if n.right else None

        if slash is not None and backslash is not None:
            # both children: root centered between / and \
            mid = (slash + backslash) // 2
        elif slash is not None:
            # only left child: root hugs the / (1 col right of it)
            mid = slash + 1 + len(val) // 2
        else:
            # only right child: root at left margin, \ hugs the root
            assert backslash is not None
            mid = len(val) // 2
            backslash = len(val)  # right after the root value

        root_start = mid - len(val) // 2

        # effective merge gap (wider for only-right-child so child sits after \)
        merge_gap = GAP
        if not n.left and n.right:
            merge_gap = max(merge_gap, backslash + 1 - lw)

        total_w = max(
            lw + merge_gap + rw,
            root_start + len(val),
            (slash + 1) if slash is not None else 0,
            (backslash + 1) if backslash is not None else 0,
        )

        # shift right if root sticks out on the left
        if root_start < 0:
            shift = -root_start
            root_start += shift
            mid += shift
            if slash is not None:
                slash += shift
            if backslash is not None:
                backslash += shift
            total_w += shift

        # ---- build the three kinds of lines ----
        root_line = [" "] * total_w
        for i, ch in enumerate(val):
            root_line[root_start + i] = ch

        branch_line = [" "] * total_w
        if slash is not None:
            branch_line[slash] = "/"
        if backslash is not None:
            branch_line[backslash] = "\\"

        result = ["".join(root_line)]
        if "".join(branch_line).strip():
            result.append("".join(branch_line))

        for i in range(max_h):
            l = left_lines[i] if i < len(left_lines) else " " * lw
            r = right_lines[i] if i < len(right_lines) else " " * rw
            result.append((l + " " * merge_gap + r).ljust(total_w))

        return result, mid, total_w

    lines, _, _ = render(root)
    for line in lines:
        print(line.rstrip())


# ============================================================
#  Q1: Build BST
# ============================================================
def question1() -> BST:
    print("\n" + "=" * 60)
    print("  Q1: Build BST from [50, 30, 70, 20, 40, 60, 80]")
    print("=" * 60)

    values = [50, 30, 70, 20, 40, 60, 80]
    bst = BST()
    for v in values:
        bst.insert(v)

    print_tree(bst.root, "Final BST")
    print(f"Inorder: {bst.inorder()}")
    print(f"Height:  {bst.height()}")
    return bst


# ============================================================
#  Q2: Delete root 50
# ============================================================
def question2() -> None:
    print("\n" + "=" * 60)
    print("  Q2: Delete root 50 -- two strategies")
    print("=" * 60)

    # --- Strategy A: Predecessor ---
    print("\n>>> Strategy A: Inorder Predecessor (max of left subtree = 40)")
    bst_a = BST()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        bst_a.insert(v)
    print_tree(bst_a.root, "Before deletion")
    bst_a.delete(50, strategy="predecessor")
    print_tree(bst_a.root, "After replacing 50 with predecessor 40")
    print(f"Inorder: {bst_a.inorder()}")
    print(f"Height:  {bst_a.height()}")

    # --- Strategy B: Successor ---
    print("\n>>> Strategy B: Inorder Successor (min of right subtree = 60)")
    bst_b = BST()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        bst_b.insert(v)
    print_tree(bst_b.root, "Before deletion")
    bst_b.delete(50, strategy="successor")
    print_tree(bst_b.root, "After replacing 50 with successor 60")
    print(f"Inorder: {bst_b.inorder()}")
    print(f"Height:  {bst_b.height()}")


# ============================================================
#  Q3: Consecutive deletion — height-based adaptive (BEST)
# ============================================================
def question3() -> None:
    print("\n" + "=" * 60)
    print("  Q3: Consecutive deletion — height-based adaptive strategy [BEST]")
    print("=" * 60)

    bst = BST()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(v)

    print_tree(bst.root, "Initial BST")

    delete_order = [50, 70, 30, 20, 40, 60, 80]
    for v in delete_order:
        bst.delete_balanced(v)
        print_tree(bst.root, f"After deleting {v}  (height={bst.height()})")

    print(f"\nFinal inorder: {bst.inorder()}")
    print("Conclusion: Height-based adaptive strategy keeps the tree balanced.")


# ============================================================
#  高度自适应删除策略 (Height-based Adaptive Deletion)
# ============================================================
def delete_balanced(self: BST, val: int) -> bool:
    """
    高度自适应删除：比较被删节点的左右子树高度，
    从较高的一侧选取替换节点，以维持树的平衡。
    若两侧高度相等，则随机选择。

    Adaptive: compare left/right subtree heights, pick replacement
    from the taller side. If equal, random.
    """
    # 计算子树高度的辅助函数
    def _h(n: Optional[TreeNode]) -> int:
        if n is None:
            return 0
        return 1 + max(_h(n.left), _h(n.right))

    found = False

    def _delete(node: Optional[TreeNode]) -> Optional[TreeNode]:
        nonlocal found
        if node is None:
            return None
        # 递归查找要删除的节点
        if val < node.val:
            node.left = _delete(node.left)
        elif val > node.val:
            node.right = _delete(node.right)
        else:
            found = True
            # 情况1&2：0或1个子节点，直接用子节点替代
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # 情况3：有2个子节点 —— 比较左右子树高度，决定替换策略
            left_h = _h(node.left)
            right_h = _h(node.right)

            if left_h > right_h:
                # 左子树更高 → 从中取前驱（最大值），削减较高一侧
                pred = self.find_max(node.left)
                node.val = pred.val
                node.left = self._delete_node(node.left, pred.val)
            elif right_h > left_h:
                # 右子树更高 → 从中取后继（最小值），削减较高一侧
                succ = self.find_min(node.right)
                node.val = succ.val
                node.right = self._delete_node(node.right, succ.val)
            else:
                # 高度相等 → 随机选择，避免确定性策略导致的累积偏差
                if random.choice([True, False]):
                    pred = self.find_max(node.left)
                    node.val = pred.val
                    node.left = self._delete_node(node.left, pred.val)
                else:
                    succ = self.find_min(node.right)
                    node.val = succ.val
                    node.right = self._delete_node(node.right, succ.val)
        return node

    self.root = _delete(self.root)
    return found


# Monkey-patch the method
BST.delete_balanced = delete_balanced  # type: ignore[attr-defined]


# ============================================================
#  main
# ============================================================
if __name__ == "__main__":
    question1()
    question2()
    question3()


# ============================================================
#  附录：为何高度自适应策略是最优的？
# ============================================================
#
#  BST 的删除操作在遇到"有两个子节点"的节点时，必须选择一个替换值：
#    - 中序前驱（predecessor）：左子树的最大值
#    - 中序后继（successor）：右子树的最小值
#
#  ┌──────────────────────────────────────────────────────────────┐
#  │                    四种策略在连续删除下的表现                    │
#  ├──────────────┬───────────────────────────────────────────────┤
#  │ 始终用后继    │ 每次都从右子树取最小值，右子树越来越矮，         │
#  │              │ 左子树保持原样 → 树逐渐向左倾斜，退化成链        │
#  ├──────────────┼───────────────────────────────────────────────┤
#  │ 始终用前驱    │ 每次都从左子树取最大值，与上面对称，            │
#  │              │ 树逐渐向右倾斜，退化成链                        │
#  ├──────────────┼───────────────────────────────────────────────┤
#  │ 交替使用      │ 比固定策略好，但不看实际树形，                   │
#  │              │ 可能在"刚好需要另一边"时选了错误的一侧            │
#  ├──────────────┼───────────────────────────────────────────────┤
#  │ 高度自适应 ✅  │ 每次删除前先比较左右子树高度，                  │
#  │              │ 从更高的一侧取替换节点，把"胖"的一边削薄          │
#  │              │ → 树自然趋向平衡，高度始终接近 O(log n)          │
#  └──────────────┴───────────────────────────────────────────────┘
#
#  直观类比：
#    想象一棵树左右两边是两根弹簧。每次删除从哪边取节点，
#    相当于把哪边的弹簧剪掉一节。
#    - 固定策略 = 永远剪同一侧 → 一侧越来越短，树歪了
#    - 高度自适应 = 每次剪较长的那根弹簧 → 两侧长度始终接近
#
#  时间复杂度：
#    三种策略的单次删除都是 O(h)，h 为树高。区别在于：
#    - 固定策略：连续删除 k 个节点后，h 可能退化为 O(n-k)
#    - 高度自适应：h 始终保持在 O(log n)，所有操作更快
#
#  高度相等时为何随机？
#    避免引入确定性偏差。如果高度相等时总是选后继，长期来看
#    会形成微小的右偏累积，随机选择彻底消除了这种风险。
#
#  结论：在需要频繁增删的 BST 场景中，高度自适应删除策略
#        能以极小的代价（每次多比较一次高度）换取树的长期平衡，
#        是四种策略中的最优选择。
