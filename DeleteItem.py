from typing import Iterable, Any

class DeleteItem:
    """
    在列表中删除元素
    """
    def __init__(self,iterable: Iterable[Any]):
        """
        __init__ 的 Docstring
        :param iterable: 可迭代对象，删除其中元素
        """
        self.iterable = list(iterable)

    def delete(self,index_to_delete:int):
        """
        delete 的 Docstring
        
        :param index_to_delete: 删除的索引
        """
        length_of_iterable:int = len(self.iterable)
        if index_to_delete >= length_of_iterable or index_to_delete < -length_of_iterable:
            raise IndexError
        for i in range(index_to_delete,length_of_iterable-1):
            self.iterable[i] = self.iterable[i+1]
        del self.iterable[length_of_iterable-1]
        return self.iterable
