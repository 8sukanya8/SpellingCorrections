from ioLocal import count_pattern, add, delete, reverse, substitute
import config,string,time


def noisy_channel_evaluation(train, word_dict, type_of_data, skip_notification = False):
    # Description:
    #   This function finds all candidates for words in the training set as per the noisy_channel approach
    # Args:
    #   training set, size of training set
    # Returns:
    #   a dictionary of dictionaries of words in training set against their candidates with the voting count
    if (not skip_notification):
        print("\n\nNoisy Channel model evaluation started...")
    start_noisy_channel = time.time()
    number_of_terms = sum(config.word_dict.values())
    if(type_of_data == 'train'):
        possible_corrections = spelling_correction_train(train, word_dict.keys()) # for the training set, the operation matrices are updated
    if(type_of_data == 'test'):
        possible_corrections = spelling_correction_test(train, word_dict.keys()) # for the test set, the existing matrices are used
    result = {}
    for i in range(0, len(possible_corrections)):
        intermediate_result = {}
        start = time.time()
        word = possible_corrections[i][0]
        candidate_list = possible_corrections[i][1]
        for candidate in candidate_list:
            candidate_word = candidate[1]
            language_model_probability = find_language_model_probability(candidate,train)  # Setting a very low value instead of zero
            #edit_dist = findEditDist(word, candidate_word)
            candidate_relative_freq_percentage = config.min_value  # so there is no null value problem
            if candidate_word in word_dict:
                candidate_freq = word_dict[candidate_word]
                candidate_relative_freq_percentage = (0.5 + candidate_freq * 100) / number_of_terms
            if candidate_word not in intermediate_result:
                intermediate_result[candidate_word] = candidate_relative_freq_percentage
            #result.append([word, candidate_word, candidate_relative_freq_percentage])
        intermediate_result = sorted(intermediate_result.items(), key=lambda x: x[1], reverse=True)
        end = time.time()
        elapsed =  end - start
        if(len(intermediate_result)>0) and word not in result:
            #result.append([word, intermediate_result])
            result[word] = [intermediate_result, elapsed]
            #print(word, " ", candidate, " lang_model_prob: ", language_model_probability, " relative freq.: ", candidate_relative_freq_percentage)
    end_noisy_channel = time.time()
    average_time_noisy_channel_train = (end_noisy_channel - start_noisy_channel) / len(train)
    if (not skip_notification):
        print("Noisy Channel model evaluation ended")
        print("Total time taken by Noisy Channel:", (end_noisy_channel - start_noisy_channel))
        print("Average time taken by Noisy Channel: ", average_time_noisy_channel_train)
    return result

def find_uncorrectable_words(word_list):
    # Description:
    #   This function calculates how many words did not have any suggestions as per the training set
    # Args:
    #   list of words with candidates
    # Returns:
    #   a count of the number of words without candidates
    count = 0
    for list in word_list:
        if(len(list)==0):
            count = count +1
    return count

def find_language_model_probability(candidate, train):
    # Description:
    #   This function calculates the probability of a candidate according to the language model
    #   from the matrices of addition, deletion, substitution and reversal
    # Args:
    #   training set, candidate for which probability has to be calculated
    # Returns:
    #   probability of a candidate according to the language model

    operation_type = candidate[0] # addition, substraction etc.
    candidate_word = candidate[1]
    char_x = candidate[2]
    char_y = candidate[3]
    #char_y = ''
    #if(candidate[3]):
    #    char_y = candidate[3]
    matrix_val = 0
    language_model_probability = config.min_value # extremely small value instead of  zero
    if (operation_type == 'deletion'):
        positions = get_deletion_matrix_indices(char_x, char_y)
        if (len(positions) > 1):
            matrix_position_x = positions[0]
            matrix_position_y = positions[1]
            if( config.deletion_matrix[matrix_position_x][matrix_position_y] >0):
                matrix_val = config.deletion_matrix[matrix_position_x][matrix_position_y]
            pattern = char_x + char_y
    elif (operation_type == 'addition'):
        positions = get_addition_matrix_indices(char_x, char_y)
        if (len(positions) > 1):
            matrix_position_x = positions[0]
            matrix_position_y = positions[1]
            if (config.addition_matrix[matrix_position_x][matrix_position_y] > 0):
                matrix_val = config.addition_matrix[matrix_position_x][matrix_position_y]
            pattern = char_x
    elif (operation_type == 'substitution'):
        positions = get_substitution_matrix_indices(char_x, char_y)
        if (len(positions) > 1):
            matrix_position_x = positions[0]
            matrix_position_y = positions[1]
            if config.substitution_matrix[matrix_position_x][matrix_position_y] > 0:
                matrix_val = config.substitution_matrix[matrix_position_x][matrix_position_y]
            pattern = char_x
    elif (operation_type == 'reversal'):
        positions = get_reversal_matrix_indices(char_x, char_y)
        if (len(positions) > 1):
            matrix_position_x = positions[0]
            matrix_position_y = positions[1]
            if config.reversal_matrix[matrix_position_x][matrix_position_y] > 0:
                matrix_val = config.reversal_matrix[matrix_position_x][matrix_position_y]
            pattern = char_x + char_y
    else:
        print("Error! Undefined operation: ", operation_type, ". Matrix for this operation does not exist!")
    count = count_pattern(train, pattern)
    if(count>=1):
        #print("matrix value: ", matrix_val, " operation: ", operation_type, " pattern: ", pattern, "count: ", count)
        language_model_probability = matrix_val / count
    return language_model_probability


def get_deletion_matrix_indices(char_x, char_y):
    #matrix_position_x = -1
    #matrix_position_y = -1
    if char_x.isalpha():
        matrix_position_x = ord(char_x) -97  # converting character to position in the matrix
    elif char_x =='':
        matrix_position_x = 26
    else:
        print("Error! Attemting to access non existing character indices in deletion_matrix")
        return
    if char_y.isalpha():
        matrix_position_y = ord(char_y) - 97  # converting character to position in the matrix
    elif char_y =='':
        matrix_position_y = 26
    else:
        print("Error! Attemting to access non existing character indices in deletion_matrix")
        return
    return [matrix_position_x, matrix_position_y]

def update_deletion_matrix (char_x, char_y):
    # Description:
    #   This function updates the deletion matrix for the training set for two characters
    # Args:
    #   two characters, xy in correct word becomes y in incorrect word
    # Returns:
    #   modified deletion matrix
    positions = get_deletion_matrix_indices (char_x, char_y)
    if(len(positions)>1):
        matrix_position_x = positions[0]
        matrix_position_y = positions[1]
        config.deletion_matrix[matrix_position_x][matrix_position_y] = config.deletion_matrix[matrix_position_x][matrix_position_y] + 1
        #print('deletion matrix updated position:', char_x, char_y, matrix_position_x, matrix_position_y)
    else:
        print("Error! Attemting to update non existing character indices in deletion_matrix")
        return

def get_addition_matrix_indices(char_x, char_y):
    #matrix_position_x = -1
    #matrix_position_y = -1
    if char_x.isalpha():
        matrix_position_x = ord(char_x) - 97  # converting character to position in the matrix
    elif char_x == '':
        matrix_position_x = 26
    else:
        print("Error! Attemting to access non existing character indices in addition_matrix")
        return
    if char_y.isalpha():
        matrix_position_y = ord(char_y) - 97  # converting character to position in the matrix
    elif char_y == '':
        matrix_position_y = 26
    else:
        print("Error! Attemting to access non existing character indices in addition_matrix")
        return
    return [matrix_position_x, matrix_position_y]

def update_addition_matrix (char_x, char_y):
    # Description:
    #   This function updates the addition matrix for the training set for two characters
    # Args:
    #   two characters, x in correct word becomes xy in incorrect word
    # Returns:
    #   modified addition matrix
    positions = get_addition_matrix_indices (char_x, char_y)
    if (len(positions) > 1):
        matrix_position_x = positions[0]
        matrix_position_y = positions[1]
        config.addition_matrix[matrix_position_x][matrix_position_y] = config.addition_matrix[matrix_position_x][matrix_position_y] + 1
        #print('addition matrix updated position:', char_x, char_y, matrix_position_x, matrix_position_y)
    else:
        print("Error! Attemting to update non existing character indices in addition_matrix")
        return

def get_reversal_matrix_indices(char_x, char_y):
    if char_x.isalpha() and char_y.isalpha():
        matrix_position_x = ord(char_x) -97  # converting character to position in the matrix
        matrix_position_y = ord(char_y) -97  # converting character to position in the matrix
        return [matrix_position_x, matrix_position_y]
    else:
        print("Error! Attemting to access non existing character indices in reversal_matrix")
        return

def update_reversal_matrix (char_x, char_y):
    # Description:
    #   This function updates the reversal matrix for the training set for two characters
    # Args:
    #   two characters, xy in correct word becomes yx in incorrect word
    # Returns:
    #   modified reversal matrix

    positions = get_reversal_matrix_indices(char_x, char_y)
    if (len(positions) > 1):
        matrix_position_x = positions[0]
        matrix_position_y = positions[1]
        config.reversal_matrix[matrix_position_x][matrix_position_y] = config.reversal_matrix[matrix_position_x][matrix_position_y] +1
        #print('reversal matrix updated position:', char_x, char_y, matrix_position_x, matrix_position_y)
    else:
        print("Error! Attemting to update non existing character indices in reversal_matrix")

def get_substitution_matrix_indices(char_x, char_y):
    if char_x.isalpha() and char_y.isalpha():
        matrix_position_x = ord(char_x) -97  # converting character to position in the matrix
        matrix_position_y = ord(char_y) -97  # converting character to position in the matrix
        return [matrix_position_x, matrix_position_y]
    else:
        print("Error! Attemting to access non existing character indices in reversal_matrix")
        return


def update_substitution_matrix (char_x, char_y):
    # Description:
    #   This function updates the substitution matrix for the training set for two characters
    # Args:
    #   two characters, x in correct word becomes y in incorrect word
    # Returns:
    #   modified substitution matrix
    positions = get_reversal_matrix_indices(char_x, char_y)
    if (len(positions) > 1):
        matrix_position_x = positions[0]
        matrix_position_y = positions[1]
        config.substitution_matrix[matrix_position_x][matrix_position_y] = config.substitution_matrix[matrix_position_x][matrix_position_y] +1
        #print('substitution matrix updated position:', char_x, char_y, matrix_position_x, matrix_position_y)
    else:
        print("Error! Attemting to update non existing character indices in substitution_matrix")


def spelling_correction_train(check_list, correct_words):
    # Description:
    #   This function checks a list of words (TRAINING set) by looking up a dictionary.
    #   If present, the word is ignored.
    #   If a word is not present, it attempts to find the best matches in the dictionary.
    #   This also builds the different matrices according to the type of operation applied to obtain the word,
    #   namely addition, deletion, substitution and reversal
    #   If no matches are found, it returns a null list as a match
    # Args:
    #   given check_list, dictionary
    # Returns:
    #   a list of type of operation, modified word, characters modified per word

    result = []
    for entry in check_list:
        word = entry.lower()
        possible_corrections = [] # contains a list of candidates with the corresponding operations and the position of the operation
        if word not in correct_words:
            for i in range(0, len(word)):
                deletion = delete(word, i) # deleting in the incorrect word, means adding to the correct word. This means that the matrix for addition must be updated
                if deletion in correct_words:
                    char_x = ''  # letter in word is deleted, so both characters can be picked from word
                    if(i>0):
                        char_x = word[i-1]
                    char_y = word[i]
                    update_addition_matrix(char_x, char_y) # Attention! Just as the correct word is formed by addition, the incorrect word is formed by deletion. developement->development qualifies as a deletion problem but commends change in the addition matrix
                    #possible_corrections.append(deletion)
                    possible_corrections.append(['deletion',deletion, char_x, char_y])
                    #possible_corrections.append("By deletion: " + deletion)
                    #print(word, ": By deletion: " , deletion, " position: ", i ,"\n")
                    #break
            for i in range(0, len(word) - 1):
                reversal = reverse(word, i)
                if reversal in correct_words:
                    char_x = word[i] # letters XY in word is reversed to YX
                    char_y = word[i+1]
                    update_reversal_matrix(char_x, char_y)
                    #possible_corrections.append(reversal)
                    possible_corrections.append(['reversal', reversal, char_x, char_y])
                    #possible_corrections.append("By reversal: " + reversal)
                    #print(word, ": By reversal: " + reversal, " position: ", i ,"\n")
                    #break
            for i in range(0, len(word)):
                for j in list(string.ascii_lowercase):
                    substitution = substitute(word, j, i)
                    if substitution in correct_words:
                        char_x = word[i]  # letter in word substituted by letter in substitution
                        char_y = substitution[i]
                        update_substitution_matrix(char_x,char_y)
                        #possible_corrections.append(substitution)
                        possible_corrections.append(['substitution', substitution, char_x, char_y])
                        #possible_corrections.append("By substitution: " + substitution)
                        #print(word, ": By substitution: " + substitution, " position: ", i ,"\n")
                        #break
            for i in range(0, (len(word) + 1)):
                for j in list(string.ascii_lowercase):
                    addition = add(word, j, i)
                    if addition in correct_words:
                        #char_x = word[i]  # letters X in correct word is becomes to XY in the incorrect word
                        char_x = ''
                        if (i-1)>0:
                            char_x = addition[i-1]
                        char_y = addition[i]#+ 1]
                        update_deletion_matrix(char_x, char_y) # Attention! Just as the correct word is formed by addition, the incorrect word is formed by deletion. developement->development qualifies as a deletion problem but commends change in the addition matrix
                        #possible_corrections.append(addition)
                        possible_corrections.append(['addition', addition, char_x, char_y])
                        #possible_corrections.append("By addition: " + addition)
                        #print(word, ": By addition: " + addition, " position: ", i ,"\n")
                        #break
                        # print(word)
                        # if(len(possible_corrections)>0):
                        #    print(possible_corrections)

            result.append([word, possible_corrections])
    return result

def spelling_correction_test(check_list, correct_words):
    # Description:
    #   This function checks a list of words (TEST set) by looking up a dictionary.
    #   If present, the word is ignored.
    #   If a word is not present, it attempts to find the best matches in the dictionary.
    #   If no matches are found, it returns a null list as a match
    # Args:
    #   given check_list, dictionary
    # Returns:
    #   a list of type of operation, modified word, characters modified per word

    result = []
    for entry in check_list:
        word = entry.lower()
        possible_corrections = [] # contains a list of candidates with the corresponding operations and the position of the operation
        if word not in correct_words:
            for i in range(0, len(word)):
                deletion = delete(word, i) # deleting in the incorrect word, means adding to the correct word. This means that the matrix for addition must be updated
                if deletion in correct_words:
                    char_x = ''  # letter in word is deleted, so both characters can be picked from word
                    if(i>0):
                        char_x = word[i-1]
                    char_y = word[i]
                    possible_corrections.append(['deletion',deletion, char_x, char_y])
                    #print(word, ": By deletion: " , deletion, " position: ", i ,"\n")
                    #break
            for i in range(0, len(word) - 1):
                reversal = reverse(word, i)
                if reversal in correct_words:
                    char_x = word[i] # letters XY in word is reversed to YX
                    char_y = word[i+1]
                    possible_corrections.append(['reversal', reversal, char_x, char_y])
                    #print(word, ": By reversal: " + reversal, " position: ", i ,"\n")
                    #break
            for i in range(0, len(word)):
                for j in list(string.ascii_lowercase):
                    substitution = substitute(word, j, i)
                    if substitution in correct_words:
                        char_x = word[i]  # letter in word substituted by letter in substitution
                        char_y = substitution[i]
                        possible_corrections.append(['substitution', substitution, char_x, char_y])
                        #print(word, ": By substitution: " + substitution, " position: ", i ,"\n")
                        #break
            for i in range(0, (len(word) + 1)):
                for j in list(string.ascii_lowercase):
                    addition = add(word, j, i)
                    if addition in correct_words:
                        #char_x = word[i]  # letters X in correct word is becomes to XY in the incorrect word
                        char_x = ''
                        if (i-1)>0:
                            char_x = addition[i-1]
                        char_y = addition[i]#+ 1]
                        possible_corrections.append(['addition', addition, char_x, char_y])
                        #print(word, ": By addition: " + addition, " position: ", i ,"\n")
                        #break
                        # print(word)
                        # if(len(possible_corrections)>0):
                        #    print(possible_corrections)
            result.append([word, possible_corrections])
    return result

