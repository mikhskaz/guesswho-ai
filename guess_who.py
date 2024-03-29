"""CSC111 Winter 2023 Project: Guess Who Artifical Intelligence
This module contains the classes and necessary functions to execute
the backend of the classic game "Guess Who".
Some features:
https://chalkdustmagazine.com/blog/cracking-guess-board-game/
All characters:
https://www.joe.co.uk/life/ranking-guess-who-least-most-horny-193991
This file is Copyright (c) 2023 Annie Wang, Mikhail Skazhenyuk, Xinyuan Gu, Ximei Lin.
"""
from __future__ import annotations

import csv
import random
from dataclasses import dataclass

from typing import Optional

########################################################################
def load_person(person_tuple: tuple[str]) -> Person:
    """Returns a Person from the defined string of characteristics.
    Preconditions:
    - len(person_tuple) == 9
    """
    features_so_far = set()
    for p in person_tuple[1:]:
        features_so_far.add(p)
    person = Person(person_tuple[0], features_so_far)
    return person


def load_persons(file_name: str) -> list[Person]:
    """Function to load all features into a list of Person classes
    as determined in the file file_name.
    Precondition:
    - file_name != ''
    """
    persons_so_far = []

    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            row = tuple(row)
            person = load_person(row)
            persons_so_far.append(person)

    return persons_so_far


########################################################################
@dataclass
class Person:
    """The main class to represent each person in the game of GuessWho.
  Instance Attributes:
  - name: The person's name (for the final guess)
  - features: A set of all the person's features
  - up: Boolean whether the person has been guessed/eliminated or not.
  Representation Invariants:
  - self.features != set()
  """
    name: str
    features: set[str]
    up: bool

    def __init__(self, name: str, features: set[str], up: bool = True) -> None:
        """Initialize Person with given Instance Attributes. """

        self.name = name
        self.features = features
        self.up = up


class GuessWho:
    """The main class to run the game of GuessWho and represent its game_state.
    Instance Attributes:
    - guesses: A list representing the moves made by both players in order.
    - spies: A list representing the spies of each player (index 0 for player one, index 1 for player two)
    - players: A list of the players in the game
    Representation Invariants:
    - len(spies) == 2
    - spy is a valid person from the given file
     """
    players: dict[int, Player]
    process: list[str]
    candidates: dict[str, dict[str, str]]

    def __init__(self, players: list[Player], candidates: dict[str, dict[str, str]]) -> None:
        """ Initialize a GuessWho game with the two players"""
        self.candidates = candidates
        self.players = {1: players[0], 2: players[1]}
        self.process = []

    def get_winner(self) -> Optional[str]:
        """ return if there is a winner in the game and which player is the winner, with the guess1 by player1
        and guess2 by player2. Guess1 is the guess made by player1 and guess2 is the guess by player2.
        One of the player wins if :
            - The player successfully guesses the spy of the opponent.
            - The opponent has run out of the questions first。
        There is a tie under two circumstances:
            - Both guessers have guessed the spy of the opponent.
            - Both players have run out of questions to ask.
        """
        if not self.players[1].questions and not self.players[2].questions:
            return 'tie'
        elif not self.players[1].questions:
            return self.players[2].name
        elif not self.players[2].questions:
            return self.players[1].name
        elif len(self.players[1].candidates) == 1 or len(self.players[2].candidates) == 1:
            guess1 = self.players[1].make_guesses()
            guess2 = self.players[2].make_guesses()
            if (guess1 == self.players[1].spy) and (guess2 == self.players[2].spy):
                return 'tie'
            elif guess2 == self.players[1].spy:
                return self.players[2].name
            elif guess1 == self.players[2].spy:
                return self.players[1].name

    def whose_turn(self) -> int:
        """ return it's which player's turn to make a guess in this round of game
            Return value 2 means it's the second plyer's turn
            Return value 1 means it's the first player's turn
        """
        if len(self.process) == 0:
            return 1
        elif len(self.process) % 2 == 0:
            return 1
        else:
            return 2

    def return_answer(self, question: str, player_num: int) -> str:
        """ Answer yes or no to the questiont that one player has asked, regarding the spy that player_num has chosen
         """
        verify_with = self.players[player_num]
        return self.candidates[verify_with.spy][question]

    def copy_and_record_player_move(self, question: str) -> GuessWho:
        """Return a copy of this game state with the question.

        """
        new_game = self._copy()
        new_game.record_player_move(question)
        return new_game

    def _copy(self) -> GuessWho:
        """Return a copy of this game state."""
        new_game = GuessWho([player for player in self.players.values()], self.candidates)
        new_game.process.extend(self.process)
        return new_game

    def record_player_move(self, question: str) -> None:
        """Record the given question by the player.
        """
        self.process.append(question)

    def get_move_sequence(self) -> list[str]:
        """Return the move sequence made in this game.

        The returned list contains all questions that have been asked in the game.

        """
        return self.process


def create_candidates(file: str, num_cha: int) -> dict[str, dict[str, str]]:
    """Function to load all questions and answers for all candidates into a dictionary
       as determined in the file. Create the candidates dictionary with num_cha characters.

       Precondition:
       - file != ''
    """
    candidate_so_far = {}
    limited_candidates = {}
    b = 0

    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            d = {}
            for i in range(0, (len(row) - 1) // 2):
                d[row[2 * i + 1]] = row[2 * i + 2]
            candidate_so_far[row[0]] = d

        while b != num_cha:
            added_pair = random.choice(list(candidate_so_far.items()))
            if added_pair[0] not in limited_candidates:
                limited_candidates[added_pair[0]] = added_pair[1]
                b += 1
        return limited_candidates


def generate_all_possible_questions(file: str) -> list[str]:
    """ A function to generate all questions from the file. """
    all_questions = []

    with open(file) as csv_file:
        row = csv_file.readlines()[0]
        for i in range(1, len(row) // 2):
            all_questions.append(row[2 * i + 1] + '?')

    return all_questions[1:]


class Player:
    """ One of the player in the game
    Instance Attributes:
    - the name of the player.
    - questions : A list representing the questions the player has asked.
    - n : an integer determining if the player is the player 0 or player 1 in the game.
    - spy : The spy this player has chosen.
    Representation Invariants:
        - spy is a valid person from the given file
    """
    name: str
    questions: list[str]
    candidates: dict[str, dict[str, str]]
    spy: Optional[str] = None

    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str], name: str) -> None:
        """ create a new player for the game. n represets if this is the first/second player and characters represent
        the list of characters that this player can potentially choose to be the spy.
         """
        self.candidates = candidates
        self.questions = questions
        self.name = name

    def select_spy(self):
        """ The player selects the docstring"""
        self.spy = random.choice([name for name in self.candidates.keys()])

    def make_guesses(self) -> str:
        """ The player makes a guess of the opponent's spy based on the current state of the game. An abstract class
            that would be nimplemented differently based on different players we define.

         Preconditions:
             - game._whose_turn() == self.n
        """
        for name in self.candidates:
            return name

    def ask_questions(self) -> str:
        """ The player asks question about the characterstics of the spy based on the current state of the game.
         Preconditions:
            - game._whose_turn() == self.n
        """
        raise NotImplementedError

    def eliminate_candidates(self, generated_question: str, answer: str):
        """ Eliminating the candidates based on the answers to the question. """
        to_delete = []
        for k, v in self.candidates.items():
            if v[generated_question] != answer:
                to_delete.append(k)
        # print(f'{self.name} candidates {len(self.candidates)}')
        # print(f'to delete{to_delete}')
        for key in to_delete:
            del self.candidates[key]

    def eliminate_question(self, generated_question: str):
        """Eliminating the questions that has been asked."""
        self.questions.remove(generated_question)

    def copy(self) -> Player:
        """Return a copy of this player, used in generating gametree for CrazyPlayer"""
        raise NotImplementedError
