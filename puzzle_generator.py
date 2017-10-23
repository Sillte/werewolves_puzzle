""" Create Werewolve's Puzzle.

"""
import argparse

from result import WhiteResult, BlackResult
from player import Player
import strategy


def _index_to_alphabet(index):
    """ Convert the index to the alphabet.
    """
    return chr(ord("A") + index)


class PuzzleGenereator(object):
    """ The generator of puzzle.

    :param villager_number: the number of villagers.
    :param wolf_number: the number of wolves.
    :param lunatic_number: the number of lunatics.
    :param lang: language.
    :param strategy_mode: the mode of generation. 
    """
    def __init__(self, villager_number, wolf_number, lunatic_number,
                 lang="en", strategy_mode=None):
        self.villager_number = villager_number
        self.wolf_number = wolf_number
        self.lunatic_number = lunatic_number

        if villager_number <= wolf_number + lunatic_number:
            raise ValueError("villager team  MUST be larger than the wolf one.")
        self.lang = lang.lower(); assert self.lang in ["en", "jp"] 

        self.index_to_player = self._initialize_players()
        self.answer = None
        strategy_class = strategy.choose_strategy(strategy_mode)
        self.strategy = strategy_class(villager_number, wolf_number, lunatic_number)

    def generate_problem(self, max_iteration=100):
        """ Generate the problems.

        :param max_iteration: the maximum iterations.  
        :return: ``True``, if generated, otherwise, ``False``. 
        """
        self.answer = self.strategy.generate_problem(self.index_to_player, max_iteration)
        self.index_to_player = self._revise_person_id(self.index_to_player)
        self.answer = self.strategy.generate_problem(self.index_to_player, 1)
        
    def display_problems(self):
        """ Display the problems.
        """
        intro_text = self._create_introduction() 
        claims_text = self._create_claims()
        return "\n".join([intro_text, claims_text])

    def display_answers(self):
        """ Display the answers.
        """
        assert self.answer
        if self.lang == "en":
            first_line = "## Answer  "
        elif self.lang == "jp":
            first_line = "## 解答  "
        answer_line = self.strategy.get_answer_line(self.answer, self.lang)
        return "\n".join([first_line, answer_line])
    
    def _initialize_players(self):
        total_players = self.villager_number + self.wolf_number + self.lunatic_number
        player_list = [Player(index) for index in range(total_players)]
        index_to_player = {index: elem for index, elem in enumerate(player_list)}
                
        return index_to_player

    def _create_introduction(self):

        person_number = len(self.index_to_player)
        if self.lang == "en":
            first_line = "## Problem"
            if self.lunatic_number == 0:
                role_line = "Roles:Villager/Wolf={v}/{w}".format(v=self.villager_number,
                                                                 w=self.wolf_number)
            else:
                role_line = "Roles:Villager/Wolf/Lunatic={v}/{w}/{l}".format(v=self.villager_number,
                                                                             w=self.wolf_number,
                                                                             l=self.lunatic_number)
            player_line = "PL:{first_pl}-{last_pl}".format(first_pl="A",
                                                           last_pl=_index_to_alphabet(person_number - 1))
            second_line = role_line + ", " + player_line
        elif self.lang == "jp":
            first_line = "## 問題"
            if self.lunatic_number == 0:
                role_line = "内訳:村陣営/狼={v}/{w}".format(v=self.villager_number,
                                                            w=self.wolf_number)
            else:
                role_line = "内訳:村陣営/狼/狂={v}/{w}/{l}".format(v=self.villager_number,
                                                                   w=self.wolf_number,
                                                                   l=self.lunatic_number)
            player_line = "PL:{first_pl}-{last_pl}".format(first_pl="A",
                                                           last_pl=_index_to_alphabet(person_number - 1))
            second_line = role_line + ", " + player_line

        return "\n".join([first_line, second_line])

    def _create_claims(self):
        def _has_result(person):
            return len(person.result) > 1

        indices = sorted(self.index_to_player.keys(),
                         key=lambda index: len(self.index_to_player[index].result),
                         reverse=True)

        text_lines = list()
        if self.lang == "en":
            text_lines.append("### Player's claims")
        elif self.lang == "jp":
            text_lines.append("### 各PLの主張")
        else:
            raise ValueError("Invalid language.", self.lang)

        text_lines += [_create_player_claim(self.index_to_player[index], self.lang)
                       for index in indices 
                       if _has_result(self.index_to_player[index]) is True]

        return "\n".join(text_lines)

    def _revise_person_id(self, index_to_player):
        """ Sort the persons' id, by the order of the number of claims. 

        :return: the changed index_to_player.
        
        """
        def _replace_player_result_ids(player, replace_map):
            player.index = replace_map[player.index]
            revised_result = dict()
            revised_result = {replace_map[prev_id]: result_id
                              for prev_id, result_id in player.result.items()}
            player.result = revised_result
            player.result[player.index] = WhiteResult.get_id()
            return player

        indices = self.index_to_player.keys()
        indices = sorted(indices,
                         key=lambda index: len(self.index_to_player[index].result.keys()),
                         reverse=True)

        replace_map = {original_id: index for index, original_id 
                       in enumerate(indices)}  

        revised_index_to_player = dict()
        for prev_index, person in self.index_to_player.items():
            person = _replace_player_result_ids(person, replace_map)

            next_index = replace_map[prev_index]
            revised_index_to_player[next_index] = person
        
        return revised_index_to_player


def _create_player_claim(person, lang="en"):
    def _index_to_result(index):
        alphabet = _index_to_alphabet(index)
        result_id = person.result[index]
        string_dict = {WhiteResult.get_id(): "○", BlackResult.get_id(): "●"}
        result_string = string_dict[result_id]
        return "{0}{1}".format(alphabet, result_string)

    indices = sorted(person.result.keys())
    indices = [index for index in indices if index != person.index]
    result_list = [_index_to_result(index) for index in indices]

    my_alphabet = _index_to_alphabet(person.index)

    if lang == "en":
        claim = "{0}'s claim".format(my_alphabet)
    elif lang == "jp":
        claim = "{0}の主張".format(my_alphabet)
    return "{0}:".format(claim) + ",".join(result_list)


def create_parser():
    """ Create argparser.
    """
    parser = argparse.ArgumentParser(description="Werewolves' Puzzle Generator.")
    parser.add_argument('-villager', '-v', type=int,
                        help="the number of villagers", default=4)

    parser.add_argument('-wolf', '-w', type=int,
                        help="the number of wolves", default=1)

    parser.add_argument('-lunatics', '-l', type=int,
                        help="the number of lunatics", default=2)

    parser.add_argument('-lang', type=str,
                        help="the language", default="en", choices=['en', 'jp'])

    parser.add_argument('-max_iteration', type=int,
                        help="the maximum iterations for generator",
                        default=100)
    mode_keys = strategy.get_strategy_map().keys()
    parser.add_argument('-strategy_mode', default=None,
                        help="the strategy_mode", choices=list(mode_keys) + [None])

    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    villager_number = args.villager
    wolf_number = args.wolf
    lunatic_number = args.lunatics
    lang = args.lang
    max_iter = args.max_iteration
    strategy_mode = args.strategy_mode

    puzzle_generator = PuzzleGenereator(villager_number, wolf_number, lunatic_number,
                                        lang, strategy_mode) 
    puzzle_generator.generate_problem(max_iteration=max_iter)
    problem_text = puzzle_generator.display_problems()
    answer_text = puzzle_generator.display_answers()
    print(problem_text)
    print(answer_text)
