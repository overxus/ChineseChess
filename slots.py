import itertools
from typing import Tuple


class Slots:
    def __init__(self, num_x:int, num_y:int):
        self.num_x, self.num_y = num_x, num_y
        self.slots = [[None for _ in range(num_y)] for _ in range(num_x)]

    def __getitem__(self, idx:Tuple[int, int]):
        x, y = idx
        if 0 <= x < self.num_x and 0 <= y < self.num_y: return self.slots[x][y]
        else: raise IndexError(f"无效的索引({x}, {y}), 0 <= x < {self.num_x}, 0 <= y < {self.num_y}")

    def __setitem__(self, idx:Tuple[int, int], v):
        x, y = idx
        if 0 <= x < self.num_x and 0 <= y < self.num_y: self.slots[x][y] = v
        else: raise IndexError(f"无效的索引({x}, {y}), 0 <= x < {self.num_x}, 0 <= y < {self.num_y}")

    def items(self):
        """遍历slots中的所有非空元素"""
        for i, j in itertools.product(range(self.num_x), range(self.num_y)):
            if self.slots[i][j] != None:
                yield self.slots[i][j]
    
    def count_x(self, start, end, yaxis):
        """统计[(start, end), yaxis]间有多少非空元素"""
        start, end = min(start, end), max(start, end)
        counter = 0
        for i in range(start+1, end):
            if self.slots[i][yaxis] != None: counter += 1
        return counter
    
    def count_y(self, start, end, xaxis):
        """统计[xaxis, [start, end]]间有多少元素"""
        start, end = min(start, end), max(start, end)
        counter = 0
        for j in range(start+1, end):
            if self.slots[xaxis][j] != None: counter += 1
        return counter
    
    def move(self, pos_a:Tuple[int, int], pos_b:Tuple[int, int]):
        """将pos_a的元素移动到pos_b"""
        a_x, a_y = pos_a
        b_x, b_y = pos_b
        if self.slots[a_x][a_y] != None:
            self.slots[b_x][b_y] = self.slots[a_x][a_y]
            self.slots[a_x][a_y] = None
