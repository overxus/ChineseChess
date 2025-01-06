from typing import Tuple
import pygame
from slots import Slots


class Chessman:
    def __init__(self, name:str, team:bool = True, code:str = 'X', init_pos:Tuple[int, int] = (0, 0)):
        self.name = name  # 棋子的名称
        self.team = team  # 棋子属于哪个队伍. True: 红方, False: 黑方
        self.code = code  # 用于确定棋子的单个字母(便于加载网上下载的图片文件)
        self.X, self.Y = init_pos  # 棋子的坐标
        self.selected = False  # 当前棋子是否被选中
        color_code = 'R' if self.team == True else 'B'
        self.img = pygame.image.load(f"./assets/Chessman/{color_code}{self.code}.GIF")
        self.img_selected = pygame.image.load(f"./assets/Chessman/{color_code}{self.code}S.GIF")
    
    def steps(self):
        """生成所有可行的移动动作: Iterator[tuple(int, int), ...]"""
        yield (0, 0)
    
    def reachable(self, pos:Tuple[int, int], slots:Slots):
        """判断当前棋子的下一步是否可以到达pos"""
        return False
    
    def render(self, display, pos:Tuple[int, int]):
        if not self.selected:
            display.blit(self.img, pos)
        else: display.blit(self.img_selected, pos)
    
    def get_pos(self):
        return self.X, self.Y
    
    def set_pos(self, pos:Tuple[int, int]):
        self.X, self.Y = pos


class Rook(Chessman):
    """车"""
    def __init__(self, team: bool = True, init_pos: Tuple[int, int] = (0, 0)):
        super().__init__("车", team=team, code='R', init_pos=init_pos)
    
    def reachable(self, pos:Tuple[int, int], slots:Slots):
        xpos, ypos = pos
        return ((self.X == xpos and slots.count_y(self.Y, ypos, xaxis=xpos) == 0) or 
                (self.Y == ypos and slots.count_x(self.X, xpos, yaxis=ypos) == 0))
    

class Knight(Chessman):
    """马"""
    def __init__(self, team: bool = True, init_pos: Tuple[int, int] = (0, 0)):
        super().__init__("马", team=team, code='N', init_pos=init_pos)
    
    def reachable(self, pos: Tuple[int, int], slots:Slots):
        xpos, ypos = pos
        xbias, ybias = 0, 0  # 阻挡马跳跃的棋子
        if self.Y - ypos == 2:
            if abs(xpos - self.X) == 1: xbias, ybias = self.X, self.Y - 1
            else: return False
        elif self.Y - ypos == -2:
            if abs(xpos - self.X) == 1: xbias, ybias = self.X, self.Y + 1
            else: return False
        elif self.X - xpos == 2:
            if abs(ypos - self.Y) == 1: xbias, ybias = self.X - 1, self.Y
            else: return False
        elif self.X - xpos == -2:
            if abs(ypos - self.Y) == 1: xbias, ybias = self.X + 1, self.Y
        else: return False
        return slots[xbias, ybias] == None

    
class Elephant(Chessman):
    """象"""
    def __init__(self, team: bool = True, init_pos: Tuple[int, int] = (0, 0)):
        super().__init__("象", team=team, code='B', init_pos=init_pos)
    
    def reachable(self, pos: Tuple[int, int], slots:Slots):
        xpos, ypos = pos
        xdis = abs(xpos - self.X)
        ydis = abs(ypos - self.Y)
        if xdis == 2 and ydis == 2:
            xbias, ybias = (xpos + self.X) // 2, (ypos + self.Y) // 2  # 阻挡象跳跃的棋子
            return (slots[xbias, ybias] == None and
                    ((self.team == True and ypos >= 5) or  #象不能越过边界, 红方棋子, ypos >= 5 
                    (self.team == False and ypos <= 4)))   #黑方棋子, ypos <= 4
        else: return False


class Mandarin(Chessman):
    """士"""
    def __init__(self, team: bool = True, init_pos: Tuple[int, int] = (0, 0)):
        super().__init__("士", team=team, code='A', init_pos=init_pos)
    
    def reachable(self, pos: Tuple[int, int], slots:Slots):
        xpos, ypos = pos
        xbias = abs(xpos - self.X)
        ybias = abs(ypos - self.Y)
        return ((xbias == 1 and ybias == 1) and 
                (3 <= xpos <= 5) and  # 士的X边界只能在[3, 5]
                ((self.team == True and 7 <= ypos <= 9) or  #红方士的Y边界在[7, 9] 
                 (self.team == False and 0 <= ypos <= 2)))  #黑方士的Y边界在[0, 2]


class King(Chessman):
    """将"""
    def __init__(self, team: bool = True, init_pos: Tuple[int, int] = (0, 0)):
        super().__init__("将", team=team, code='K', init_pos=init_pos)
    
    def reachable(self, pos: Tuple[int, int], slots:Slots):
        xpos, ypos = pos
        x_legal = (3 <= xpos <= 5)
        y_legal = (self.team and 7 <= ypos <= 9) or (not self.team and 0 <= ypos <= 2)
        return x_legal and y_legal


class Cannon(Chessman):
    """炮"""
    def __init__(self, team: bool = True, init_pos: Tuple[int, int] = (0, 0)):
        super().__init__("炮", team=team, code='C', init_pos=init_pos)
    
    def reachable(self, pos: Tuple[int, int], slots:Slots):
        xpos, ypos = pos
        if self.X == xpos:  # 在Y方向移动
            num_inner_chessman = slots.count_y(self.Y, ypos, xaxis=xpos)
            return num_inner_chessman == 0 or num_inner_chessman == 1
        elif self.Y == ypos:  # 在X方向移动
            num_inner_chessman = slots.count_x(self.X, xpos, yaxis=ypos)
            return num_inner_chessman == 0 or num_inner_chessman == 1
        else: return None


class Pawn(Chessman):
    """卒"""
    def __init__(self, team: bool = True, init_pos: Tuple[int, int] = (0, 0)):
        super().__init__("卒", team=team, code='P', init_pos=init_pos)
    
    def reachable(self, pos: Tuple[int, int], slots:Slots):
        xpos, ypos = pos
        if self.team: #红方棋子
            return (xpos == self.X and ypos == self.Y - 1) or (ypos <= 4 and abs(xpos - self.X) == 1 and ypos == self.Y)
        else:
            return (xpos == self.X and ypos == self.Y + 1) or (ypos >= 5 and abs(xpos - self.X) == 1 and ypos == self.Y)
