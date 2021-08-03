"""
Requirements to account for:
- accepts two inputs:
    - test (i.e. contains incorrect words) file that's ASCII text, delimited by whitespace
    - dictionary (i.e. contains correct words) file that's ASCII text, delimited by newline
- outputs:
    - list of words not found in dictionary file

Considerations:
- Re: Novrig article
    - Determine probabilities of words against dictionary (i.e. implement levenshtein distance of each word)
    - Return max() candidate of words (i.e. most probable correction) using probabilities
    - Consider edits (e.g. splits, deletes, transposes, replaces, inserts)
- Re: Wikipedia Damerau-Levenshtein Distance
    - Follow pseudocode and produce algorithm to calculate edit distances
        - Entries with 0 distance are same as those in the dictionary
- Re: Trie
    - Follow implementations of Trie
        - Entries which can't be found in dictionary Trie spit out as "incorrect" words
- inputFile
    - lowercase() and remove punctuation for comparison
- dictionaryFile
    - Process into set datatype for comparison
"""

import sys
import re
import argparse
import time


def command_line_help():
    """
    This is a simple command line help directory to guide users on the usage of this program.
    It describes how users are expected to input an input file and dictionary file in the positional
    arguments of 1 and 2 after calling this file.
    :return: command line help and instructions
    """

    parser = argparse.ArgumentParser(prog='spellcheck',
                                     usage='python %(prog)s.py i d',
                                     description='''A Spell Checking Python3 script on Command Line.''',
                                     epilog="""Have a great weekend!""")
    parser.add_argument('i', nargs='*', type=str, default='Inputfile',
                        help='The file that you intend to compare against the dictionary.')
    parser.add_argument('d', nargs='*', type=str, default='Dictionaryfile',
                        help='The file that you intend to use as the dictionary.')

    args = parser.parse_args()

    return args


class ProcessFiles(object):
    """
    The Processfiles class takes any file input and processes them into a set data type
    for a baseline comparison between the input and dictionary files. The process_input
    function reads the files using the regex pattern '\w+' then enforces lower case on all strings.
    After this step, the list of words is processed into a set data type in order
    to correct for duplicate entries, decreasing processing time by minimizing loop iterations.
    """

    def __init__(self, input_file):
        self.input_file = input_file

    def check_file_format(self):
        """
        The check_file_format funciton accepts a file and reads each line of the file into a list.
        If the ratio of lines to words is not 1, then it can be safely assumed that the user mixed the dictionary
        and input files during the script call.
        :return: ratio of lines to words
        """
        file = open(self.input_file)

        number_of_lines = 0
        number_of_words = 0
        for line in file:
            line = line.strip('\n')

            words = line.split()
            number_of_lines += 1
            number_of_words += len(words)

        return number_of_lines / number_of_words

    def process_input(self):
        """
        The process_input function accepts a file and reads all words from it using the regular expression '\w+'.
        By finding all words in the file and processing them into lowercase strings, there is a uniform foundation for
        comparing words from the input file and the dictionary file.
        :return: word_list, a set of words from the inputted file, set to lower case for comparison
        """

        with open(self.input_file) as file:
            file_content = file.read()

        word_list = re.findall(r'\w+', file_content)

        word_list = [word.lower() for word in word_list]

        word_set = set(word_list)

        return word_set


class Node:
    """
    The Node class initializes each node of the Trie. These nodes are the base unit which accept
    each character of the string and act as the base unit of the Trie data structure.
    """

    def __init__(self, value):
        self.value = value
        self.children = dict()
        self.end = False

    def __getitem__(self, key):
        if key in self.children:
            return self.children[key]

        return None

    def __setitem__(self, key, value):
        self.children[key] = value

    def __contains__(self, value):
        return value in self.children

    def __str__(self):
        return str(self.value)


class Trie:
    """
    The Trie class initializes an empty Node class to then populate with the letters which make up the strings of
    each word (i.e. end node). The Trie structure is produced by adding a letter to each subsequent node to "build"
    strings until no more letters can be provided. By building this structure, words can be effectively sought for
    within a tree data structure.
    """

    def __init__(self):
        self.root = Node('')

    def add(self, word):
        word = word.strip()
        node = self.root
        for letter in word:
            next_letter = node[letter]
            if next_letter is not None:
                node = next_letter
            else:
                node[letter] = Node(letter)
                node = node[letter]
        node.end = True

    def __contains__(self, word):
        node = self.root
        for letter in word:
            if letter not in node:
                return False
            node = node[letter]

        if node.end:
            return True
        return False


class SpellCheck(object):
    """
    The Spellcheck class adds all dictionary file words into the Trie in order to cross reference the word list against
    the input file Trie. The __init__ adds the dictionary file's words into its own Trie then checks if the input
    file's words are in the dictionary Trie. If the input file's words can't be found, they're printed out as
    incorrect words.
    """

    def __init__(self, processed_dictionary):
        self.processed_dictionary = processed_dictionary
        self.words = Trie()
        for word in self.processed_dictionary:
            self.words.add(word)

    def spellcheck(self, word):
        """
        The spellcheck function determines whether the words in the input Trie are in the dictionary Trie. If the
        input words aren't found in the dictionary, the words are appended into the incorrect_words list, printed,
        and then returned as a list.
        :param word:
        :return: incorrect_words list
        """

        incorrect_words = []

        if word not in self.words:
            incorrect_words.append(word)
            print(word)

        return incorrect_words


def main():
    """
    The main function directs the sequence of operations in this script.

    Firstly, the input file and dictionary file are accepted into the ProcessFiles class to be processed,
    then the outputs are sent over to the SpellCheck class.

    The SpellCheck class then calls the spellcheck() function which compares the words in the
    input file against the words in the dictionary file to determine misspellings.

    :return: all input file words not found in the dictionary file
    """

    command_line_help()

    if len(sys.argv) <= 1:
        print('Please input the input files and dictionary files!')
        sys.exit()
    elif len(sys.argv) > 3:
        print('Oops, too many arguments this time!')
        sys.exit()
    else:
        input_processing = ProcessFiles(sys.argv[1])
        dictionary_processing = ProcessFiles(sys.argv[2])

        start_file_check = time.time()
        print('Checking file format correctness!')

        if dictionary_processing.check_file_format() == 1:
            end_file_check = time.time()
            print('Function check_file_format() took: ' + str(end_file_check - start_file_check) + ' seconds\n')
            print('Checking input words against dictionary!\n')
            trie = Trie()

            processed_input = input_processing.process_input()

            # Correcting for all digits and ordinal numbers in the input text
            processed_input = [word for word in processed_input if not re.match(r'\d+', word)]

            processed_dictionary = dictionary_processing.process_input()

            for word in processed_input:
                trie.add(word)
                try:
                    assert (word in trie)
                except AssertionError:
                    print(word)
                    sys.exit()

            spell_check_start_time = time.time()
            check_spelling = SpellCheck(processed_dictionary)

            for word in processed_input:
                check_spelling.spellcheck(word)

            spell_check_end_time = time.time()
            print('Function spellcheck() took: ' + str(spell_check_end_time - spell_check_start_time) + ' seconds')

            sys.exit()

        else:
            end_file_check = time.time()
            print('File format checking took: ' + str(end_file_check - start_file_check) + ' seconds')
            print('The dictionary file hasn\'t been formatted properly, please format your file correctly!')
            sys.exit()


if __name__ == "__main__":
    main()
