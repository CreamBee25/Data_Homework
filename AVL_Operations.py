# -*- coding: utf-8 -*-
"""
AVL Tree — 构建与旋转实操
插入序列: [30, 20, 10, 25, 40, 35, 50]
每步展示: 平衡因子、失衡类型、旋转轴、旋转后树形
"""

from __future__ import annotations
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from typing import Optional, List, Tuple


# ============================================================
#  AVLNode
# ============================================================
class AVLNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional[AVLNode] = None
        self.right: Optional[AVLNode] = None
        self.height: int = 1


# ============================================================
#  AVLTree
# ============================================================
class AVLTree:
    def __init__(self):
        self.root: Optional[AVLNode] = None

    # ---------- helpers ----------
    @staticmethod
    def height(n: Optional[AVLNode]) -> int:
        return n.height if n else 0

    @staticmethod
    def balance(n: Optional[AVLNode]) -> int:
        """balance factor = height(left) - height(right)"""
        if n is None:
            return 0
        return AVLTree.height(n.left) - AVLTree.height(n.right)

    @staticmethod
    def update_height(n: AVLNode) -> None:
        n.height = 1 + max(AVLTree.height(n.left), AVLTree.height(n.right))

    # ---------- rotations ----------
    def right_rotate(self, z: AVLNode) -> AVLNode:
        """LL: 右旋 — z 的左孩子 y 成为新根"""
        y = z.left
        assert y is not None
        T2 = y.right
        y.right = z
        z.left = T2
        self.update_height(z)
        self.update_height(y)
        return y

    def left_rotate(self, z: AVLNode) -> AVLNode:
        """RR: 左旋 — z 的右孩子 y 成为新根"""
        y = z.right
        assert y is not None
        T2 = y.left
        y.left = z
        z.right = T2
        self.update_height(z)
        self.update_height(y)
        return y

    # ---------- insert ----------
    def insert(self, val: int) -> bool:
        """标准 AVL 插入（含自动旋转）。返回是否发生了旋转。"""
        rotated = False

        def _insert(node: Optional[AVLNode]) -> Tuple[Optional[AVLNode], bool]:
            nonlocal rotated
            if node is None:
                return AVLNode(val), False

            child_rotated = False
            if val < node.val:
                node.left, child_rotated = _insert(node.left)
            elif val > node.val:
                node.right, child_rotated = _insert(node.right)
            else:
                return node, False  # duplicate

            self.update_height(node)
            bf = self.balance(node)

            # ---- rebalance ----
            if bf > 1:                          # 左重
                if self.balance(node.left) >= 0:   # LL
                    rotated = True
                    return self.right_rotate(node), True
                else:                               # LR
                    rotated = True
                    node.left = self.left_rotate(node.left)
                    return self.right_rotate(node), True
            if bf < -1:                         # 右重
                if self.balance(node.right) <= 0:   # RR
                    rotated = True
                    return self.left_rotate(node), True
                else:                               # RL
                    rotated = True
                    node.right = self.right_rotate(node.right)
                    return self.left_rotate(node), True

            return node, child_rotated

        self.root, was_rotated = _insert(self.root)
        return was_rotated

    # ---------- BST-only insert (for demo: show imbalance before rotation) ----------
    def insert_bst(self, val: int) -> Optional[AVLNode]:
        """纯 BST 插入（更新高度但不旋转）。
        返回第一个失衡节点（|BF|>1），无失衡则返回 None。"""

        imbalanced: List[Optional[AVLNode]] = [None]

        def _insert(node: Optional[AVLNode]) -> Optional[AVLNode]:
            if node is None:
                return AVLNode(val)
            if val < node.val:
                node.left = _insert(node.left)
            elif val > node.val:
                node.right = _insert(node.right)
            self.update_height(node)
            # 记录路径上第一个失衡节点（最深的一个）
            if imbalanced[0] is None and abs(self.balance(node)) > 1:
                imbalanced[0] = node
            return node

        self.root = _insert(self.root)
        return imbalanced[0]

    # ---------- rebalance a specific node ----------
    def rebalance_at(self, node: AVLNode) -> AVLNode:
        """对指定节点执行恰当的旋转，返回新子树根。"""
        bf = self.balance(node)
        if bf > 1:
            if self.balance(node.left) >= 0:
                return self.right_rotate(node)   # LL
            else:
                node.left = self.left_rotate(node.left)
                return self.right_rotate(node)   # LR
        elif bf < -1:
            if self.balance(node.right) <= 0:
                return self.left_rotate(node)    # RR
            else:
                node.right = self.right_rotate(node.right)
                return self.left_rotate(node)    # RL
        return node

    # ---------- classify imbalance ----------
    def classify(self, node: AVLNode) -> str:
        """返回失衡类型: 'LL' / 'LR' / 'RR' / 'RL'"""
        bf = self.balance(node)
        if bf > 1:
            return "LL" if self.balance(node.left) >= 0 else "LR"
        else:
            return "RR" if self.balance(node.right) <= 0 else "RL"

    # ---------- traverse ----------
    def inorder(self) -> List[int]:
        result: List[int] = []
        def _in(n: Optional[AVLNode]):
            if n:
                _in(n.left)
                result.append(n.val)
                _in(n.right)
        _in(self.root)
        return result

    # ---------- clone ----------
    def clone(self) -> AVLTree:
        """深拷贝整棵树（用于演示失衡前后对比）。"""
        def _copy(n: Optional[AVLNode]) -> Optional[AVLNode]:
            if n is None:
                return None
            c = AVLNode(n.val)
            c.height = n.height
            c.left = _copy(n.left)
            c.right = _copy(n.right)
            return c
        t = AVLTree()
        t.root = _copy(self.root)
        return t


# ============================================================
#  Tree printer (recursive compact layout, shows balance factor)
# ============================================================
def print_avl(root: Optional[AVLNode], title: str = "") -> None:
    """打印 AVL 树，每个节点显示 val(BF)。"""
    if title:
        print(f"\n--- {title} ---")
    if root is None:
        print("  (empty)")
        return

    def _h(n: Optional[AVLNode]) -> int:
        return n.height if n else 0

    def render(n: Optional[AVLNode]) -> Tuple[List[str], int, int]:
        if n is None:
            return [], 0, 0

        bf = _h(n.left) - _h(n.right)
        val = f"{n.val}({bf:+d})" if bf != 0 else f"{n.val}(0)"

        left_lines, l_center, lw = render(n.left)
        right_lines, r_center, rw = render(n.right)

        # ---- leaf ----
        if not left_lines and not right_lines:
            return [val], len(val) // 2, len(val)

        # ---- pad children to same height ----
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

        GAP = 1

        slash = l_center if n.left else None
        backslash = (lw + GAP + r_center) if n.right else None

        if slash is not None and backslash is not None:
            mid = (slash + backslash) // 2
        elif slash is not None:
            mid = slash + 1 + len(val) // 2
        else:
            assert backslash is not None
            mid = len(val) // 2
            backslash = len(val)

        root_start = mid - len(val) // 2
        merge_gap = GAP
        if not n.left and n.right:
            merge_gap = max(merge_gap, backslash + 1 - lw)

        total_w = max(
            lw + merge_gap + rw,
            root_start + len(val),
            (slash + 1) if slash is not None else 0,
            (backslash + 1) if backslash is not None else 0,
        )

        if root_start < 0:
            shift = -root_start
            root_start += shift
            mid += shift
            if slash is not None:
                slash += shift
            if backslash is not None:
                backslash += shift
            total_w += shift

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
#  Demo: step-by-step AVL construction
# ============================================================
def run_demo() -> None:
    values = [30, 20, 10, 25, 40, 35, 50]
    tree = AVLTree()

    print("=" * 65)
    print("  AVL 树构建与旋转实操")
    print(f"  插入序列: {values}")
    print("=" * 65)

    for step, v in enumerate(values, 1):
        print(f"\n{'─' * 65}")
        print(f"  Step {step}: Insert {v}")
        print(f"{'─' * 65}")

        # ---- 插入前 ----
        if tree.root is not None:
            print_avl(tree.root, f"Before inserting {v}")

        # 先保存一份当前树的快照（用于失衡展示）
        snapshot = tree.clone()

        # ---- BST 插入（不旋转），检测失衡 ----
        imbalanced = snapshot.insert_bst(v)

        if imbalanced is not None:
            # 有失衡！展示失衡树
            print_avl(snapshot.root, f"BST insert {v} → IMBALANCE at node {imbalanced.val}")
            rot_type = snapshot.classify(imbalanced)
            print(f"  ⚠ 失衡类型: {rot_type}   旋转轴: node({imbalanced.val})")

            # 解释旋转
            if rot_type == "LL":
                print(f"  → 右旋 (right rotate) at {imbalanced.val}:"
                      f" {imbalanced.val} 下沉为其左孩子的右子树")
            elif rot_type == "RR":
                print(f"  → 左旋 (left rotate) at {imbalanced.val}:"
                      f" {imbalanced.val} 下沉为其右孩子的左子树")
            elif rot_type == "LR":
                print(f"  → 先左旋 {imbalanced.val}.left, 再右旋 {imbalanced.val}")
            elif rot_type == "RL":
                print(f"  → 先右旋 {imbalanced.val}.right, 再左旋 {imbalanced.val}")

            # ---- 执行旋转 ----
            # 找到失衡节点在树中的父节点并执行旋转
            snapshot.root = snapshot.rebalance_at(imbalanced)
            print_avl(snapshot.root, "After rotation (balanced)")
        else:
            # 无失衡
            print_avl(snapshot.root, f"After inserting {v} (balanced)")

        # ---- 更新主树（标准 AVL 插入） ----
        tree.insert(v)

        # 验证
        inorder = tree.inorder()
        expected = sorted(values[:step])
        assert inorder == expected, f"BST 性质破坏! inorder={inorder}, expected={expected}"

    # ---- 最终总结 ----
    print(f"\n{'═' * 65}")
    print("  最终 AVL 树")
    print(f"{'═' * 65}")
    print_avl(tree.root, "Final AVL Tree")
    print(f"\n  中序遍历: {tree.inorder()}")
    print(f"  树高: {AVLTree.height(tree.root)}")
    print(f"  期望中序: {sorted(values)}  ← BST 性质保持 ✓")
    print(f"  所有节点 |BF| ≤ 1  ← AVL 平衡性质 ✓")
    print()

    # 逐节点验证平衡因子
    def verify_balance(n: Optional[AVLNode]) -> bool:
        if n is None:
            return True
        bf = AVLTree.balance(n)
        if abs(bf) > 1:
            print(f"  ✗ 节点 {n.val} 失衡! BF={bf}")
            return False
        return verify_balance(n.left) and verify_balance(n.right)
    assert verify_balance(tree.root), "AVL 平衡验证失败!"


# ============================================================
#  main
# ============================================================
if __name__ == "__main__":
    run_demo()
