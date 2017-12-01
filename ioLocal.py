import re
import numpy as np, matplotlib.pyplot as plt


def readWholeText(filename):
    # Description:
    #   Uses a file path and reads the file and returns the whole text as a string
    # Args:
    #   Filepath
    # Returns:
    #   A string
    with open(filename) as f:
        lines = f.read()
    return lines


def splitText(text):
    # Description:
    #   Splits the text into words as per delimiters
    # Args:
    #   text
    # Returns:
    #   A list of split words
    text = re.sub(r'\n', r' ', text)
    text = re.sub(r',', r'', text)
    text = re.sub(r'\'', r'', text)
    text = re.sub(r'\.', r'', text)
    text = re.sub(r'"', r'', text)
    text = re.sub(r'-', r' ', text)
    text = re.sub(r';', r'', text)
    text = re.sub(r'<', r'', text)
    text = re.sub(r'>', r'', text)
    text = re.sub(r'\?', r' ', text)
    text = re.sub(r'\\', r' ', text)
    text = re.sub(r'/', r' ', text)
    text = re.sub(r'\(', r'', text)
    text = re.sub(r'\)', r' ', text)
    text = re.sub(r':', r'', text)
    words = text.split()
    return words


def readFileIntoList(filepath="~/"):
    # Description:
    #   Uses a file path and reads the file and returns a tokenized list of words in small letters
    # Args:
    #   Filepath
    # Returns:
    #   List of correct email adresses
    print("Reading file at" + filepath)
    # delimiters = ['\n', ' ', ',', '.', '?', '!', ':', 'and_what_else_you_need']
    try:
        text = open(filepath).read().lower()
        text = re.sub(r'\n', r' ', text)
        text = re.sub(r',', r'', text)
        text = re.sub(r'\'', r'', text)
        text = re.sub(r'\.', r'', text)
        text = re.sub(r'"', r'', text)
        text = re.sub(r'-', r' ', text)
        text = re.sub(r';', r'', text)
        text = re.sub(r'<', r'', text)
        text = re.sub(r'>', r'', text)
        text = re.sub(r'\?', r' ', text)
        text = re.sub(r'\\', r' ', text)
        text = re.sub(r'/', r' ', text)
        text = re.sub(r'\(', r'', text)
        text = re.sub(r':', r'', text)
        text = re.sub(r'\)', r' ', text)
        words = text.split()
        return words
    except FileNotFoundError:
        print("\nFile not found at path", filepath)
    except UnboundLocalError:
        print("\nCheck variable returned", filepath)
    return


'''   
def writeListToFile(list, filename= "text.txt"):
    # Description:
    #   Writes a list onto a filepath
    # Args:
    #   List
    #   Filepath
    # Returns:
    #   Nothing
    file = open(filename, 'w')
    rows = len(list)
    
    if(rows == 0):
        print("Empty List!")
        return 
    cols = len(list[0])
    if (cols >0):
        try:
            for i in range(0,rows):
                file.write("\n")
                for j in range(0,cols):
                    file.write("\t%s" %list[i][j])
            print("\nFile has been written at", filename)
            file.close()
        except FileNotFoundError:
            print("\nFilepath not found ", filename)
    else:
        try:
            for i in range(0,rows):
                file.write("\n%s" %list[i])
            print("\nFile has been written at", filename)
            file.close()
        except FileNotFoundError:
            print("\nFilepath not found ", filename)
'''


def writeListToFile(list, filename="text.txt"):
    # Description:
    #   Writes a list onto a filepath
    # Args:
    #   List
    #   Filepath
    # Returns:
    #   Nothing
    file = open(filename, 'w')
    rows = len(list)

    if rows == 0:
        print("Empty List!")
        return

    try:
        for i in range(0, rows):
            row = list[i]
            cols = len(row)
            file.write("\n")
            for j in range(0, cols):
                file.write("%s" % row[j])
        print("\nFile has been written at", filename)
        file.close()
    except FileNotFoundError:
        print("\nFilepath not found ", filename)


def create_dict_stem(words):
    # Description:
    #   Given a list of words, returns a dictionary of the stem values
    # Args:
    #   a list of words
    # Returns:
    #   a dictionary of stem words
    print("\nCreating Dictionary \n")
    if (len(words) < 1):
        print("Error! Empty input")
        return
    word_dict = {}
    for word in words:
        if (len(word) > 0):
            stem_word = stemmer(word)
            count = 0
            if stem_word in word_dict:
                count = word_dict[stem_word]
                count = count + 1
                word_dict[stem_word] = count
            else:
                word_dict[stem_word] = 1
    return word_dict


def create_dict_stem_from_freq_list(lines, word_dict={}):
    # Description:
    #   Given a frequency list (lines of word_freq), and a dictionary (optional),  returns a dictionary of the stem values
    # Args:
    #   a list of words and their frequencies, optional dictionary
    # Returns:
    #   a dictionary of stem words
    for line in lines:
        words = line.lower().split(' ')
        if len(words[1]) > 0:
            stem_word = stemmer(words[1])
            if stem_word in word_dict:
                count = word_dict[stem_word]
                count = count + int(words[0])
                word_dict[stem_word] = count
            else:
                word_dict[stem_word] = int(words[0])
    return word_dict


def stemmer(word):
    # Description:
    #   Given a word, returns the stem value (if possible) as per given rules of stemming
    # Args:
    #   a word
    # Returns:
    #   a stem word if possible else given word
    transformed_word = ""
    if (len(word) < 5):
        # print('Skipping \"'+word+'\" as length is shorter than 5 characters!')
        return word
    if (re.search(r'[^e|a]ies$', word)):  # if word ends in 'ies' replace by 'y'
        transformed_word = re.sub(r'ies$', 'y', word)
    elif (re.search(r'[^e|a|o]es$', word)):
        transformed_word = re.sub(r'es$', 'e', word)  # if word ends in 'es' replace by 'e'
    elif (re.search(r'[^u|s]s$', word)):
        transformed_word = re.sub(r's$', '', word)  # if word ends in 's' delete 's'
    if (len(transformed_word) < 1):
        return word
    return transformed_word


def find_edit_dist(s1, s2):
    # Description:
    #   This function finds Levenstein edit distance between two strings
    # Args:
    #   two strings
    # Returns:
    #   edit distance
    if (len(s1) == 0 and len(s2) == 0):
        print(" Strings must be non empty!")
        return
    s1 = "0" + s1  # adding epsilon for empty character
    s2 = "0" + s2  # adding epsilon for empty character
    len_s1 = len(s1)
    len_s2 = len(s2)
    editDist = np.zeros((len_s1, len_s2))
    for i in range(1, len_s1): # addition to Y axis word
        editDist[i][0] = editDist[i - 1][0] + 1
    for j in range(1, len_s2): # addition to X axis word
        editDist[0][j] = editDist[0][j - 1] + 1
    for i in range(1, len_s1): # substitution
        for j in range(1, len_s2):
            dist_add = editDist[i - 1][j] + 1
            dist_del = editDist[i][j - 1] + 1
            dist_rev = dist_add # assigning some value so that it is not selected as minimum
            dist_weighted = 0
            if (s1[i] != s2[j]):
                # print(s1[i] + " " + s2[j])
                dist_weighted = 1
            dist_sub = editDist[i - 1][j - 1] + dist_weighted
            if i>=2 and j>=2 and i<len(s1) and j < len(s2) :
                if(s1[i]==s2[j-1]) and (s2[j]==s1[i-1]):
                    dist_rev = editDist[i - 2][j - 2]+1
            #print("i: " , i , " j: ", j, " add: ", dist_add, " del: ", dist_del, " rev: ", dist_rev, " sub: ", dist_sub)
            editDist[i][j] = min(dist_add, dist_del, dist_sub, dist_rev)
    #print("\n ", end="")
    #for i in range(0, len_s2):
    #    print("  ", s2[i], end="")
    #print("\n")
    #for i in range(0, len_s1):
    #    print(s1[i], editDist[i,])
    editDistValue = editDist[len(editDist) - 1][len(editDist[1,]) - 1]
    #print("The Damerau Levenstein edit distance is: ", editDistValue)
    return editDistValue


def count_pattern(words, pattern):
    # Description:
    #   This function counts the number of times a pattern occurs in a list of words
    # Args:
    #   list of words, a pattern to search
    # Returns:
    #   a count of the number of times a pattern was found in the list

    #if len(pattern) > 0 :
    count = 0
    for word in words:
        count = count + len(re.findall(pattern, word))
    return count
    #else:
    #    print("Error! Attempting to find empty pattern in a word: ", pattern)

def matching_pattern(words, pattern):
    # Description:
    #   This function returns iterates over a list of words, and returns those that matches the given pattern
    # Args:
    #   list of words, a pattern to search
    # Returns:
    #   a list of the words that match the pattern
    result = []
    for word in words:
        candidate = re.match(pattern,word)
        if(candidate):
            result.append(word)
    return result



def delete(word, position=0, numOfChar=1):
    # This function deleted one or more characters from the specified position
    #
    #
    # Arguments: given word, position, number of characters to be deleted
    # Returns: modified word
    if (position < 0) or (numOfChar < 1):
        print("Error! Deletion position cannot be negative and minimum chars to delete must be atleast one")
        return
    if (position + numOfChar > len(word)):
        print("Error! Trying to delete more characters than present")
        return
    first_part = word[0: position]
    second_part = word[position + numOfChar: len(word)]
    return first_part + second_part


def reverse(word, position=0):
    # Description:
    #   This function swaps characters at the specified position
    # Args:
    #   given word, position
    # Returns:
    #   modified word
    if (position < 0):
        print("Error! reverse position cannot be negative")
        return
    if (position + 1 >= len(word)):
        print("Error! Trying to reverse chars more than the length of the word")
        return
    char_1 = word[position]
    char_2 = word[position + 1]
    first_part = word[:position]
    if (position + 2 <= len(word)):
        second_part = word[position + 2: len(word)]
    else:
        second_part = ""
    return first_part + char_2 + char_1 + second_part


def substitute(word, new_char, position=0):
    # Description:
    #   This function replaces a character at the specified position with a new character
    # Args:
    #   given word, new character, position
    # Returns:
    #   modified word
    if (position < 0) or (position >= len(word)):
        print(
            "Error! substitution position cannot be negative. substitution Position cannot be greater than length of word")
        return
    if (new_char):
        first_part = word[:position]
        if (position + 1 < len(word)):
            second_part = word[position + 1: len(word)]
        else:
            second_part = ""
        # print(first_part)
        # print(new_char)
        # print(second_part)
        return first_part + new_char + second_part
    else:
        print("Error! substitution character cannot be empty")


def add(word, new_char, position=0):
    # Description:
    #   This function adds a new character at the specified position
    # Args:
    #   given word, new character, position
    # Returns:
    #   modified word
    if (position < 0) or (position > len(word)):
        print("Error! Addition position cannot be negative or greater than the length of the word")
        return
    if (new_char):
        first_part = word[:position]
        if (position < len(word)):
            second_part = word[position: len(word)]
        else:
            second_part = ""
        return first_part + new_char + second_part
    else:
        print("Error! Addition character cannot be empty")

def word_frequency_voting(words):
    word_freq_dict = {}
    number_of_words = len(words)
    word_set = set(words)
    for word in word_set:
        if word not in word_freq_dict:
            word_freq_dict[word] = words.count(word)
    for word in word_freq_dict.keys(): # normalised voting for over all votes cast. Note that all votes cast == number of candidates
        word_freq_dict[word] = word_freq_dict[word]/number_of_words
    return word_freq_dict


def plot_data(data, row_name_list, xlabel = '', ylabel = '', main = ''):
    rows = len(data)
    design = ['ro','bs', 'g^']
    if(rows != len(row_name_list)):
        print("Error! Unnamed columns exist!")
        return
    for i in  range (1, rows):
        plt.plot(data[0], data[i], design[i-1], label=row_name_list[i])
    #plt.plot(plot_time[0], plot_time[2], , label='n gram channel')
    #plt.plot(plot_time[0], plot_time[3], 'g^', label='unsupervised channel')
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(s=main, loc='center')
    plt.legend(loc='upper right')
    plt.show()
    return

