""" Create Werewolve's Puzzle.  

"""

wolf_number = 2
village_number = 4

import os, glob
from itertools import combinations
import random
from collections import namedtuple

class FResult(object):
    def __init__(self):
        pass
    @classmethod
    def get_id(cls):
        raise SyntaxError("Please Implement.")

class White_Result(FResult):
    def __init__(self):
        pass
    @classmethod
    def get_id(cls):
        return "white"

class Black_Result(FResult):
    def __init__(self):
        pass
    @classmethod
    def get_id(cls):
        return "black"



class Player(object):
    """ Abstract class for players.
    """
    def __init__(self, index):
        self.result = dict()
        self.index = index
        self.result[index] = White_Result.get_id()
    
    @classmethod
    def get_name(cls):
        raise SyntaxError("Please implement this function.")
    
    def add_result(self, index, result_name):
        self.result[index] = result_name

    def delete_result(self, target_index):  
        assert target_index in self.result
        assert target_index != self.index 

        del self.result[target_index]

    def refer_result(self):
        return self.result

    def has_result(self):
        return len(self.result) > 1

    def display_index_result(self, lang="en"):
        def _index_to_alphabet(number):
            return chr(ord("A") + number)
        indices = sorted(self.result.keys())
        indices = [index for index in indices if index != self.index]
        result_list = list()
        for index in indices:
            alphabet = _index_to_alphabet(index)
            result_id = self.result[index]
            if result_id == White_Result.get_id():
                result_list.append("{0}{1}".format(alphabet, "○"))
            elif result_id == Black_Result.get_id():
                result_list.append("{0}{1}".format(alphabet, "●"))
            else:
                raise ValueError(result_id)
        my_alphabet = _index_to_alphabet(self.index)

        if lang == "en":
            claim = "{0}'s claim".format(my_alphabet)
        elif lang == "jp":
            claim = "{0}の主張".format(my_alphabet)

        return "{0}:".format(claim) + ",".join(result_list)

    def replace_result_ids(self, replace_map):
        """ Replace the result and own ids.

        :param replace_map: prev_id: next_id.
        """
        self.index = replace_map[self.index]
        revised_result = dict()
        for prev_id, result_id in self.result.items():
            next_id = replace_map[prev_id]
            revised_result[next_id] = result_id
        self.result = revised_result
        self.result[self.index] = White_Result.get_id()
        

class Wolf(Player):
    """ Wolf.
    """
    def __init__(self, index):
        super(Wolf, self)
        self.result = dict()
        self.result[index] = White_Result.get_id()
        self.index = index

    def get_name(self):
        return "wolf"
    pass

class Forseener(Player):
    """ Forseener.
    """
    def __init__(self, index):
        super(Forseener, self)
        self.result = dict()
        self.result[index] = White_Result.get_id()
        self.index = index

    @classmethod
    def get_name(cls):
        return "forseener"

def generate_answer(f, w):
    """ Generate the answer.

    :param f: the number of forseener. 
    :param w: the number of wolf. 
    :return: the list of Players.  
    """
    answer_list = list()
    answer_list += [Forseener(index) for index in range(f)] 
    answer_list += [Wolf(len(answer_list) + index ) for index in range(w)] 
    return answer_list


def is_result_coherent(index_to_person, forseener_indices, wolf_indices):
    def _coherent_check(p_result_dict): 
        for index_key, name_value in p_result_dict.items():
            if index_key in wolf_indices:
                if name_value != Black_Result.get_id():
                    return False
            elif index_key in forseener_indices:
                if name_value != White_Result.get_id():
                    return False
            else:
                raise ValueError("Invalid", index_key)
        return True


    assert len(forseener_indices) == village_number
    assert len(wolf_indices) == wolf_number

    for f_index in forseener_indices:
        f_result = index_to_person[f_index].result
        if _coherent_check(f_result) is False:
            return False
    return True

def get_coherent_cases(index_to_person):
    """ Return the cases where the results are coherent.

    :param index_person: :obj:`dict`. 
    :return :obj:`list`: whose elem is :obj:`dict`.
                - refer to the **wolf_indices** and *forseener_indices*.
    """

    coherent_ret_list = list()
    indices = list(range(wolf_number + village_number))
    for candidate in combinations(indices, wolf_number):
        wolf_indices = [index for index in indices if index in candidate]
        forseener_indices = [index for index in indices if index not in candidate]

        if is_result_coherent(index_to_person, forseener_indices, wolf_indices):
            row = dict()
            row["wolf_indices"] = wolf_indices
            row["forseener_indices"] = forseener_indices
            coherent_ret_list.append(row)
    return coherent_ret_list

def random_add_result(index_to_person):
    """ Strategy to restrict the possibility. 
    """
    from_target_indices = [index for index, person in index_to_person.items()
                          if len(person.result) < wolf_number + village_number]
    from_index = random.choice(from_target_indices)
    from_person = index_to_person[from_index]
    current_indices = from_person.result.keys()
    to_target = [index for index in index_to_person.keys() if from_index != index
            and index not in current_indices]
    to_index = random.choice(to_target)
    if 0 <= random.random() <= 1/2:
        index_to_person[from_index].add_result(to_index, White_Result.get_id())
    else:
        index_to_person[from_index].add_result(to_index, Black_Result.get_id())
    return index_to_person

def random_delete_result(index_to_person):

    """ Strategy to loose the restriction.  
    """
    # The target should have result except himself.  
    target_indices = [index for index, person in index_to_person.items() if len(person.result) > 1]

    from_index = random.choice(target_indices)
    result_indices = list(index_to_person[from_index].result.keys())
    to_target = [index for index in result_indices if from_index != index]
    to_index = random.choice(to_target)

    index_to_person[from_index].delete_result(to_index)

    return index_to_person


def assort_person_id(index_to_person):
    """ Sort the person's id, by the order of the number of claims. 

    :return: the changed index_to_person.
    
    """
    indices = index_to_person.keys()
    indices = sorted(indices,
                    key=lambda index: len(index_to_person[index].result.keys()),
                    reverse=True)

    replace_map = {original_id: index for index, original_id 
                   in enumerate(indices)}  

    revised_index_to_person = dict()
    for prev_index, person in index_to_person.items():
        person.replace_result_ids(replace_map)

        next_index = replace_map[prev_index]
        revised_index_to_person[next_index] = person
    
    return revised_index_to_person

def _index_to_alphabet(index):
    return chr(ord("A") + index)

def display_problems(village_number, wolf_number, index_to_person, lang="en"):
    text_lines = list()
    persons = len(index_to_person)
    if lang == "en":
        first_line = "## Problem"
        second_line = "Roles:Villagers/Wolves={v}/{w}, PL:{first_pl}~{last_pl}"\
                     .format(v=village_number, 
                             w=wolf_number, 
                             first_pl='A',
                             last_pl=_index_to_alphabet(persons-1))
        third_line = "### Player's claims"
    elif lang == "jp":
        first_line = "## 問題"
        second_line = "内訳:村陣営/狼={v}/{w}, PL:{first_pl}~{last_pl}"\
                     .format(v=village_number, 
                             w=wolf_number,
                             first_pl='A',
                             last_pl=_index_to_alphabet(persons-1))

        third_line = "### 各PLの主張"
    else:
        raise ValueError("Specification of lang is invalid.", lang) 
    text_lines += [first_line, second_line, third_line]

    indices = sorted(index_to_person.keys(),
                    key=lambda index: len(index_to_person[index].result),
                    reverse=True)
    for index  in indices:
        person = index_to_person[index]
        if person.has_result():
            text_lines.append(person.display_index_result(lang))
    return "\n".join(text_lines)

def display_answers(answer_row, lang="en"):
    def _index_to_alphabet(index):
        return chr(ord("A") + index)

    text_lines = list()
    villagers = [_index_to_alphabet(elem) for elem in sorted(answer_row["forseener_indices"])]
    wolves = [_index_to_alphabet(elem) for elem in sorted(answer_row["wolf_indices"])]
    if lang == "en":
        first_line = "## Answer  "
        wolf_line = "Wolves={0}".format(",".join(wolves))
    elif lang == "jp":
        first_line = "## 解答  "
        wolf_line = "Wolves={0}".format(",".join(wolves))
    else:
        raise ValueError("Invalid lang", lang)
    
    text_lines += [first_line, wolf_line]
    return "\n".join(text_lines)


if __name__ ==  "__main__":
    lang = "en"
    result = generate_answer(wolf_number, village_number)
    index_to_person = {index:elem for index, elem in enumerate(result)}

    max_iteration = 100
    for iter_number in range(max_iteration):

        ret_list = get_coherent_cases(index_to_person)

        for row in ret_list:
            wolf_indices = row["wolf_indices"]
            forseener_indices = row["forseener_indices"]

        #print("length", len(ret_list))

        if len(ret_list) == 0:
            random_delete_result(index_to_person)
        elif len(ret_list) > 1:
            random_add_result(index_to_person)
        else:
            break


    index_to_person = assort_person_id(index_to_person)
    ret_list = get_coherent_cases(index_to_person)
    #assert len(ret_list) == 1
    answer_row = ret_list[0]
    #print(answer_row) 
    texts = display_problems(village_number, wolf_number, index_to_person, lang)
    print(texts);
    texts = display_answers(answer_row, lang)
    print(texts);exit(0)
    str_list = list()
