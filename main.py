from ioLocal import readWholeText
from ioLocal import create_dict_stem_from_freq_list
from ioLocal import readFileIntoList
import config
from noisyChannel import noisy_channel_evaluation, find_uncorrectable_words

# Creating dictionary from different documents
word_dict = {}
for filename in config.list_of_filenames:
    lines = readWholeText(filename).split('\n')
    word_dict = create_dict_stem_from_freq_list(lines, word_dict)

number_of_terms = sum(word_dict.values())


# replacing absolute frequency by relative frequency rounded to 3 decimal places
'''for key in word_dict:
    value = word_dict[key]
    word_dict[key] = round(value/number_of_terms, 3)
'''

# reading all train and test data of incorrect spellings
incorrect =  []
for filename in config.mistake_filenames: # fix the problem of creating one list. Now lists of lists are being created
    #incorrect.append(readFileIntoList(filename))
    incorrect = readFileIntoList(filename)

train = incorrect[1: int (0.7* len(incorrect))]
test = incorrect[int (0.7* len(incorrect)+1): len(incorrect)]

#train = ['fltter', 'mganificence', 'culmineting', 'dependeble', 'hungery', 'celculation', 'defintion']

match_list_noisy_channel = noisy_channel_evaluation(train, word_dict, number_of_terms)
print("Percentage of Words which were incorrect but had no candidates: ", (find_uncorrectable_words(match_list_noisy_channel)*100)/len(train),"%")



# find a proper logging library