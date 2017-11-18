import re
from ioLocal import add, delete
import config


def rule1(word, K):
    k = 0
    length = len(word)
    result = []
    while length > 0 and k < K:
        k = k + 1
        word = delete(word,0,1)
        length = len(word)
        word = delete(word, length-1, 1)
        if len(word) > 1:
            #print(word)
            result.append(word)
        else:
            break
    return result


def rule2(word, K):
    length = len(word)
    result = []
    #if K < length/2:
    k= 0
    #mid = int(length / 2)
    while length > 0 and k < K:
        k = k + 1
        length = len(word)
        mid = int(length / 2)
        if length % 2 == 0:
            word = delete(word, mid-1, 2)
        else:
            word = delete(word, mid, 1)
        if len(word) > 1:
            #print(word)
            result.append(word)
        else:
            break
    return result
    #else:
    #    print("Error! Trying to remove more characters than present bt rule2. K=",K)
    #    return []


def rule3(word): # second part
    length = len(word)
    mid = int(length/2)
    #first_part = word[0: mid]
    second_part = word[mid: length]
    return second_part


def rule4(word):
    length = len(word)
    mid = int(length/2 + 1)
    first_part = word[0: mid]
    return first_part


def rule5(word):
    start_char = word[0]
    end_char = word[len(word)-1]
    return start_char + end_char


def rule6(word):
    first_part = word[0:1]
    second_part = word[len(word) - 2: len(word) - 1]
    return first_part + second_part


def candidate_generation(word, word_dict):
    result_list = []
    temp_results = rule1(word, config.K)
    for entry in temp_results:
        result_list.append(entry)
    temp_results = rule2(word, config.K)
    for entry in temp_results:
        result_list.append(entry)
    result_list.append(rule3(word))
    result_list.append(rule4(word))
    result_list.append(rule5(word))
    result_list.append(rule6(word))
    return result_list

# use re.match these candidates in word_dictionary to find candidates
