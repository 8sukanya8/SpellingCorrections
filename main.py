from ioLocal import readWholeText, find_edit_dist, create_dict_stem_from_freq_list, readFileIntoList, plot_data, \
    splitText
import config, time, matplotlib.pyplot as plt
from ngram import ngram_evaluation, unigram_word, bigram_word, trigram_word, bigram_count
from noisyChannel import noisy_channel_evaluation, find_uncorrectable_words

# Creating dictionary from different documents
#config.word_dict = {}
from unsupervisedRulesBased import unsupervised_rules_evaluation

for filename in config.list_of_filenames:
    lines = readWholeText(filename).split('\n')
    config.word_dict = create_dict_stem_from_freq_list(lines, config.word_dict)




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

# Training phase
start_noisy_channel = time.time()
print("Training Noisy Channel started...")
match_list_noisy_channel_train = noisy_channel_evaluation(train, config.word_dict, type_of_data = 'train')
end_noisy_channel = time.time()
print("Training Noisy Channel ended")
average_time_noisy_channel_train = (end_noisy_channel - start_noisy_channel)/ len(train)

start_n_gram = time.time()
print("Training N Gram started...")
match_list_n_gram_train = ngram_evaluation(train)
end_n_gram = time.time()
print("Training N Gram ended")
average_time_n_gram_train = (end_n_gram - start_n_gram)/ len(train)

start_unsupervised_rules = time.time()
print("Training unsupervised rules started...")
match_list_unsupervised_rules_train =  unsupervised_rules_evaluation(train)
end_unsupervised_rules = time.time()
print("Training unsupervised rules ended")
average_time_unsupervised_rules_train = (end_unsupervised_rules - start_unsupervised_rules)/ len(train)

print("\n\nTraining Output\n\n")
print("Average time taken by Noisy Channel: ", average_time_noisy_channel_train)
print("Average time taken by N gram: ", average_time_n_gram_train)
print("Average time taken by Unsupervised Rules:", average_time_unsupervised_rules_train)

plot_time = [[0.0 for _ in range(len(train)+1)] for _ in range(4)]
edit_distance = [[0.0 for _ in range(len(train)+1)] for _ in range(4)]
i = 0
for word in train:
    plot_time[0][i] = i
    edit_distance[0][i] = i
    i = i + 1
    if(len(word)>0):
        print("\n\n",word)
        if word in match_list_noisy_channel_train:
            candidates = match_list_noisy_channel_train[word][0]
            time_taken_noisy = match_list_noisy_channel_train[word][1]
            max_key = max(candidates,
                      key=lambda k: candidates[k])
            edit_dist_noisy = find_edit_dist(word, max_key)
            edit_distance[1][i] = edit_dist_noisy
            print("Noisy Channel-- :", max_key, " : ", candidates[max_key], "edit dist:",edit_dist_noisy , " time taken:",time_taken_noisy )
            plot_time[1][i] = time_taken_noisy
        if word in match_list_n_gram_train:
            candidates = match_list_n_gram_train[word][0]
            time_taken_n_gram = match_list_n_gram_train[word][1]
            max_key = max(candidates,
                          key=lambda k: candidates[k])
            edit_dist_n_gram = find_edit_dist(word, max_key)
            edit_distance[2][i] = edit_dist_n_gram
            print("N gram-- :", max_key, " : ", candidates[max_key],"edit dist:", edit_dist_n_gram," time taken:",time_taken_n_gram)
            plot_time[2][i] = time_taken_n_gram
        if word in match_list_unsupervised_rules_train:
            candidates = match_list_unsupervised_rules_train[word][0]
            time_taken_unsupervised = match_list_unsupervised_rules_train[word][1]
            max_key = max(candidates,
                          key=lambda k: candidates[k])
            edit_dist_unsupervised = find_edit_dist(word, max_key)
            edit_distance[3][i] = edit_dist_unsupervised
            print("Unsupervised-- :", max_key, " : ", candidates[max_key],"edit dist:", edit_dist_unsupervised," time taken:",time_taken_unsupervised)
            plot_time[3][i] = time_taken_unsupervised


plot_data(plot_time, ['count', 'noisy channel', 'n gram channel', 'unsupervised channel'],
          xlabel = 'models', ylabel = 'time taken', main = 'Training time comparison')
plot_data(edit_distance, ['count', 'noisy channel', 'n gram channel', 'unsupervised channel'],
          xlabel = 'models', ylabel = 'edit distance', main = 'Training Edit Distance comparison')

#plt.plot(plot_time[0],plot_time[1],'ro',label = 'noisy channel')
#plt.plot(plot_time[0],plot_time[2], 'bs',label = 'n gram channel')
#plt.plot(plot_time[0],plot_time[3],'g^',label = 'unsupervised channel')
#plt.ylabel('time taken')
#plt.xlabel('models')
#plt.text('Training time comparison', loc = 'upper center')
#plt.legend(loc='upper right')
#plt.show()



# Test phase 1
match_list_noisy_channel_test = noisy_channel_evaluation(test, config.word_dict, type_of_data = 'test')
match_list_n_gram_test = ngram_evaluation(test)
match_list_unsupervised_rules_test =  unsupervised_rules_evaluation(test)

plot_time = [[0.0 for _ in range(len(test)+1)] for _ in range(4)]
edit_distance = [[0.0 for _ in range(len(test)+1)] for _ in range(4)]
bigram_frequency = [[0.0 for _ in range(len(test)+1)] for _ in range(4)]
text = readWholeText(config.ngram_filename).lower()
bigram = bigram_word(text)
i = 0

print("\n\nTesting Output 1\n\n")
for word in test:
    plot_time[0][i] = i
    edit_distance[0][i] = i
    bigram_frequency[0][i] = i
    i = i + 1
    if(len(word)>0):
        print("\n\n",word)
        if word in match_list_noisy_channel_test:
            candidates = match_list_noisy_channel_test[word][0]
            time_taken_noisy = match_list_noisy_channel_test[word][1]
            max_key = max(candidates, key=lambda k: candidates[k])
            edit_dist_noisy = find_edit_dist(word, max_key)
            edit_distance[1][i] = edit_dist_noisy
            bigram_frequency[1][i] = bigram_count(bigram, max_key)
            print("Noisy Channel-- :", max_key, " : ", candidates[max_key], "edit dist:",edit_dist_noisy , " time taken:",time_taken_noisy , "bigram frequency:", bigram_frequency[1][i])
            plot_time[1][i] = time_taken_noisy
            print("bigram:", bigram_frequency[1][i])
        if word in match_list_n_gram_test:
            candidates = match_list_n_gram_test[word][0]
            time_taken_n_gram = match_list_n_gram_test[word][1]
            max_key = max(candidates, key=lambda k: candidates[k])
            edit_dist_n_gram = find_edit_dist(word, max_key)
            edit_distance[2][i] = edit_dist_n_gram
            bigram_frequency[2][i] = bigram_count(bigram, max_key)
            print("N gram-- :", max_key, " : ", candidates[max_key],"edit dist:", edit_dist_n_gram," time taken:",time_taken_n_gram,"bigram frequency:", bigram_frequency[2][i])
            plot_time[2][i] = time_taken_n_gram
        if word in match_list_unsupervised_rules_test:
            candidates = match_list_unsupervised_rules_test[word][0]
            time_taken_unsupervised = match_list_unsupervised_rules_test[word][1]
            max_key = max(candidates, key=lambda k: candidates[k])
            edit_dist_unsupervised = find_edit_dist(word, max_key)
            edit_distance[3][i] = edit_dist_unsupervised
            bigram_frequency[3][i] = bigram_count(bigram, max_key)
            print("Unsupervised-- :", max_key, " : ", candidates[max_key],"edit dist:", edit_dist_unsupervised," time taken:",time_taken_unsupervised, "bigram frequency:", bigram_frequency[3][i])
            plot_time[3][i] = time_taken_unsupervised


plot_data(plot_time, ['count', 'noisy channel', 'n gram channel', 'unsupervised channel'], xlabel='models',
                  ylabel='time taken', main='Testing 1 time comparison')
plot_data(edit_distance, ['count', 'noisy channel', 'n gram channel', 'unsupervised channel'], xlabel='models',
                  ylabel='edit distance', main='Testing 1 Edit Distance comparison')
plot_data(bigram_frequency, ['count', 'noisy channel', 'n gram channel', 'unsupervised channel'], xlabel='models',
                  ylabel='edit distance', main='Testing 1 bigram frequency comparison')
# ignore suggestions more than edit distance 3
# combine the three approaches and compare accuracy
# take first three suggestions given by the models and then run through the n-gram
# accuracy is defined by using a context based ngram approach and seeing out of three best choices which one performed the best
# write report
# find a proper logging library
# Requires two days of work


# Test phase n-gram words
# Create ngram words
print("\n\nTesting Output 2\n\n")
print('Testing for context based spelling correction')

unigram = unigram_word(text)
bigram = bigram_word(text)
trigram = trigram_word(text)

test_ngram = readWholeText(config.ngram_test_filename).lower()
test_ngram = splitText(test_ngram)


