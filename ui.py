import itertools
import math
import sys
from typing import Tuple
import pygame
from load_chess import SLOTS

pygame.init()


def to_real_pos(chessboard_pos: Tuple[int, int]):
    """将棋子坐标转化为用于绘制的物理坐标"""
    x, y = chessboard_pos
    if y <= 4:  # 棋子位于棋盘的上方
        x_pos = 4 + x * 72
        y_pos = 2 + y * 72
        return x_pos, y_pos
    else:  # 棋子位于棋盘的下方
        x_pos = 4 + x * 72
        y_pos = 364 + (y - 5) * 72
        return x_pos, y_pos


def to_chessboard_pos(real_pos: Tuple[int, int]):
    """将物理坐标(通常通过点击鼠标左键获取)转化为棋盘上的棋子坐标"""
    x_pos, y_pos = real_pos
    x_rel, y_rel = -1, -1
    if 4 <= x_pos < 4 + 10 * 72:
        x_rel = math.floor((x_pos - 4) / 72)
        if 2 <= y_pos <= 2 + 6 * 72:
            y_rel = math.floor((y_pos - 2) / 72)
        elif 364 <= y_pos <= 364 + 6 * 72:
            y_rel = math.floor((y_pos - 364) / 72) + 5
    return x_rel, y_rel


class ChessBoard:
    def __init__(self) -> None:
        pygame.display.set_caption("中国象棋")
        self.display = pygame.display.set_mode((665, 737))
        self.image_chessboard = pygame.image.load("./assets/wood.jpg")
        self.NUM_CHESSMAN_X = 9
        self.NUM_CHESSMAN_Y = 10
        self.team = True  # 当前棋手, True为红方, False为黑方
        self.slots = SLOTS
        self.current = None  # 当前被选中的棋子坐标

    def render(self):
        self.display.blit(self.image_chessboard, (0, 0))
        for idx in itertools.product(range(self.NUM_CHESSMAN_X), range(self.NUM_CHESSMAN_Y)):
            if self.slots[idx] is not None:
                self.slots[idx].render(self.display, to_real_pos(idx))  # type:ignore

        pygame.display.flip()

    def goto(self, pos: Tuple[int, int]):
        """pos为鼠标左键时所在的棋盘坐标，本函数处理相关逻辑"""
        target_chessman = self.slots[pos]  # 鼠标点击处的棋子
        if target_chessman is None:  # 目标处没有棋子
            if self.current and self.current.reachable(pos, self.slots):  # 当前有选中的棋子且棋子可到达pos处
                self.current.selected = False  # 取消选中
                self.slots.move(self.current.get_pos(), pos)  # 移动棋子
                self.current.set_pos(pos)  # 更新当前棋子的坐标
                self.current = None
                self.team = not self.team  # 更新下棋的一方
                # print(f"更新棋子位置：当前队伍：{self.team}")
            elif self.current:  # 当前有选中的棋子，但无法到达pos处
                self.current.selected = False  # 取消选中
                self.current = None
                # print(f"{self.team}: 取消当前棋子的选中")
            else:
                return None  # 当前无选中的棋子
        else:  # 目标处有棋子
            if not self.current:  # 当前无选中的棋子
                if target_chessman.team == self.team:  # 当前玩家选择本方棋子
                    self.current = target_chessman
                    self.current.selected = True
                    # print(f"{self.team}: 选择本方棋子")
                else:
                    return None
            else:  # 当前有被选中的棋子
                if self.current.reachable(pos,
                                          self.slots) and self.current.team != target_chessman.team:  # 当前棋子可以到达pos处
                    self.current.selected = False  # 取消选中
                    self.slots.move(self.current.get_pos(), pos)  # 吃掉pos处的敌方棋子
                    self.current.set_pos(pos)  # 更新移动后棋子的坐标
                    self.current = None
                    self.team = not self.team  # 更新队伍
                    # print(f"吃掉棋子：当前队伍{self.team}")
                elif self.current.team == target_chessman.team:  # 目标处有不可达的同类棋子
                    self.current.selected = False  # 更新选中的棋子
                    self.current = target_chessman
                    self.current.selected = True
                    # print(f"{self.team}: 选中另一个棋子")
                else:  # 取消当前选中
                    self.current.selected = False
                    self.current = None
                    # print(f"{self.team}: 取消当前选中")
        return None

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                x_rel, y_rel = to_chessboard_pos(event.pos)
                if 0 <= x_rel < self.NUM_CHESSMAN_X and 0 <= y_rel < self.NUM_CHESSMAN_Y:
                    self.goto((x_rel, y_rel))

    def mainloop(self):
        clock = pygame.time.Clock()
        while True:
            self.render()
            self.events()
            clock.tick(50)


if __name__ == "__main__":
    board = ChessBoard()
    board.mainloop()
