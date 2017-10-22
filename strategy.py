""" Strategy. 
"""
import random
import math
from itertools import combinations

from result import WhiteResult, BlackResult
from player import Player   

def _index_to_alphabet(index):
    """ Convert the index to the alphabet.
    """
    return chr(ord("A") + index)

def get_strategy_map():
    """ Return the defined strategy modes.
    """
    _mode_dict = {"half_forseener": HalfForseener,
                  "master_wolf": OneMasterWolfStrategy, 
                  "master_wolves":MasterWolvesStrategy}
    return _mode_dict


def choose_strategy(mode_key):
    mode_dict = get_strategy_map()
    if mode_key is None:
        return Strategy
    if not mode_key in mode_dict:
        print("The corresponding strategy is not exisistent.", "mode", mode_key)
        print("Default strategy is returned.")
        return Strategy
    return mode_dict[mode_key]
        

class Strategy(object):
    """ Strategy for the problem.
    When you create the new strategy, you should derive this class.  
    """
    def __init__(self, villager_number, wolf_number, lunatic_number):
        self.villager_number = villager_number
        self.wolf_number = wolf_number
        self.lunatic_number = lunatic_number
        pass


    def is_result_coherent(self, index_to_player, villager_indices, wolf_indices, lunatic_indices):
        """ Check whether the result is  coherent or not. 

        :return: ``True``, if the result is coherent. Otherwise, ``False``.
        """
        def _coherent_check(p_result_dict): 
            for index_key, name_value in p_result_dict.items():
                if index_key in wolf_indices:
                    if name_value != BlackResult.get_id():
                        return False
                elif index_key in villager_indices:
                    if name_value != WhiteResult.get_id():
                        return False
                elif index_key in lunatic_indices:
                    if name_value != WhiteResult.get_id():
                        return False
                else:
                    raise ValueError("Invalid", index_key)
            return True

        assert len(villager_indices) == self.villager_number
        assert len(wolf_indices) == self.wolf_number
        assert len(lunatic_indices) == self.lunatic_number

        if all([_coherent_check(index_to_player[v_index].result)
               for v_index in villager_indices]):
            return True
        return False
        

    def get_coherent_cases(self, index_to_player):
        """ Return the cases where the results are coherent.

        :param index_person: :obj:`dict`. 
        :return: ``list``, in which each element is ``dict``.
                   which represents the (possible) coherent cases. 
        """

        coherent_ret_list = list()
        indices = list(range(len(index_to_player)))

        number_list = [self.villager_number, self.wolf_number, self.lunatic_number]
        for indices_list in _multiple_combination(indices, number_list):
            villager_indices, wolf_indices, lunatic_indices = indices_list
            if self.is_result_coherent(index_to_player, villager_indices, wolf_indices, lunatic_indices):
                row = dict()
                row["wolf_indices"] = wolf_indices
                coherent_ret_list.append(row)
        return coherent_ret_list


    def add_claim(self, index_to_player):
        """ Add the one claim so that the possible cases should be restricted. 

        :return: ``index_to_player``, into which one claim is added. 
        """
        from_index, to_index = self.choose_add_pair_randomly(index_to_player)
        claim_id = self.choose_claim_randomly(index_to_player, from_index, to_index)
        from_player = index_to_player[from_index]
        from_player.result[to_index] = claim_id
        return index_to_player


    def choose_add_pair_randomly(self, index_to_player):
        """ Choose the pair of players randomly at adding claims.  
        """
        from_target_indices = [index for index, player in index_to_player.items()
                              if not self.is_player_full_results(player)]
        from_index = random.choice(from_target_indices)
        from_player = index_to_player[from_index]

        current_indices = from_player.result.keys()
        to_target = [index for index in index_to_player.keys()
                     if index not in current_indices]
        to_index = random.choice(to_target)
        return from_index, to_index


    def delete_claim(self, index_to_player): 
        """ Delete the one claim so that the possible cases should be expanded. 
        Especially, this function is called when the possible case does not exist.
        """
        from_index, to_index = self.choose_delete_pair_randomly(index_to_player)

        del index_to_player[from_index].result[to_index]

        return index_to_player
    

    def choose_delete_pair_randomly(self, index_to_player):
        """ Choose the pair of players randomly at adding claims.  
        """
        from_target_indices = [index for index, player in index_to_player.items() 
                              if self.is_player_has_claims(player)]
        from_index = random.choice(from_target_indices)
        result_indices = list(index_to_player[from_index].result.keys())
        to_target = [index for index in result_indices if from_index != index]
        to_index = random.choice(to_target)
        return from_index, to_index


    def choose_claim_randomly(self, index_to_player, from_index, to_index):
        """ Choose the result claims stated by ***from_index** player.  
        Simply speaking, the result is selected randomly, however,clear illogical
        statements are avoided.

        :return: the id of result. 
        """
        from_player = index_to_player[from_index]
        black= len([key for key, value in
                   from_player.result.items() if value == BlackResult.get_id()])

        white= len([key for key, value in
                   from_player.result.items() if value == WhiteResult.get_id()])

        if self.wolf_number == black:
            return WhiteResult.get_id()

        if self.villager_number + self.lunatic_number == white:  
            return BlackResult.get_id()
        

        if random.random() <= 1/2:
            return WhiteResult.get_id()
        else:
            return BlackResult.get_id()


    def generate_problem(self, index_to_player, max_iteration):
        """ Generate the problem.
        :return: ``dict``, which represents answer.
        :func:`get_answer_line` must assure that 
        the return of this function convert to the appropriate string.
        At default setting, 
        ``dict`` as the element of the return of :func:`get_coherent_cases` is returned. 
        
        """

        for iter_number in range(max_iteration):
            coherent_list = self.get_coherent_cases(index_to_player)

            if len(coherent_list) == 0:
                index_to_player = self.delete_claim(index_to_player)
            elif len(coherent_list) > 1:
                index_to_player = self.add_claim(index_to_player)
            elif len(coherent_list) == 1:
                answer = coherent_list[0]
                return answer
        raise RuntimeError("Cannot generate the problem.")
    
    def get_answer_line(self, answer, lang="en"):
        """ Return the answer line.  
        """
        wolves = [_index_to_alphabet(elem) for elem in sorted(answer["wolf_indices"])]
        if lang == "en":
            answer_line = "Wolves:{0}".format(",".join(wolves))
        elif lang == "jp":
            answer_line = "狼:{0}".format(",".join(wolves))
        else:
            raise ValueError("Input language is invalid.")
        return answer_line

    def is_player_full_results(self, player):
        """ Return whether player's results are full or not.   
        """
        total_number = self.wolf_number + self.villager_number + self.lunatic_number
        return len(player.result) >= total_number

    def is_player_has_claims(self, player):
        return len(player.result) > 1


class HalfForseener(Strategy):
    """ Half of **villagers** and **wolves** are forseener
        and pretend to be forseener,
        respectively. 
    """

    def __init__(self, villager_number, wolf_number, lunatic_number):
        def _half_number(number):
            number = number / 2
            if random.random() < 1/2:
                return math.floor(number)
            return math.ceil(number)

        super().__init__(villager_number, wolf_number, lunatic_number)
        villager_forseener_number = _half_number(villager_number)
        wolf_forseener_number = _half_number(wolf_number)
        lunatic_forseener_number = _half_number(lunatic_number)

        total_forseeners = villager_forseener_number + wolf_forseener_number + lunatic_forseener_number
        wolf_non_forseener_number = wolf_number - wolf_forseener_number
        total_number = total_forseeners + wolf_non_forseener_number
        target_indices = range(total_number)
        p_list = _partition_sequence(target_indices,
                                    [villager_forseener_number, wolf_forseener_number, lunatic_forseener_number,
                                     wolf_non_forseener_number])
        self.villager_forseener_indices = p_list[0]
        self.wolf_forseener_indices = p_list[1]
        self.lunatic_forseener_indices = p_list[2]
        self.wolf_non_forseener_indices = p_list[3]


    def add_claim(self, index_to_player):
        """ Add the one claim so that the possible cases should be restricted. 

        :return: ``index_to_player``, into which one claim is added. 
        """
        def _is_forseener_target(index):
            return (index in self.villager_forseener_indices) or  \
                   (index in self.wolf_forseener_indices) or \
                   (index in self.lunatic_forseener_indices) 
        from_target_indices = [index for index, person in index_to_player.items()
                              if not self.is_player_full_results(person)]

        from_target_indices = [index for index in from_target_indices
                              if _is_forseener_target(index)]


        if not from_target_indices:
            return self.delete_claim(index_to_player)

        from_index = random.choice(from_target_indices)
        from_person = index_to_player[from_index]

        current_indices = from_person.result.keys()
        to_target = [index for index in index_to_player.keys() if index not in current_indices]
        to_index = random.choice(to_target)

        # For assumed villager_forseener, claims must be right. 
        if from_index in self.villager_forseener_indices:
            if to_index in self.wolf_forseener_indices:
                from_person.result[to_index] = BlackResult.get_id()
            elif to_index in self.wolf_non_forseener_indices:
                from_person.result[to_index] = BlackResult.get_id()
            else:
                from_person.result[to_index] = WhiteResult.get_id()
        else:
            if 0 <= random.random() <= 1/2:
                from_person.result[to_index] = WhiteResult.get_id()
            else:
                from_person.result[to_index] = BlackResult.get_id()
        return index_to_player



class MasterWolvesStrategy(Strategy):
    """ 
    Assure that all wolves' claims are right except oneself. 
    """
    def __init__(self, villager_number, wolf_number, lunatic_number):
        super().__init__(villager_number, wolf_number, lunatic_number)
        self.wolf_indices = range(wolf_number)
        self.villager_indices = range(wolf_number, wolf_number + villager_number)

    def add_claim(self, index_to_player):
        from_index, to_index = self.choose_add_pair_randomly(index_to_player)
        from_player = index_to_player[from_index]

        if from_index in self.wolf_indices or from_index in self.villager_indices:
            if to_index in self.wolf_indices:
                claim_id = BlackResult.get_id()
            else:
                claim_id = WhiteResult.get_id()
        else:
            # Strategy of lunatics.
            black= len([key for key, value in
                   from_player.result.items() if value == BlackResult.get_id()])

            if black == self.wolf_number:
                claim_id = WhiteResult.get_id()
            else:
                if to_index in self.wolf_indices:
                    claim_id = WhiteResult.get_id()
                else:
                    claim_id = BlackResult.get_id()

        from_player.result[to_index] = claim_id
        return index_to_player


class OneMasterWolfStrategy(Strategy):
    """ 
    Assure that at least one wolf exists such that his claims are right
    except himself. 
    """
    def __init__(self, villager_number, wolf_number, lunatic_number):
        super().__init__(villager_number, wolf_number, lunatic_number)
        self.master_wolf_index = 0 
        self.wolf_indices = range(wolf_number)
        self.villager_indices = range(wolf_number, wolf_number + villager_number)

    def add_claim(self, index_to_player):
        """ Add the one claim so that the possible cases should be restricted. 

        :return: ``index_to_player``, into which one claim is added. 
        """
        from_index, to_index = self.choose_add_pair_randomly(index_to_player)
        from_player = index_to_player[from_index]

        if from_index == self.master_wolf_index or from_index in self.villager_indices:
            if to_index in self.wolf_indices:
                claim_id = BlackResult.get_id()
            else:
                claim_id = WhiteResult.get_id()
        else:
            # Strategy of lunatics.
            black= len([key for key, value in
                   from_player.result.items() if value == BlackResult.get_id()])

            if black == self.wolf_number:
                claim_id = WhiteResult.get_id()
            else:
                if to_index in self.wolf_indices:
                    claim_id = WhiteResult.get_id()
                else:
                    claim_id = BlackResult.get_id()

        from_player.result[to_index] = claim_id
        return index_to_player

                
#Utility functions. 
def _multiple_combination(sequence, number_list):
    assert sum(number_list) <= len(sequence) 
    sequence = tuple(sequence)
    indices  = list(range(len(sequence)))

    def _inner(remain_indices, num_list, current_list):
        if not num_list:
            yield current_list
            return

        for c_indices in combinations(remain_indices, num_list[0]):
            candidate = [sequence[c_index] for c_index in c_indices]
            next_current_list = current_list + [candidate]
            next_remain_indices = [index for index in remain_indices if not index in c_indices]
            yield from  _inner(next_remain_indices, num_list[1:] , next_current_list)

    yield from _inner(indices, number_list, []) 

def _partition_sequence(sequence, number_list):
    assert len(sequence) == sum(number_list)
    result_list = list()
    accumulation = 0
    for number in number_list:
        list_elem = [sequence[accumulation + sub_index] for sub_index in range(number)]
        result_list.append(list_elem)
        accumulation += number
    return result_list


if __name__ == "__main__":
    # Easy test codes for utility functions. 
    for elem in _multiple_combination(["A", "B", "C", "D"], [2, 1]):
        print(elem)
    print(_partition_sequence(range(6), [1, 2, 3]))

