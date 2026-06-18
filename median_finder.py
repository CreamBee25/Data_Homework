"""
双堆求中位数 (Median Finder using Two Heaps)

数据结构: MedianFinder
- 使用两个堆来实现高效的中位数查询
- 大顶堆 (max_heap): 存储数据流中较小的一半数字
- 小顶堆 (min_heap): 存储数据流中较大的一半数字

时间复杂度:
- addNum(num):  O(log n)  — 堆的插入和删除
- findMedian(): O(1)      — 仅读取堆顶元素

空间复杂度: O(n) — 存储所有输入的数字
"""

import heapq


class MedianFinder:
    """
    双堆求中位数

    核心思想:
    - small: 大顶堆，存放较小的一半数字（Python heapq 是最小堆，通过取负数模拟大顶堆）
    - large: 小顶堆，存放较大的一半数字
    - 始终保持 len(small) == len(large) 或 len(small) == len(large) + 1
    - 这样中位数要么是 small 的堆顶（奇数个），要么是两堆顶的平均值（偶数个）
    """

    def __init__(self):
        """初始化两个堆"""
        # small: 大顶堆（存储较小的一半），Python 中用负数模拟
        #   堆顶是 small 中的最大值（即负数的最小值）
        self.small = []
        # large: 小顶堆（存储较大的一半）
        #   堆顶是 large 中的最小值
        self.large = []

    def addNum(self, num: int) -> None:
        """
        添加一个整数到数据结构中

        算法步骤:
        1. 先将数字加入 small（大顶堆），再从中取出最大值放入 large（小顶堆）
           这保证了 large 中的所有数字都 >= small 中的所有数字
        2. 如果 large 比 small 大，将 large 的最小值移回 small
           这保持了平衡条件: len(small) >= len(large)

        时间复杂度: O(log n) — 最多 4 次堆操作，每次 O(log n)

        参数:
            num: 要添加的整数
        """
        # 步骤1: 将数字推入 small（大顶堆），
        #        然后从 small 弹出最大值，推入 large（小顶堆）
        #        这样保证 small 中的元素 <= large 中的元素
        heapq.heappush(self.small, -num)                    # 入 small（取负 = 大顶堆）
        largest_in_small = -heapq.heappop(self.small)       # 弹出 small 最大值
        heapq.heappush(self.large, largest_in_small)        # 移入 large

        # 步骤2: 平衡两个堆的大小
        #        small 可以比 large 多一个元素（总数为奇数时）
        #        但 large 不能比 small 大
        if len(self.large) > len(self.small):
            # large 太大，将其最小值移到 small
            smallest_in_large = heapq.heappop(self.large)   # 弹出 large 最小值
            heapq.heappush(self.small, -smallest_in_large)  # 移入 small（取负 = 大顶堆）

    def findMedian(self) -> float:
        """
        返回当前所有数字的中位数

        规则:
        - 如果总数是奇数  (len(small) > len(large)): 中位数 = small 堆顶（较小一半的最大值）
        - 如果总数是偶数  (len(small) == len(large)): 中位数 = (small堆顶 + large堆顶) / 2

        时间复杂度: O(1) — 仅读取堆顶元素，不修改堆

        返回:
            当前中位数（浮点数）
        """
        if len(self.small) > len(self.large):
            # 奇数个元素: 中位数是小的一半中的最大值
            return float(-self.small[0])
        else:
            # 偶数个元素: 中位数是两半最值的平均数
            return (-self.small[0] + self.large[0]) / 2.0


# ============================================================
# 测试代码
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("测试: 双堆求中位数 (MedianFinder)")
    print("=" * 50)

    mf = MedianFinder()

    # 按照题目示例逐步测试
    test_data = [3, 1, 4, 1, 5]
    expected = [3, 2, 3, 2, 3]

    for i, num in enumerate(test_data):
        mf.addNum(num)
        median = mf.findMedian()
        status = "OK" if median == expected[i] else "FAIL"
        print(f"addNum({num}) → 中位数: {median}  期望: {expected[i]}  {status}")

    print("-" * 50)

    # 更详细的堆状态展示
    print("\n最终堆的状态:")
    print(f"  small (大顶堆, 较小一半): {[-x for x in mf.small]}")
    print(f"  large (小顶堆, 较大一半): {mf.large}")
    print(f"  最终中位数: {mf.findMedian()}")

    print("-" * 50)

    # 边界测试
    print("\n边界测试:")

    # 单元素
    mf2 = MedianFinder()
    mf2.addNum(42)
    print(f"  单元素 [42]: 中位数 = {mf2.findMedian()}  (期望: 42)")

    # 两个元素
    mf2.addNum(100)
    print(f"  两元素 [42, 100]: 中位数 = {mf2.findMedian()}  (期望: 71.0)")

    # 负数测试
    mf3 = MedianFinder()
    for n in [-1, -2, -3, -4, -5]:
        mf3.addNum(n)
    print(f"  全负数 [-5,-4,-3,-2,-1]: 中位数 = {mf3.findMedian()}  (期望: -3.0)")

    # 大量数据测试
    import random
    mf4 = MedianFinder()
    nums = [random.randint(1, 100) for _ in range(1000)]
    for n in nums:
        mf4.addNum(n)
    # 用排序验证
    sorted_nums = sorted(nums)
    n = len(sorted_nums)
    true_median = (sorted_nums[n // 2] + sorted_nums[(n - 1) // 2]) / 2.0
    print(f"  1000个随机数: 中位数 = {mf4.findMedian()}, 期望 = {true_median}  "
          f"{'OK' if mf4.findMedian() == true_median else 'FAIL'}")

    print("\n" + "=" * 50)
    print("测试完成!")
    print("=" * 50)
