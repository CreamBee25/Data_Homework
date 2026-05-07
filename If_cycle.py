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

    def has_cycle(self):
        # 快慢指针：慢指针走1步，快指针走2步
        slow = self.head
        fast = self.head
        
        # 循环条件：快指针和快指针的下一个节点都不为空
        while fast and fast.next:
            slow = slow.next         # 慢指针走1步
            fast = fast.next.next    # 快指针走2步
            
            # 快慢指针相遇 → 存在环
            if slow == fast:
                return True
        # 快指针走到链表末尾 → 无环
        return False
