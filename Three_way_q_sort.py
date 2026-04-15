import random
def quick_sort_three_way(arr, left, right):
    if left >= right:
        return
    pivot_idx = random.randint(left, right)
    arr[pivot_idx], arr[left] = arr[left], arr[pivot_idx]
    pivot = arr[left]
    
    lt = left       # [left, lt-1] < pivot
    gt = right      # [gt+1, right] > pivot
    i = left + 1    # [lt, i-1] == pivot, [i, gt] 待处理
    
    while i <= gt:
        if arr[i] < pivot:
            # 小于轴：交换到lt位置，lt和i都右移
            arr[i], arr[lt] = arr[lt], arr[i]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            # 大于轴：交换到gt位置，gt左移，i不变（交换后元素需重新判断）
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            # 等于轴：i右移
            i += 1
    quick_sort_three_way(arr, left, lt - 1)
    quick_sort_three_way(arr, gt + 1, right)

def three_way_quick_sort(arr):
    quick_sort_three_way(arr, 0, len(arr) - 1)
    return arr
