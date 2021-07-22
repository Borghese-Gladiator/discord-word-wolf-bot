from prettytable import PrettyTable

def load_word_pairs(path):
    '''
    @return list of word pairs
    Load word pair tuple list from TXT file
    '''
    word_pairs = []
    with open(path) as f:
        content = f.readlines()
    for line in content:
        line = line.strip() # remove whitespace characters
        two_word_tuple = tuple(line.split(','))
        if len(two_word_tuple) != 2:
            raise Exception("Length of two word tuple is {} instead of 2".format(len(two_word_tuple)))
        word_pairs.append(two_word_tuple)
    return word_pairs
