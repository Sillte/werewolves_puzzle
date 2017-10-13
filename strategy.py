""" Strategy. 
"""
import random
from itertools import combinations

from result import WhiteResult, BlackResult
from player import Wolf, Villager

def _index_to_alphabet(index):
    """ Convert the index to the alphabet.
    """
    return chr(ord("A") + index)


class Strategy(object):
    """ Strategy for the problem.
    When you create the new strategy, you should derive this class.  
    """
    def __init__(self, villager_number, wolf_number):
        self.villager_number = villager_number
        self.wolf_number = wolf_number
        pass

    def is_result_coherent(self, index_to_person, villager_indices, wolf_indices):
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
                else:
                    raise ValueError("Invalid", index_key)
            return True

        assert len(villager_indices) == self.villager_number
        assert len(wolf_indices) == self.wolf_number

        ## When Lunatics is added, revise this. 
        if all([_coherent_check(index_to_person[v_index].result)
               for v_index in villager_indices]):
            return True
        return False
        

    def get_coherent_cases(self, index_to_person):
        """ Return the cases where the results are coherent.

        :param index_person: :obj:`dict`. 
        :return: ``list``, in which each element is ``dict``.
                   which represents the (possible) coherent cases. 
        """

        coherent_ret_list = list()
        indices = list(range(len(index_to_person)))
        # When lunatics are added, please revise here.  
        for candidate in combinations(indices, self.wolf_number):
            wolf_indices = [index for index in indices if index in candidate]
            forseener_indices = [index for index in indices if index not in candidate]

            if self.is_result_coherent(index_to_person, forseener_indices, wolf_indices):
                row = dict()
                row["wolf_indices"] = wolf_indices
                coherent_ret_list.append(row)
        return coherent_ret_list


    def add_claim(self, index_to_person):
        """ Add the one claim so that the possible cases should be restricted. 

        :return: ``index_to_person``, into which one claim is added. 
        """
        from_target_indices = [index for index, person in index_to_person.items()
                              if len(person.result) < self.wolf_number + self.villager_number]
        from_index = random.choice(from_target_indices)
        from_person = index_to_person[from_index]
        current_indices = from_person.result.keys()
        to_target = [index for index in index_to_person.keys() if from_index != index
                and index not in current_indices]
        to_index = random.choice(to_target)
        if 0 <= random.random() <= 1/2:
            index_to_person[from_index].result[to_index] = WhiteResult.get_id()
        else:
            index_to_person[from_index].result[to_index] = BlackResult.get_id()
        return index_to_person


    def delete_claim(self, index_to_person): 
        """ Delete the one claim so that the possible cases should be expanded. 
        Especially, this function is called when the possible case does not exist.
        """

        # The target should have result except himself.  
        target_indices = [index for index, person in index_to_person.items() if len(person.result) > 1]

        from_index = random.choice(target_indices)
        result_indices = list(index_to_person[from_index].result.keys())
        to_target = [index for index in result_indices if from_index != index]
        to_index = random.choice(to_target)

        del index_to_person[from_index].result[to_index]

        return index_to_person

    def generate_problem(self, index_to_person, max_iteration):
        """ Generate the problem.

        :return: ``dict``, which represents answer. :func:`get_answer_line` must assure that 
        the return of this function convert to the appropriate string.  At default setting, 
        ``dict`` as the element of the return of :func:`get_coherent_cases` is returned. 
        
        """

        for iter_number in range(max_iteration):
            coherent_list = self.get_coherent_cases(index_to_person)
            if len(coherent_list) == 0:
                index_to_person = self.delete_claim(index_to_person)
            elif len(coherent_list) > 1:
                index_to_person = self.add_claim(index_to_person)
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


