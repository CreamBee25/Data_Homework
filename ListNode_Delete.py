class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val  # 节点的值
        self.next = next  # 指向下一个节点的指针

class LinkedList:
    def __init__(self):
        self.head = None  # 头节点初始为空

    # 在尾部添加节点（方便构造链表）
    def append(self, val):
        new_node = ListNode(val)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    # 按索引删除节点
    def delete_at_index(self, index):
        # 如果链表为空 或 索引非法
        if not self.head or index < 0:
            return

        # 特殊情况：删除头节点
        if index == 0:
            self.head = self.head.next
            return

        # 找到 前驱节点（index-1 的位置）
        current = self.head
        for i in range(index - 1):
            # 如果索引超出链表长度
            if not current.next:
                return
            current = current.next

        # 如果当前节点的下一个节点不存在（索引超界）
        if not current.next:
            return

        # 关键：跳过要删除的节点
        current.next = current.next.next

    # 按值删除节点
    def delete_by_value(self, val):
        if not self.head:
            return

        # 特殊：头节点就是要删的值
        if self.head.val == val:
            self.head = self.head.next
            return

        current = self.head
        # 找到目标节点的前驱
        while current.next and current.next.val != val:
            current = current.next

        # 如果找到了，删除
        if current.next:
            current.next = current.next.next

    # 遍历打印链表
    def print_list(self):
        current = self.head
        while current.next:
            print(current.val, end=" → ")
            current = current.next
        print(current.val)
