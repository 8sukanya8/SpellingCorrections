import re
from ioLocal import add, delete, matching_pattern, word_frequency_voting
import config,time


def rule1(word, K):
    # Description:
    #   This function finds candidates by deleting characters from the ends
    # Args:
    #   given word, max number of iterations
    # Returns:
    #   candidates
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
            pattern = '\w*'+word+'\w*'
            candidates = matching_pattern(config.word_dict.keys(), pattern)
            #print("\n",word," By rule1: ", candidates)
            for entry in candidates:
                result.append(entry)
        else:
            break
    return result


def rule2(word, K):
    # Description:
    #   This function finds candidates by deleting characters from the middle
    # Args:
    #   given word, max number of iterations
    # Returns:
    #   candidates
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
            first_part = word[0: mid - 1]
            second_part = word[mid+1:length]
        else:
            first_part = word[0: mid]
            second_part = word[mid+1:length]
        word = first_part + second_part
        length = len(word)
        if length > 1:
            # print(word)
            pattern = '^'+ first_part + '\w*' + second_part +'$'
            candidates = matching_pattern(config.word_dict.keys(), pattern)
            #print("\n",first_part+"_"+second_part, " By rule2: ", candidates)
            for entry in candidates:
                result.append(entry)
        else:
            break
    return result

def rule3(word): # second part
    # Description:
    #   This function finds candidates by using the second half of a word
    # Args:
    #   given word
    # Returns:
    #   candidates
    length = len(word)
    mid = int(length/2)
    #first_part = word[0: mid]
    second_part = word[mid: length]
    pattern = '\w*' + second_part + '$'
    candidates = matching_pattern(config.word_dict.keys(), pattern)
    #print("\n","_"+ second_part, "By rule3: ", candidates)
    return candidates


def rule4(word):
    # Description:
    #   This function finds candidates by using the first half of a word
    # Args:
    #   given word
    # Returns:
    #   candidates
    length = len(word)
    mid = int(length/2 + 1)
    first_part = word[0: mid]
    pattern = '^' + first_part + '\w*'
    candidates = matching_pattern(config.word_dict.keys(), pattern)
    #print("\n",first_part+ "_", "By rule4: ", candidates)
    return candidates


def rule5(word):
    # Description:
    #   This function finds candidates by using the first and last characters of a word
    # Args:
    #   given word
    # Returns:
    #   candidates

    start_char = word[0]
    end_char = word[len(word)-1]
    pattern = '^' + start_char + '\w*' + end_char + '$'
    candidates = matching_pattern(config.word_dict.keys(), pattern)
    #print("\n",start_char + "_" + end_char, "By rule5: ", candidates)
    return candidates


def rule6(word):
    # Description:
    #   This function finds candidates by using the first two and last two characters of a word
    # Args:
    #   given word
    # Returns:
    #   candidates
    first_part = word[0:2]
    second_part = word[len(word) - 2: len(word)]
    pattern = '^' + first_part + '\w*' + second_part + '$'
    candidates = matching_pattern(config.word_dict.keys(), pattern)
    #print("\n",first_part+ '_' +second_part," By rule6: ", candidates)
    return candidates


def candidate_generation(word):
    # Description:
    #   This function finds candidates by using all the rules
    # Args:
    #   given word
    # Returns:
    #   A dictionary of candidates with the voting value of each candidate
    candidate_list = []
    result = {}
    if(word not in config.word_dict.keys()):
        temp_results = rule1(word, config.K, )
        for entry in temp_results:
            candidate_list.append(entry)
        temp_results = rule2(word, config.K)
        for entry in temp_results:
            candidate_list.append(entry)
        temp_results = rule3(word)
        for entry in temp_results:
            candidate_list.append(entry)
        temp_results = rule4(word)
        for entry in temp_results:
            candidate_list.append(entry)
        temp_results = rule5(word)
        for entry in temp_results:
            candidate_list.append(entry)
        temp_results = rule6(word)
        for entry in temp_results:
            candidate_list.append(entry)
    for entry in candidate_list:
        if entry not in result:
            vote = candidate_list.count(entry)/len(candidate_list)
            result[entry] = vote
    return result


def unsupervised_rules_evaluation(list):
    # Description:
    #   This function finds all possible candidates for each word in the training set
    # Args:
    #   training set
    # Returns:
    #   A dictionary of dictionaries of each word against candidates with the voting value of each candidate
    result = {}
    for word in list:
        start = time.time()
        temp_result = candidate_generation(word)
        end = time.time()
        elapsed = end - start
        if(len(temp_result)>0) and word not in result:
            result[word]= [temp_result,elapsed]
    return result


# n gram approach
'''
filename = "Dataset/FederalistTraining.txt"
texts = readWholeText(filename).split("PUBLIUS")

lines = ''
for text in texts:
    if(len(text)>2):
        author = re.search(r'<AUTHOR>[\w ]*', text).group(0)
        author = re.sub (r'<AUTHOR>', '', author)
        #docNo = re.search(r'<DOCNO>[\w ]*', text).group(0)
        speech = text.split("</SOURCE>")[1].lower()
        lines = lines + speech

        lines = re.sub(r'\n', r' ', lines)
        lines = re.sub(r',', r'', lines)
        lines = re.sub(r'\'', r'', lines)
        lines = re.sub(r'\.', r'', lines)
        lines = re.sub(r'"', r'', lines)
        lines = re.sub(r'-', r' ', lines)
        lines = re.sub(r';', r'', lines)
        lines = re.sub(r'<', r'', lines)
        lines = re.sub(r'>', r'', lines)
        lines = re.sub(r'\?', r' ', lines)
        lines = re.sub(r'\\', r' ', lines)
        lines = re.sub(r'/', r' ', lines)
        lines = re.sub(r'\(', r'', lines)
        lines = re.sub(r':', r'', lines)
        lines = re.sub(r'\)', r' ', lines)
'''
