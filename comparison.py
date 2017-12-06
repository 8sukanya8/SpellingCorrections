from ioLocal import find_edit_dist, plot_data, readWholeText, splitText
import config
from noisyChannel import noisy_channel_evaluation
from ngram import ngram_evaluation, bigram_word, trigram_word
from unsupervisedRulesBased import unsupervised_rules_evaluation

def compare(match_list_noisy_channel, match_list_n_gram, match_list_unsupervised_rules, correct, list, plot_title = ""):
    # Description:
    #   This function compares four models in terms of time taken, edit distance and accuracy
    # Args:
    #   candidate list for each model, plot title desired for the type of data
    # Returns:
    #   Nothing
    plot_time = [[0.0 for _ in range(len(list) + 1)] for _ in range(5)] # used for plotting time taken
    edit_distance = [[0.0 for _ in range(len(list) + 1)] for _ in range(5)] # used for plotting edit_distance
    count_noisy =0 # used for calculating Accuracy
    count_ngram =0 # used for calculating Accuracy
    count_unsupervised = 0 # used for calculating Accuracy
    count_combined = 0 # used for calculating Accuracy
    i = 0 # denotes each word in list
    #print("\n\nTesting Output 1\n\n")
    print("Model Comparison started")
    for word in list:
        plot_time[0][i] = i
        edit_distance[0][i] = i
        i = i + 1
        if (len(word) > 0):
            print("\n\n", word)
            confidence_unsupervised = 0
            confidence_ngram = 0
            if word in match_list_noisy_channel:
                candidates = match_list_noisy_channel[word][0]
                time_taken_noisy = match_list_noisy_channel[word][1]
                max_key_noisy = candidates[0][0]
                if(max_key_noisy ==correct[i-1]):
                    count_noisy = count_noisy+1
                edit_dist_noisy = find_edit_dist(word, max_key_noisy)
                edit_distance[1][i] = edit_dist_noisy
                print("Noisy Channel-- :", max_key_noisy, " : ", candidates[0][1], "edit dist:", edit_dist_noisy,
                      " time taken:", time_taken_noisy, "count: ", count_noisy, "/", i, correct[i-1])
                plot_time[1][i] = time_taken_noisy
            if word in match_list_n_gram:
                candidates = match_list_n_gram[word][0]
                time_taken_n_gram = match_list_n_gram[word][1]
                max_key_ngram = candidates[0][0]
                if(max_key_ngram == correct[i-1]):
                    count_ngram = count_ngram +1
                confidence_ngram = candidates[0][1]
                edit_dist_n_gram = find_edit_dist(word, max_key_ngram)
                edit_distance[2][i] = edit_dist_n_gram
                print("N gram-- :", max_key_ngram, " : ", confidence_ngram, "edit dist:", edit_dist_n_gram,
                      " time taken:", time_taken_n_gram, "count: ", count_ngram, "/", i, correct[i-1])
                plot_time[2][i] = time_taken_n_gram
            if word in match_list_unsupervised_rules:
                candidates = match_list_unsupervised_rules[word][0]
                time_taken_unsupervised = match_list_unsupervised_rules[word][1]
                max_key_unsupervised = candidates[0][0]
                if(max_key_unsupervised == correct[i-1]):
                    count_unsupervised = count_unsupervised+1
                confidence_unsupervised = candidates[0][1]
                edit_dist_unsupervised = find_edit_dist(word, max_key_unsupervised)
                edit_distance[3][i] = edit_dist_unsupervised
                print("Unsupervised-- :", max_key_unsupervised, " : ", confidence_unsupervised, "edit dist:",
                      edit_dist_unsupervised, " time taken:", time_taken_unsupervised, "count: ", count_unsupervised, "/", i, correct[i-1])
                plot_time[3][i] = time_taken_unsupervised
            if confidence_unsupervised < config.beta:
                time_taken_unsupervised = 0
                time_taken_n_gram = 0
                if (confidence_ngram < confidence_unsupervised):
                    if word in match_list_unsupervised_rules:
                        candidates = match_list_unsupervised_rules[word][0]
                        time_taken_unsupervised = match_list_unsupervised_rules[word][1]
                        max_key_combined = candidates[0][0]
                        if(max_key_combined == correct[i-1]):
                            count_combined = count_combined +1
                        edit_dist_combined = find_edit_dist(word, max_key_combined)
                        edit_distance[4][i] = edit_dist_combined
                        print("Unsupervised Ngram Combination-- :", max_key_combined, " : ", confidence_unsupervised,
                              "edit dist:", edit_dist_combined,
                              " time taken:", time_taken_unsupervised, "count: ", count_combined, "/", i, correct[i-1])
                else:
                    if word in match_list_n_gram:
                        candidates = match_list_n_gram[word][0]
                        time_taken_n_gram = match_list_n_gram[word][1]
                        max_key_combined = candidates[0][0]
                        if (max_key_combined == correct[i-1]):
                            count_combined = count_combined + 1
                        edit_dist_combined = find_edit_dist(word, max_key_combined)
                        edit_distance[4][i] = edit_dist_combined
                        print("Unsupervised Ngram Combination--:", max_key_combined, " : ", confidence_ngram,
                              "edit dist:", edit_dist_combined,
                              " time taken:", time_taken_n_gram, "count: ", count_combined, "/", i, correct[i-1])
                plot_time[4][i] = plot_time[2][i] + plot_time[3][i]
                # print("time taken:", plot_time[4][i])
    print("Count Noisy: ", count_noisy)
    print("Accuracy Noisy Channel: ", count_noisy / i)
    print("Count N gram: ", count_ngram)
    print("Accuracy N gram: ", count_ngram / i)
    print("Count Unsupervised: ", count_unsupervised)
    print("Accuracy Unsupervised: ", count_unsupervised / i)
    print("Count Combined: ", count_combined)
    print("Accuracy Combined: ", count_combined / i)
    plot_data(plot_time, ['count', 'noisy channel', 'n gram', 'unsupervised', 'combined (n gram, unsupervised)'], xlabel='incorrect words',
              ylabel='time taken', main= plot_title+' Time comparison')
    plot_data(edit_distance, ['count', 'noisy channel', 'n gram', 'unsupervised', 'combined (n gram, unsupervised)'], xlabel='models',
              ylabel='edit distance', main= plot_title+' Edit Distance comparison')

def compare_with_bigram(text, test_ngram_word_list, correct, plot_title = ""):
    bigram = bigram_word(text)
    plot_ngram = [[0.0 for _ in range(len(test_ngram_word_list) + 1)] for _ in range(5)]
    count_mistakes = 0
    count_noisy =0
    count_ngram = 0
    count_unsupervised = 0
    count_combined =0
    bigram_noisy =0
    bigram_ngram =0
    bigram_unsupervised =0
    bigram_combined =0
    for i in range(1, len(test_ngram_word_list) - 1):
        plot_ngram[0][i] = i
        if test_ngram_word_list[i] not in config.word_dict.keys():
            count_mistakes = count_mistakes + 1
            print("\n\n", test_ngram_word_list[i - 1], " ", test_ngram_word_list[i])
            match_list_noisy_channel_test = noisy_channel_evaluation([test_ngram_word_list[i]], config.word_dict,
                                                                     type_of_data='test', skip_notification=True)
            candidates_noisy_channel = []
            if (len(match_list_noisy_channel_test) > 0):
                candidates_noisy_channel = match_list_noisy_channel_test[test_ngram_word_list[i]][0]
            match_list_n_gram_test = ngram_evaluation([test_ngram_word_list[i]], skip_notification=True)
            candidates_n_gram = []
            if (len(match_list_n_gram_test) > 0):
                candidates_n_gram = match_list_n_gram_test[test_ngram_word_list[i]][0]
            match_list_unsupervised_rules_test = unsupervised_rules_evaluation([test_ngram_word_list[i]], skip_notification=True)
            candidates_unsupervised_rules = []
            if (len(match_list_unsupervised_rules_test) > 0):
                candidates_unsupervised_rules = match_list_unsupervised_rules_test[test_ngram_word_list[i]][0]
            for j in range(0, 3):
                expr_noisy = test_ngram_word_list[i - 1] + ' '
                expr_ngram = test_ngram_word_list[i - 1] + ' '
                expr_unsupervised = test_ngram_word_list[i - 1] + ' '
                print("Candidate number: ", j + 1)
                if (len(candidates_noisy_channel) > j):
                    expr_noisy = expr_noisy + candidates_noisy_channel[j][0]
                    if expr_noisy in bigram:
                        bigram_noisy = bigram_noisy +1
                        if(candidates_noisy_channel[j][0] == correct[count_mistakes -1]):
                            count_noisy = count_noisy+1
                        print("noisy: ", expr_noisy, bigram[expr_noisy], " ",count_noisy, "/", count_mistakes, correct[count_mistakes-1])
                        if (plot_ngram[1][i] < bigram[expr_noisy]):
                            plot_ngram[1][i] = bigram[expr_noisy]
                if (len(candidates_n_gram) > j):
                    expr_ngram = expr_ngram + candidates_n_gram[j][0]
                    if expr_ngram in bigram:
                        if (candidates_n_gram[j][0] == correct[count_mistakes -1]):
                            count_ngram = count_ngram + 1
                        print("ngram: ", expr_ngram, bigram[expr_ngram], " ",count_ngram, "/", count_mistakes, correct[count_mistakes-1])
                        if (plot_ngram[2][i] < bigram[expr_ngram]):
                            plot_ngram[2][i] = bigram[expr_ngram]
                if (len(candidates_unsupervised_rules) > j):
                    expr_unsupervised = expr_unsupervised + candidates_unsupervised_rules[j][0]
                    if expr_unsupervised in bigram:
                        if (candidates_unsupervised_rules[j][0] == correct[count_mistakes -1]):
                            count_unsupervised = count_unsupervised + 1
                        print("unsupervised: ", expr_unsupervised, bigram[expr_unsupervised], " ",count_unsupervised, "/", count_mistakes, correct[count_mistakes-1])
                        if (plot_ngram[3][i] < bigram[expr_unsupervised]):
                            plot_ngram[3][i] = bigram[expr_unsupervised]
                #if (len(candidates_n_gram) > j) and len(candidates_unsupervised_rules) > j:
                #    if candidates_n_gram[j][0]== correct[count_mistakes -1] or candidates_unsupervised_rules[j][0] ==correct[count_mistakes-1]:
                #        count_combined = count_combined + 1
                #        print("combined : ",correct[count_mistakes-1], "/", count_mistakes," ", count_combined)
                if(bigram[expr_unsupervised]> bigram[expr_ngram]):
                    plot_ngram[4][i] = bigram[expr_unsupervised]
                    if(len(candidates_unsupervised_rules) > j):
                        if candidates_unsupervised_rules[j][0] == correct[count_mistakes - 1]:
                            count_combined = count_combined + 1
                            print("combined unsupervised : ",expr_unsupervised, " ", correct[count_mistakes - 1],count_combined, "/", count_mistakes)
                else:
                    plot_ngram[4][i] = bigram[expr_ngram]
                    if (len(candidates_n_gram) > j):
                        if candidates_n_gram[j][0] == correct[count_mistakes - 1]:
                            count_combined = count_combined + 1
                            print("combined ngram: ",expr_ngram, " ", correct[count_mistakes - 1], count_combined, "/", count_mistakes)

    plot_data(plot_ngram, ['count', 'noisy channel', 'n gram channel', 'unsupervised channel','combined (n gram, unsupervised)'],
              xlabel='words',
              ylabel='Bigram Count', main= plot_title + 'Bigram Frequency Comparison')
    print("Count Noisy: ", count_noisy)
    print("Accuracy Noisy Channel: ", count_noisy/ count_mistakes)
    print("Count N gram: ", count_ngram)
    print("Accuracy N gram: ", count_ngram / count_mistakes)
    print("Count Unsupervised: ", count_unsupervised)
    print("Accuracy Unsupervised: ", count_unsupervised / count_mistakes)
    print("Count Combined: ", count_combined)
    print("Accuracy Combined: ", count_combined/count_mistakes)


def compare_with_trigram(text, test_ngram_word_list,correct, plot_title = ""):
    trigram = trigram_word(text)
    count_mistakes = 0
    count_noisy = 0
    count_ngram = 0
    count_unsupervised = 0
    count_combined = 0
    trigram_noisy=0
    trigram_ngram=0
    trigram_unsupervised =0
    trigram_combined =0
    plot_ngram = [[0.0 for _ in range(len(test_ngram_word_list) + 1)] for _ in range(5)]
    for i in range(1, len(test_ngram_word_list) - 1):
        plot_ngram[0][i] = i
        if test_ngram_word_list[i] not in config.word_dict.keys():
            count_mistakes = count_mistakes + 1
            print("\n\n", test_ngram_word_list[i - 1], " ", test_ngram_word_list[i], " ", test_ngram_word_list[i+1])
            match_list_noisy_channel_test = noisy_channel_evaluation([test_ngram_word_list[i]], config.word_dict,
                                                                     type_of_data='test', skip_notification=True)
            candidates_noisy_channel = []
            if (len(match_list_noisy_channel_test) > 0):
                candidates_noisy_channel = match_list_noisy_channel_test[test_ngram_word_list[i]][0]
            match_list_n_gram_test = ngram_evaluation([test_ngram_word_list[i]], skip_notification=True)
            candidates_n_gram = []
            if (len(match_list_n_gram_test) > 0):
                candidates_n_gram = match_list_n_gram_test[test_ngram_word_list[i]][0]
            match_list_unsupervised_rules_test = unsupervised_rules_evaluation([test_ngram_word_list[i]], skip_notification=True)
            candidates_unsupervised_rules = []
            if (len(match_list_unsupervised_rules_test) > 0):
                candidates_unsupervised_rules = match_list_unsupervised_rules_test[test_ngram_word_list[i]][0]
            for j in range(0, 3):
                expr_noisy = test_ngram_word_list[i - 1] + ' '
                expr_ngram = test_ngram_word_list[i - 1] + ' '
                expr_unsupervised = test_ngram_word_list[i - 1] + ' '
                print("Candidate number: ", j + 1)
                if (len(candidates_noisy_channel) > j):
                    expr_noisy = expr_noisy + candidates_noisy_channel[j][0] + ' ' + test_ngram_word_list[i + 1]
                    #print("Noisy candidate:", expr_noisy)
                    if expr_noisy in trigram:
                        trigram_noisy = trigram_noisy+1
                        print('trigram noisy:', trigram_noisy)
                    if (candidates_noisy_channel[j][0] == correct[count_mistakes - 1]):
                        count_noisy = count_noisy + 1
                        print("noisy: ", expr_noisy, trigram[expr_noisy], " ", count_noisy,"/", count_mistakes, correct[count_mistakes - 1])
                        if (plot_ngram[1][i] < trigram[expr_noisy]):
                            plot_ngram[1][i] = trigram[expr_noisy]
                if (len(candidates_n_gram) > j):
                    expr_ngram = expr_ngram + candidates_n_gram[j][0] + ' ' + test_ngram_word_list[i + 1]
                    if expr_ngram in trigram:
                        trigram_ngram = trigram_ngram +1
                        print('trigram ngram:', trigram_ngram)
                    if (candidates_n_gram[j][0] == correct[count_mistakes -1]):
                        count_ngram = count_ngram + 1
                        print("ngram: ", expr_ngram, trigram[expr_ngram]," ", count_ngram,"/", count_mistakes, correct[count_mistakes - 1])
                        if (plot_ngram[2][i] < trigram[expr_ngram]):
                            plot_ngram[2][i] = trigram[expr_ngram]
                if (len(candidates_unsupervised_rules) > j):
                    expr_unsupervised = expr_unsupervised + candidates_unsupervised_rules[j][0] + ' ' + test_ngram_word_list[i + 1]
                    if expr_unsupervised in trigram:
                        trigram_unsupervised = trigram_unsupervised +1
                        print('trigram unsupervised:', trigram_unsupervised)
                    if (candidates_unsupervised_rules[j][0] == correct[count_mistakes -1]):
                        count_unsupervised = count_unsupervised + 1
                        print("unsupervised: ", expr_unsupervised, trigram[expr_unsupervised]," ", count_unsupervised,"/", count_mistakes, correct[count_mistakes - 1])
                        if (plot_ngram[3][i] < trigram[expr_unsupervised]):
                            plot_ngram[3][i] = trigram[expr_unsupervised]
                if(expr_unsupervised in trigram or expr_ngram in trigram):
                    trigram_combined = trigram_combined+1
                    print("trigram combined", trigram_combined)
                if(trigram[expr_unsupervised]> trigram[expr_ngram]): # checking for confidence, if confidence of unsupervised is higher, take its candidate
                    plot_ngram[4][i] = trigram[expr_unsupervised]
                    if(len(candidates_unsupervised_rules) > j):
                        if candidates_unsupervised_rules[j][0] == correct[count_mistakes - 1]:
                            count_combined = count_combined + 1
                            print("combined unsupervised : ",expr_unsupervised, " ", correct[count_mistakes - 1],count_combined, "/", count_mistakes, correct[count_mistakes - 1])
                else:
                    plot_ngram[4][i] = trigram[expr_ngram]
                    if (len(candidates_n_gram) > j):
                        if candidates_n_gram[j][0] == correct[count_mistakes - 1]:
                            count_combined = count_combined + 1
                            print("combined ngram: ",expr_ngram, " ", correct[count_mistakes - 1], count_combined, "/", count_mistakes, correct[count_mistakes - 1])
                #if (trigram[expr_unsupervised] > trigram[expr_ngram]):
                #    plot_ngram[4][i] = trigram[expr_unsupervised]
                #else:
                #    plot_ngram[4][i] = trigram[expr_ngram]
    print("Count Noisy: ", count_noisy)
    print("Accuracy Noisy Channel: ", count_noisy / count_mistakes)
    print("Count N gram: ", count_ngram)
    print("Accuracy N gram: ", count_ngram / count_mistakes)
    print("Count Unsupervised: ", count_unsupervised)
    print("Accuracy Unsupervised: ", count_unsupervised / count_mistakes)
    print("Count Combined: ", count_combined)
    print("Accuracy Combined: ", count_combined / count_mistakes)
    print("Trigram Count Noisy: ", trigram_noisy)
    print("Hits Noisy Channel: ", trigram_noisy / count_mistakes)
    print("Trigram Count N gram: ", trigram_ngram)
    print("Hits N gram: ", trigram_ngram / count_mistakes)
    print("Trigram Count Unsupervised: ", trigram_unsupervised)
    print("Hits Unsupervised: ", trigram_unsupervised / count_mistakes)
    print("Trigram Count Combined: ", trigram_combined)
    print("Hits Combined: ", trigram_combined / count_mistakes)
    plot_data(plot_ngram, ['count', 'noisy channel', 'n gram channel', 'unsupervised channel', 'combined (n gram, unsupervised)'],
              xlabel='words',
              ylabel='Trigram Count', main= plot_title + 'Trigram Frequency Comparison')


'''
def compare_with_trigram(text, test_ngram_word_list,correct, plot_title = ""):
    trigram = trigram_word(text)
    count_mistakes = 0
    count_noisy = 0
    count_ngram = 0
    count_unsupervised = 0
    count_combined = 0
    trigram_noisy=0
    trigram_ngram=0
    trigram_unsupervised =0
    trigram_combined =0
    plot_ngram = [[0.0 for _ in range(len(test_ngram_word_list) + 1)] for _ in range(5)]
    for i in range(1, len(test_ngram_word_list) - 1):
        plot_ngram[0][i] = i
        if test_ngram_word_list[i] not in config.word_dict.keys():
            count_mistakes = count_mistakes + 1
            print("\n\n", test_ngram_word_list[i - 1], " ", test_ngram_word_list[i], " ", test_ngram_word_list[i+1])
            match_list_noisy_channel_test = noisy_channel_evaluation([test_ngram_word_list[i]], config.word_dict,
                                                                     type_of_data='test', skip_notification=True)
            candidates_noisy_channel = []
            if (len(match_list_noisy_channel_test) > 0):
                candidates_noisy_channel = match_list_noisy_channel_test[test_ngram_word_list[i]][0]
            match_list_n_gram_test = ngram_evaluation([test_ngram_word_list[i]], skip_notification=True)
            candidates_n_gram = []
            if (len(match_list_n_gram_test) > 0):
                candidates_n_gram = match_list_n_gram_test[test_ngram_word_list[i]][0]
            match_list_unsupervised_rules_test = unsupervised_rules_evaluation([test_ngram_word_list[i]], skip_notification=True)
            candidates_unsupervised_rules = []
            if (len(match_list_unsupervised_rules_test) > 0):
                candidates_unsupervised_rules = match_list_unsupervised_rules_test[test_ngram_word_list[i]][0]
            for j in range(0, 3):
                expr_noisy = test_ngram_word_list[i - 1] + ' '
                expr_ngram = test_ngram_word_list[i - 1] + ' '
                expr_unsupervised = test_ngram_word_list[i - 1] + ' '
                print("Candidate number: ", j + 1)
                if (len(candidates_noisy_channel) > j):
                    expr_noisy = expr_noisy + candidates_noisy_channel[j][0] + ' ' + test_ngram_word_list[i + 1]
                    print("Noisy candidate:", expr_noisy, trigram)
                    if expr_noisy in trigram:
                        if (candidates_noisy_channel[j][0] == correct[count_mistakes - 1]):
                            count_noisy = count_noisy + 1
                        print("noisy: ", expr_noisy, trigram[expr_noisy], " ", count_noisy,"/", count_mistakes, correct[count_mistakes - 1])
                        if (plot_ngram[1][i] < trigram[expr_noisy]):
                            plot_ngram[1][i] = trigram[expr_noisy]
                if (len(candidates_n_gram) > j):
                    expr_ngram = expr_ngram + candidates_n_gram[j][0] + ' ' + test_ngram_word_list[i + 1]
                    if expr_ngram in trigram:
                        if (candidates_n_gram[j][0] == correct[count_mistakes -1]):
                            count_ngram = count_ngram + 1
                        print("ngram: ", expr_ngram, trigram[expr_ngram]," ", count_ngram,"/", count_mistakes, correct[count_mistakes - 1])
                        if (plot_ngram[2][i] < trigram[expr_ngram]):
                            plot_ngram[2][i] = trigram[expr_ngram]
                if (len(candidates_unsupervised_rules) > j):
                    expr_unsupervised = expr_unsupervised + candidates_unsupervised_rules[j][0] + ' ' + test_ngram_word_list[i + 1]
                    if expr_unsupervised in trigram:
                        if (candidates_unsupervised_rules[j][0] == correct[count_mistakes -1]):
                            count_unsupervised = count_unsupervised + 1
                        print("unsupervised: ", expr_unsupervised, trigram[expr_unsupervised]," ", count_unsupervised,"/", count_mistakes, correct[count_mistakes - 1])
                        if (plot_ngram[3][i] < trigram[expr_unsupervised]):
                            plot_ngram[3][i] = trigram[expr_unsupervised]
                if(trigram[expr_unsupervised]> trigram[expr_ngram]): # checking for confidence, if confidence of unsupervised is higher, take its candidate
                    plot_ngram[4][i] = trigram[expr_unsupervised]
                    if(len(candidates_unsupervised_rules) > j):
                        if candidates_unsupervised_rules[j][0] == correct[count_mistakes - 1]:
                            count_combined = count_combined + 1
                            print("combined unsupervised : ",expr_unsupervised, " ", correct[count_mistakes - 1],count_combined, "/", count_mistakes, correct[count_mistakes - 1])
                else:
                    plot_ngram[4][i] = trigram[expr_ngram]
                    if (len(candidates_n_gram) > j):
                        if candidates_n_gram[j][0] == correct[count_mistakes - 1]:
                            count_combined = count_combined + 1
                            print("combined ngram: ",expr_ngram, " ", correct[count_mistakes - 1], count_combined, "/", count_mistakes, correct[count_mistakes - 1])
                #if (trigram[expr_unsupervised] > trigram[expr_ngram]):
                #    plot_ngram[4][i] = trigram[expr_unsupervised]
                #else:
                #    plot_ngram[4][i] = trigram[expr_ngram]
    print("Count Noisy: ", count_noisy)
    print("Accuracy Noisy Channel: ", count_noisy / count_mistakes)
    print("Count N gram: ", count_ngram)
    print("Accuracy N gram: ", count_ngram / count_mistakes)
    print("Count Unsupervised: ", count_unsupervised)
    print("Accuracy Unsupervised: ", count_unsupervised / count_mistakes)
    print("Count Combined: ", count_combined)
    print("Accuracy Combined: ", count_combined / count_mistakes)

    plot_data(plot_ngram, ['count', 'noisy channel', 'n gram channel', 'unsupervised channel', 'combined (n gram, unsupervised)'],
              xlabel='words',
              ylabel='Trigram Count', main= plot_title + 'Trigram Frequency Comparison')


def compare_with_bigram(text, test_ngram_word_list, correct, plot_title = ""):
    bigram = bigram_word(text)
    plot_ngram = [[0.0 for _ in range(len(test_ngram_word_list) + 1)] for _ in range(5)]
    count_mistakes = 0
    count_noisy =0
    count_ngram = 0
    count_unsupervised = 0
    count_combined =0
    for i in range(1, len(test_ngram_word_list) - 1):
        plot_ngram[0][i] = i
        if test_ngram_word_list[i] not in config.word_dict.keys():
            count_mistakes = count_mistakes + 1
            print("\n\n", test_ngram_word_list[i - 1], " ", test_ngram_word_list[i])
            match_list_noisy_channel_test = noisy_channel_evaluation([test_ngram_word_list[i]], config.word_dict,
                                                                     type_of_data='test', skip_notification=True)
            candidates_noisy_channel = []
            if (len(match_list_noisy_channel_test) > 0):
                candidates_noisy_channel = match_list_noisy_channel_test[test_ngram_word_list[i]][0]
            match_list_n_gram_test = ngram_evaluation([test_ngram_word_list[i]], skip_notification=True)
            candidates_n_gram = []
            if (len(match_list_n_gram_test) > 0):
                candidates_n_gram = match_list_n_gram_test[test_ngram_word_list[i]][0]
            match_list_unsupervised_rules_test = unsupervised_rules_evaluation([test_ngram_word_list[i]], skip_notification=True)
            candidates_unsupervised_rules = []
            if (len(match_list_unsupervised_rules_test) > 0):
                candidates_unsupervised_rules = match_list_unsupervised_rules_test[test_ngram_word_list[i]][0]
            for j in range(0, 3):
                expr_noisy = test_ngram_word_list[i - 1] + ' '
                expr_ngram = test_ngram_word_list[i - 1] + ' '
                expr_unsupervised = test_ngram_word_list[i - 1] + ' '
                print("Candidate number: ", j + 1)
                if (len(candidates_noisy_channel) > j):
                    expr_noisy = expr_noisy + candidates_noisy_channel[j][0]
                    if expr_noisy in bigram:
                        if(candidates_noisy_channel[j][0] == correct[count_mistakes -1]):
                            count_noisy = count_noisy+1
                        print("noisy: ", expr_noisy, bigram[expr_noisy], " ",count_noisy, "/", count_mistakes, correct[count_mistakes-1])
                        if (plot_ngram[1][i] < bigram[expr_noisy]):
                            plot_ngram[1][i] = bigram[expr_noisy]
                if (len(candidates_n_gram) > j):
                    expr_ngram = expr_ngram + candidates_n_gram[j][0]
                    if expr_ngram in bigram:
                        if (candidates_n_gram[j][0] == correct[count_mistakes -1]):
                            count_ngram = count_ngram + 1
                        print("ngram: ", expr_ngram, bigram[expr_ngram], " ",count_ngram, "/", count_mistakes, correct[count_mistakes-1])
                        if (plot_ngram[2][i] < bigram[expr_ngram]):
                            plot_ngram[2][i] = bigram[expr_ngram]
                if (len(candidates_unsupervised_rules) > j):
                    expr_unsupervised = expr_unsupervised + candidates_unsupervised_rules[j][0]
                    if expr_unsupervised in bigram:
                        if (candidates_unsupervised_rules[j][0] == correct[count_mistakes -1]):
                            count_unsupervised = count_unsupervised + 1
                        print("unsupervised: ", expr_unsupervised, bigram[expr_unsupervised], " ",count_unsupervised, "/", count_mistakes, correct[count_mistakes-1])
                        if (plot_ngram[3][i] < bigram[expr_unsupervised]):
                            plot_ngram[3][i] = bigram[expr_unsupervised]
                #if (len(candidates_n_gram) > j) and len(candidates_unsupervised_rules) > j:
                #    if candidates_n_gram[j][0]== correct[count_mistakes -1] or candidates_unsupervised_rules[j][0] ==correct[count_mistakes-1]:
                #        count_combined = count_combined + 1
                #        print("combined : ",correct[count_mistakes-1], "/", count_mistakes," ", count_combined)
                if(bigram[expr_unsupervised]> bigram[expr_ngram]):
                    plot_ngram[4][i] = bigram[expr_unsupervised]
                    if(len(candidates_unsupervised_rules) > j):
                        if candidates_unsupervised_rules[j][0] == correct[count_mistakes - 1]:
                            count_combined = count_combined + 1
                            print("combined unsupervised : ",expr_unsupervised, " ", correct[count_mistakes - 1],count_combined, "/", count_mistakes)
                else:
                    plot_ngram[4][i] = bigram[expr_ngram]
                    if (len(candidates_n_gram) > j):
                        if candidates_n_gram[j][0] == correct[count_mistakes - 1]:
                            count_combined = count_combined + 1
                            print("combined ngram: ",expr_ngram, " ", correct[count_mistakes - 1], count_combined, "/", count_mistakes)

    plot_data(plot_ngram, ['count', 'noisy channel', 'n gram channel', 'unsupervised channel','combined (n gram, unsupervised)'],
              xlabel='words',
              ylabel='Bigram Count', main= plot_title + 'Bigram Frequency Comparison')
    print("Count Noisy: ", count_noisy)
    print("Accuracy Noisy Channel: ", count_noisy/ count_mistakes)
    print("Count N gram: ", count_ngram)
    print("Accuracy N gram: ", count_ngram / count_mistakes)
    print("Count Unsupervised: ", count_unsupervised)
    print("Accuracy Unsupervised: ", count_unsupervised / count_mistakes)
    print("Count Combined: ", count_combined)
    print("Accuracy Combined: ", count_combined/count_mistakes)





'''

