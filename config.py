import numpy as np

list_of_filenames = ['Dataset/Frequency.USpresidents.txt'] # following format, one [frequency word] entry, per line in document
mistake_filenames =  ['Dataset/mistakes2.txt'] # following format, one incorrect word per line
ngram_test_filename = 'Dataset/mistakes.txt' # Speech extract of Obama with mistakes
ngram_filename = 'Dataset/FederalistTraining.txt'
# smoothing factor
smoothing_factor = 0.01

# min value to be assigned, when a value is extremely close to zero
min_value = 0.001

# XY in correct word becomes Y in incorrect word
deletion_matrix = np.zeros(shape = (27,26), dtype = int, order = 'C')

# X in correct word becomes XY in incorrect word
addition_matrix = np.zeros(shape = (27,26), dtype = int, order = 'C')

# XY in the correct word becomes YX in the incorrect word
reversal_matrix = np.zeros(shape = (26,26), dtype = int, order = 'C')

# X in the correct word becomes Y in the incorrect word
substitution_matrix = np.zeros(shape = (26,26), dtype = int, order = 'C')

# K iteration value for unsupervised rules based method
K = 4

word_dict = {}

# n gram size
ngram_size = 3
