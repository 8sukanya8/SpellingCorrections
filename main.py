from ioLocal import readWholeText, find_edit_dist
from ioLocal import create_dict_stem_from_freq_list
from ioLocal import readFileIntoList
import config
from ngram import ngram_evaluation
from noisyChannel import noisy_channel_evaluation, find_uncorrectable_words

# Creating dictionary from different documents
#config.word_dict = {}
from unsupervisedRulesBased import unsupervised_rules_evaluation

for filename in config.list_of_filenames:
    lines = readWholeText(filename).split('\n')
    config.config.word_dict = create_dict_stem_from_freq_list(lines, config.word_dict)

number_of_terms = sum(config.word_dict.values())


# replacing absolute frequency by relative frequency rounded to 3 decimal places
'''for key in config.word_dict:
    value = config.word_dict[key]
    config.word_dict[key] = round(value/number_of_terms, 3)
'''

# reading all train and test data of incorrect spellings
incorrect =  []
for filename in config.mistake_filenames: # fix the problem of creating one list. Now lists of lists are being created
    #incorrect.append(readFileIntoList(filename))
    incorrect = readFileIntoList(filename)


train = incorrect[1: int (0.7* len(incorrect))]
test = incorrect[int (0.7* len(incorrect)+1): len(incorrect)]

#train = ['fltter', 'mganificence', 'culmineting', 'dependeble', 'hungery', 'celculation', 'defintion']

match_list_noisy_channel = noisy_channel_evaluation(train, config.word_dict, number_of_terms)
#print("Percentage of Words which were incorrect but had no candidates: ", (find_uncorrectable_words(match_list_noisy_channel)*100)/len(train),"%")

match_list_n_gram = ngram_evaluation(train, number_of_terms)
match_list_unsupervised_rules =  unsupervised_rules_evaluation(train, number_of_terms)


# find a proper logging library

for word in train:
    if(len(word)>0):
        print("\n\n",word)
        if word in match_list_noisy_channel:
            candidates = match_list_noisy_channel[word]
            max_key = max(candidates,
                      key=lambda k: candidates[k])
            print("Noisy Channel-- :", max_key, " : ", candidates[max_key], "edit dist:", find_edit_dist(word, max_key))
        if word in match_list_n_gram:
            candidates = match_list_n_gram[word]
            max_key = max(candidates,
                          key=lambda k: candidates[k])
            print("N gram-- :", max_key, " : ", candidates[max_key],"edit dist:", find_edit_dist(word, max_key))
        if word in match_list_unsupervised_rules:
            candidates = match_list_unsupervised_rules[word]
            max_key = max(candidates,
                          key=lambda k: candidates[k])
            print("Unsupervised-- :", max_key, " : ", candidates[max_key],"edit dist:", find_edit_dist(word, max_key))


