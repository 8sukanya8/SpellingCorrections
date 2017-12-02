from ioLocal import splitText, matching_pattern, word_frequency_voting
import config,time,re
from collections import Counter


def unigram_word(text):
    # Description:
    #   This function finds all unigram words in a given text
    # Args:
    #   text
    # Returns:
    #   a dictionary of unigrams with frequency count
    print("Finding unigrams. This might take a while...")
    words = splitText(text)
    unique_words = set(words)
    result = {}
    for word in unique_words:
        if word not in result:
            result[word] = words.count(word)
    return result

def bigram_word(text):
    # Description:
    #   This function finds all bigram words in a given text
    # Args:
    #   text
    # Returns:
    #   a dictionary of bigrams with frequency count
    print("Finding bigrams. This might take a while...")
    words = splitText(text)
    bigram = []
    bigram_dict = {}
    for i in range(1, len(words)-1):
        word = words[i]
        previous_word = words[i-1]
        bigram.append(previous_word + ' ' + word)
    bigram_dict = Counter(bigram)
    return bigram_dict
    #unique_bigrams = set(bigram)
    #print("\n\n Number of unique bigrams:", len(unique_bigrams))
    #for word in unique_bigrams:
        #print(bigram.count(word))
    #    if word not in bigram_dict:
    #        bigram_dict[word] = bigram.count(word)

#start = time.time()
#bigram_word(text)
#end = time.time()
#print("Time taken with Counter",end -start)

def bigram_count(bigrams, search_word):
    sum = 0
    for key in bigrams.keys():
        if (re.match(search_word, key)) or re.match('^[\w ]*'+search_word,key):
            sum = sum + bigrams[key]
            #print(key, bigrams[key])
    return sum

def trigram_word(text):
    # Description:
    #   This function finds all trigram words in a given text
    # Args:
    #   text
    # Returns:
    #   a dictionary of trigrams with frequency count
    print("Finding trigrams. This might take a while...")
    words = splitText(text)
    trigram = []
    trigram_dict = {}
    for i in range(1, len(words)-1):
        word = words[i]
        next_word = words[i+1]
        previous_word = words[i-1]
        trigram.append(previous_word + ' ' + word + ' '+ next_word)
    unique_trigrams = set(trigram)
    for word in unique_trigrams:
        #print(bigram.count(word))
        if word not in trigram_dict:
            trigram_dict[word] = trigram.count(word)
    return trigram_dict


def ngram_char(word, size):
    # Description:
    #   This function finds all ngram characters in a given text
    # Args:
    #   word, size of n gram
    # Returns:
    #   a dictionary of ngram characters with frequency count
    ngrams = []
    if size > len(word):
        print("Error!", size, " gram size is larger than word ", word, " size")
        return
    for i in range(0, (len(word)-size +1)):
        gram = word[i: i+size]
        ngrams.append(gram)
    return ngrams


def ngram_candidates(word):
    # Description:
    #   This function finds all ngram candidates
    # Args:
    #   word,
    # Returns:
    #   a dictionary of ngram characters with frequency count
    ngrams = ngram_char(word, config.ngram_size)
    candidates = []
    result = {}
    for ngram in ngrams:
        pattern = '\w*'+ ngram +'\w*'
        temp_result = matching_pattern(config.word_dict.keys(), pattern)
        for candidate in temp_result:
            candidates.append(candidate)
    for candidate in candidates:
        if candidate not in result:
            result[candidate] = candidates.count(candidate)/len(candidates)
    return result


def ngram_evaluation(train):
    # Description:
    #   This function finds all candidates for words in the training set as per the n-gram approach
    # Args:
    #   training set, size of training set
    # Returns:
    #   a dictionary of dictionaries of words in training set against their candidates with the voting count
    candidates = {}
    for word in train:
        start = time.time()
        temp_result = ngram_candidates(word)
        temp_result = sorted(temp_result.items(), key=lambda x: x[1], reverse=True)
        end = time.time()
        elapsed = end - start
        if(len(temp_result)>0) and word not in candidates:
            candidates[word] = [temp_result, elapsed]
        #for entry in temp_result:
        #    candidates.append(entry)
    #result = word_frequency_voting(candidates)
    return candidates

def matching_bigrams(bigrams, match, type = 'previous', max = 1):
    match_list = {}
    if(type =='previous'):
        expr = match
    elif (type == 'after'):
        expr = '[\w ]*' + match + '$'
    else:
        print('Error! type error! type can be only \'previous\' or \'after\'')
    for word in bigrams:
        if(re.match(expr, word)):
            match_list[word]= bigrams[word]
            #print(word, " ", bigrams[word])
    match_list_sorted = sorted(match_list.items(), key=lambda x: x[1])
    return match_list_sorted [len(match_list_sorted)-max-1 : len(match_list_sorted)-1]


