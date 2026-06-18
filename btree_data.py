"""B-Tree 数据导出 — 可直接 import 使用"""

M = 3
KEYS = [10, 20, 5, 6, 12, 30, 25]

# 树结构 (嵌套字典)
tree_structure = {'keys': [10, 20], 'is_leaf': False, 'num_keys': 2, 'num_children': 3, 'children': [{'keys': [5, 6], 'is_leaf': True, 'num_keys': 2, 'num_children': 0, 'children': []}, {'keys': [12], 'is_leaf': True, 'num_keys': 1, 'num_children': 0, 'children': []}, {'keys': [25, 30], 'is_leaf': True, 'num_keys': 2, 'num_children': 0, 'children': []}]}

# 验证结果
verification_passed = True
verification_details = ['[OK] 性质1: 每个结点最多 2 个键', '[OK] 性质2: 每个结点最多 3 个子结点', '[OK] 性质3: 根结点至少有 1 个键 (实际=2)', '[OK] 性质4: 每个非根结点至少 1 个键', '[OK] 性质5: k 键内部结点有 k+1 个子结点', '[OK] 性质6: 所有叶结点在同一层 (depth=1)', '[OK] 性质7: 结点内键值有序排列', '[OK] 性质8 (BST): 所有子结点键值在正确范围内']
