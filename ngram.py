from ioLocal import readWholeText, splitText, matching_pattern, word_frequency_voting
import re
import config


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
        next_word = words[i+1]
        previous_word = words[i-1]
        bigram.append(word+' '+ next_word)
        bigram.append(previous_word + ' ' + word)
    unique_bigrams = set(bigram)
    #print("\n\n Number of unique bigrams:", len(unique_bigrams))
    for word in unique_bigrams:
        #print(bigram.count(word))
        if word not in bigram_dict:
            bigram_dict[word] = bigram.count(word)
    return bigram_dict


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


def ngram_evaluation(train, number_of_terms):
    # Description:
    #   This function finds all candidates for words in the training set as per the n-gram approach
    # Args:
    #   training set, size of training set
    # Returns:
    #   a dictionary of dictionaries of words in training set against their candidates with the voting count
    candidates = {}
    for word in train:
        temp_result = ngram_candidates(word)
        if(len(temp_result)>0) and word not in candidates:
            candidates[word] = temp_result
        #for entry in temp_result:
        #    candidates.append(entry)
    #result = word_frequency_voting(candidates)
    return candidates


