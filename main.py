"""CSC111 Winter 2023 Project: Guess Who Artifical Intelligence
This module contains the classes and necessary functions to execute
the frontend with the backend of the classic game "Guess Who".

The files interface.py and guess_who.py are combined in this file to work together.
artifical_intelligence is provided to play against as an opponent and the player
may choose which opponent to play against.

This file also contins the main function to run games and test performaces between AIs.

This file is Copyright (c) 2023 Annie Wang, Mikhail Skazhenyuk, Xinyuan Gu, Ximei Lin.
"""
from __future__ import annotations

import csv
from tkinter import *

import guess_who as GW
from guess_who import Player

import artificial_intelligence as AI
from artificial_intelligence import RandomPlayer, GreedyPlayer, PoorPlayer

import interface as IF

GAME_SETTINGS = {'question': ''}


###########################################################
# main function to run games and test performances between the GuessWho AIs that we've defined.
###########################################################

if __name__ == "__main__":
    IF.initiate()

if __name__ == '__main__':
    pass
    # Define data to initialize two players
    candidates = guess_who.create_candidates('data/questions.csv', 12)      # with 12 characters in each game
    candidates1 = candidates.copy()                                          # with 12 characters in each game
    questions = guess_who.generate_all_possible_questions('data/questions.csv')
########################
#  Sample call between GreedyPlayer and PoorPlayer.
########################
    # You may change the first parameter to determine how many games to run.
    # player1 = GreedyPlayer(candidates, questions)
    # player2 = PoorPlayer(candidates1, questions)
    # print(run_games(100, [player1, player2], 12, 'data/questions.csv', True, True))
    """NOTE: You can see GreedyPlayer has obviously better performance."""

########################
#  Sample call between GreedyPlayer and RandomPlayer.
########################
    # player1 = GreedyPlayer(candidates, questions)
    # player2 = RandomPlayer(candidates1, questions)
    # print(run_games(100, [player1, player2], 12, 'data/questions.csv', True, True))

    """NOTE:You should notive a more nuanced difference between performance of these two players compared to
     that between PoorPlayer and GreedyPlayer. Sometimes GreedyPlayer and RandoPlayer may even have the same
     winning probability!"""

########################
#  Sample call between PoorPlayer and CrazyPlayer.
########################
    # NOTE: we only use a small number of characters since it takes long to generate a complete GameTree.
#     candidates2 = guess_who.create_candidates('data/questions.csv', 8)
#     candidates2 = candidates2.copy()
#     questions1 = guess_who.generate_all_possible_questions('data/questions.csv')
#     player1 = PoorPlayer(candidates, questions)
#     print(run_crazy(25, player1, 8, 'data/questions.csv', True, True))

#     """ NOTE: You should notive that CrazyPlayer has significantly better performances than PoorPlayer, and the
#      difference is (mostly) bigger than that between GreedyPlayer and PoorPlayer. Run it for multiple times
#      you would find CrazyPlayer doesn't have the same performances in each game(there are times when its winning rate
#      is 90+ % but sometimes it's 70+%"""
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'extra-imports': ['tkinter', 'guess_who', 'features', 'artificial_intelligence', 'csv', 'interface'],
    #     'disable': ['forbidden-top-level-code',
    #                 'wildcard-import',
    #                 'too-many-branches',
    #                 'forbidden-global-variables',
    #                 'unused-argument',
    #                 'too-many-arguments',
    #                 'too-many-locals',
    #                 'unused-import'
    #                 ],
    #     'allowed-io': []
    # })
