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

    def print_list(self):
        current = self.head
        while current.next:
            print(current.val, end=" → ")
            current = current.next
        print(current.val)

    def reverse(self):
        prev = None
        curr = self.head  # 从链表头开始遍历
        while curr:
            next_temp = curr.next  # 暂存下一个节点
            curr.next = prev       # 反转指针
            prev = curr            # 移动prev
            curr = next_temp       # 移动curr
        self.head = prev  # 反转后，头节点更新为prev
