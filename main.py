from ioLocal import readWholeText, find_edit_dist, create_dict_stem_from_freq_list, readFileIntoList, plot_data, \
    splitText, filterAlpha
import config
from ngram import ngram_evaluation, unigram_word, bigram_word, trigram_word, bigram_count, matching_bigrams
from noisyChannel import noisy_channel_evaluation, find_uncorrectable_words
from comparison import compare, compare_with_bigram, compare_with_trigram
from unsupervisedRulesBased import unsupervised_rules_evaluation

# Creating dictionary from different documents
for filename in config.list_of_filenames:
    lines = readWholeText(filename).split('\n')
    config.word_dict = create_dict_stem_from_freq_list(lines, config.word_dict)

# Creating train and test sets
incorrect =  []
for filename in config.mistake_filenames: # fix the problem of creating one list. Now lists of lists are being created
    #incorrect.append(readFileIntoList(filename))
    incorrect = readFileIntoList(filename)

train = incorrect[0: int (0.7* len(incorrect))]
test = incorrect[int (0.7* len(incorrect)+1): len(incorrect)]
correct = readWholeText(config.mistake_correction_filename)
correct = filterAlpha(correct)
correct = splitText(correct)
train_correct = correct[0: int (0.7* len(correct))]
test_correct = correct[int (0.7* len(correct)+1): len(correct)]

# Training phase
print("\n\nModel Training started\n\n")
match_list_noisy_channel_train = noisy_channel_evaluation(train, config.word_dict, type_of_data = 'train')
match_list_n_gram_train = ngram_evaluation(train)
match_list_unsupervised_rules_train =  unsupervised_rules_evaluation(train)
# Training models comparison


print("\n\nTraining Comparison\n\n")
compare(match_list_noisy_channel_train, match_list_n_gram_train, match_list_unsupervised_rules_train, list=train, correct=train_correct, plot_title="Training")


# Testing phase 1
match_list_noisy_channel_test = noisy_channel_evaluation(test, config.word_dict, type_of_data = 'test')
match_list_n_gram_test = ngram_evaluation(test)
match_list_unsupervised_rules_test =  unsupervised_rules_evaluation(test)

compare(match_list_noisy_channel_test, match_list_n_gram_test, match_list_unsupervised_rules_test, correct=test_correct, list=test, plot_title="Testing")

# Testing phase 2 [ using context/ n-gram words]
# Create ngram words
print("\n\nTesting Output 2\n\n")
print('Testing for context based spelling correction')
text = readWholeText(config.ngram_filename).lower()
test_ngram = readWholeText(config.ngram_test_filename).lower()
test_ngram = filterAlpha(test_ngram)
test_ngram = splitText(test_ngram)

test_ngram_correct = readWholeText(config.ngram_test_filename_correct)
test_ngram_correct = filterAlpha(test_ngram_correct)
test_ngram_correct = splitText(test_ngram_correct)
compare_with_trigram(text, test_ngram, plot_title=" Testing ", correct = test_ngram_correct)


compare_with_bigram(text, test_ngram, plot_title=" Testing ", correct=test_ngram_correct)

# fix bigram count in code
# fix accuracy upto 3 places
# find precision recall graph
# accuracy is defined by using a context based ngram approach and seeing out of three best choices which one performed the best
# write report
# find a proper logging library
# Requires two days of work

j =0
for i in range(0, len(test_ngram)):
    if(test_ngram[i] not in config.word_dict):
        print(test_ngram[i], " ", test_ngram_correct[j])
        j = j+1