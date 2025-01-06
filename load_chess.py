from typing import Dict, List
import pygame
from chessman import *


CHESSMAN_RED:Dict[str, List[Chessman,]] = {
    "Rook": [Rook(team=True, init_pos=(0, 9)),
             Rook(team=True, init_pos=(8, 9))],
    "Knight": [Knight(team=True, init_pos=(1, 9)),
               Knight(team=True, init_pos=(7, 9))],
    "Elephant": [Elephant(team=True, init_pos=(2, 9)),
                 Elephant(team=True, init_pos=(6, 9))],
    "Mandarin": [Mandarin(team=True, init_pos=(3, 9)),
                 Mandarin(team=True, init_pos=(5, 9))],
    "King": [King(team=True, init_pos=(4, 9))],
    "Cannon": [Cannon(team=True, init_pos=(1, 7)),
               Cannon(team=True, init_pos=(7, 7))],
    "Pawn": [Pawn(team=True, init_pos=(0, 6)),
             Pawn(team=True, init_pos=(2, 6)),
             Pawn(team=True, init_pos=(4, 6)),
             Pawn(team=True, init_pos=(6, 6)),
             Pawn(team=True, init_pos=(8, 6))],
}

CHESSMAN_BLACK:Dict[str, List[Chessman,]] = {
    "Rook": [Rook(team=False, init_pos=(0, 0)),
             Rook(team=False, init_pos=(8, 0))],
    "Knight": [Knight(team=False, init_pos=(1, 0)),
               Knight(team=False, init_pos=(7, 0))],
    "Elephant": [Elephant(team=False, init_pos=(2, 0)),
                 Elephant(team=False, init_pos=(6, 0))],
    "Mandarin": [Mandarin(team=False, init_pos=(3, 0)),
                 Mandarin(team=False, init_pos=(5, 0))],
    "King": [King(team=False, init_pos=(4, 0))],
    "Cannon": [Cannon(team=False, init_pos=(1, 2)),
               Cannon(team=False, init_pos=(7, 2))],
    "Pawn": [Pawn(team=False, init_pos=(0, 3)),
             Pawn(team=False, init_pos=(2, 3)),
             Pawn(team=False, init_pos=(4, 3)),
             Pawn(team=False, init_pos=(6, 3)),
             Pawn(team=False, init_pos=(8, 3))],
}


def bind_slots(chessman_dict:dict):
    for _, v in chessman_dict.items():
        for chessman in v:
            SLOTS[chessman.X, chessman.Y] = chessman

from slots import Slots

SLOTS = Slots(9, 10)
bind_slots(CHESSMAN_RED)
bind_slots(CHESSMAN_BLACK)
