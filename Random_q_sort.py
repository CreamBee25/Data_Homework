import random

def quick_sort_random(arr, left, right):
    if left >= right:
        return
    pivot_idx = random.randint(left, right)
    arr[pivot_idx], arr[right] = arr[right], arr[pivot_idx]
    pivot = arr[right]
    i = left - 1
    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    pivot_pos = i + 1
    quick_sort_random(arr, left, pivot_pos - 1)
    quick_sort_random(arr, pivot_pos + 1, right)

def quick_sort(arr):
    quick_sort_random(arr, 0, len(arr) - 1)
    return arr
