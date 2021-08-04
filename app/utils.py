import random

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

def generate_dad_joke():
    DAD_JOKES = [
        "\"Why do fathers take an extra pair of socks when they go golfing?\" \"In case they get a hole in one!\"')",
        "\"What do a tick and the Eiffel Tower have in common?\" \"They're both Paris sites.\"",
        "\"What do you call a factory that makes okay products?\" \"A satisfactory.\""
    ]
    return random.choice(DAD_JOKES)

def get_rules():
    return "Who among you is the wolf with a different word?\n1. Every player receives a word\n2. One player has a different word from the rest\n3. Discuss to find the imposter\n4. Vote on the person you belive to be the imposter"

def get_word_pairs():
    return [
        ("Eiffel Tower","State of Liberty"),
        ("Fireworks","Guns"),
        ("Light","Dark"),
        ("USA","China"),
        ("Water Flea","Locust"),
        ("Schools","Military"),
        ("Dell","Apple"),
        ("MIT","Harvard")
    ]