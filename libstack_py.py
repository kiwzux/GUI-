class Stack:
    def __init__(self):
        self._data = []
    
    def push(self, value):
        self._data.append(value)
        return True
    
    def pop(self):
        if self._data:
            return self._data.pop()
        raise IndexError("Стек пуст")
    
    def peek(self):
        if self._data:
            return self._data[-1]
        raise IndexError("Стек пуст")
    
    def is_empty(self):
        return len(self._data) == 0
    
    def size(self):
        return len(self._data)
    
    def get_all(self):
        return list(reversed(self._data))
    
    def clear(self):
        self._data.clear()