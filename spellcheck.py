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
- inputFile
    - lowercase() and remove punctuation for comparison
- dictionaryFile
    - Process into set datatype for comparison
"""

import sys
import re
import unittest
import argparse
import time


def command_line_help():
    """
    This is a simple command line help directory to guide users on the usage of this program.
    It describes how users are expected to input an input file and dictionary file in the positional
    arguments of 1 and 2 after calling this file.
    :return: command line help and instructions
    """
    """
    Identify dictionary file vs input file and return error when identified
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
        file = open(self.input_file)

        number_of_lines = 0
        number_of_words = 0
        for line in file:
            line = line.strip('\n')

            words = line.split()
            number_of_lines += 1
            number_of_words += len(words)

        return number_of_lines/number_of_words

    def process_input(self):
        """
        The process_input function accepts a file and reads all words from it using the regular expression '\w+'.
        By finding all words in the file and processing them into lowercase strings, there is a uniform foundation for
        comparing words from the input file and the dictionary file.
        :return: word_list, a set of words from the inputted file, set to lower case for comparison
        """
        regex = r'\w+'

        with open(self.input_file) as file:
            file_content = file.read()

        word_list = re.findall(regex, file_content)

        word_list = [word.lower() for word in word_list]

        sorted_input_dictionary = {}

        for word in word_list:
            if word[0] not in sorted_input_dictionary.keys():
                sorted_input_dictionary[word[0]] = set()
                sorted_input_dictionary[word[0]].add(word)
            else:
                if word not in sorted_input_dictionary[word[0]]:
                    sorted_input_dictionary[word[0]].add(word)

        return sorted_input_dictionary


class SpellCheck(object):
    """
    The SpellCheck class functions as a method to call the damerau_levenshtein_distance function iteratively then
    return the results of the spell checking. This class accepts the input set and dictionary set from the
    ProcessFiles class and calls them within the read_dictionary function.

    """

    def __init__(self, processed_input, processed_dictionary):
        self.processed_input = processed_input
        self.processed_dictionary = processed_dictionary

    def read_dictionary(self):
        """
        The read_dictionary() function takes in the processed_input and processed_dictionary variables to compare
        their corresponding keys (i.e. all input words starting with A will be compared against the dictionary
        items under key A).

        First, matching and mismatched keys are determined. By doing so, read_dictionary() can then determine
        which items within the processed_input dict variable can be found within the items in the processed_dictionary
        dict variable. The mismatched keys covers any keys in processed_input that can't be found in processed_dictionary.

        Additionally, numeric entries are corrected for within the processed_input dict, as they're outside the scope
        of the expected data of the dictionary input.

        :param input_set: word set of all words in input file
        :return: all incorrect words, delimited by new lines
        """

        """
        1. Iterate through D-L Distance
            1a. for loop on dictionary
            1b. for loop on input file
        2. Append to overall list
        3. If any values in dictionary = 0, drop that entry
        4. Return remaining results  
        """

        """
        organize all words in dictionary and input file into an alphabetically ordered dictionary
        i.e. all words arranged into key:value of matching first character letter
        call D-L distance according to these pairs
        figure out a way to run the calls against dictionary terms which match first character
        """

        shared_keys = sorted(set(self.processed_input.keys()).intersection(self.processed_dictionary.keys()))
        missing_keys = sorted(set(self.processed_input.keys()) - set(self.processed_dictionary.keys()))
        alpha_missing_keys = [key for key in missing_keys if not(key.isdigit())]

        incorrect_words = []

        for keys in shared_keys:
            for words in self.processed_input[keys]:
                if words not in self.processed_dictionary[keys]:
                    incorrect_words.append(words)
                    print(words)

        for key in alpha_missing_keys:
            for words in self.processed_input[key]:
                incorrect_words.append(words)
                print(words)

        return sorted(incorrect_words)


def main():
    """
    The main function directs the sequence of operations in this script.

    Firstly, the input file and dictionary file are accepted into the ProcessFiles class to be processed,
    then the outputs are sent over to the SpellCheck class.

    The SpellCheck class then calls the read_dictionary function which compares the words in the
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

        if input_processing.check_file_format() != 1 and dictionary_processing.check_file_format() == 1:
            end_file_check = time.time()
            print('Function check_file_format() took: ' + str(end_file_check - start_file_check) + ' seconds\n')
            print('Checking input words against dictionary!\n')
            processed_input = input_processing.process_input()
            processed_dictionary = dictionary_processing.process_input()

            check_spelling = SpellCheck(processed_input, processed_dictionary)

            start_time = time.time()
            check_spelling.read_dictionary()
            end_time = time.time()
            print("read_dictionary() took: " + str(end_time - start_time) + ' seconds')
        else:
            end_file_check = time.time()
            print('File format checking took: ' + str(end_file_check - start_file_check) + ' seconds')
            print('The input and dictionary files haven\'t been formatted properly, please format your files correctly!')
            sys.exit()

    class SpellCheckTesting(unittest.TestCase):
        """
        The SpellCheckTesting class is a quick unit test to sanity check my development with the spell checker.
        By knowing the expected output, I can test the results during development and be certain that I'm developing
        towards the correct direction.
        """

        """def test_spell_checking(self):
            self.assertEqual(calculate_damerau_levenshtein_distance('a', 'a'),
                             0)
            self.assertEqual(calculate_damerau_levenshtein_distance('ab', 'ba'),
                             1)
            self.assertEqual(calculate_damerau_levenshtein_distance('abcd', 'bac'),
                             2)
            self.assertEqual(calculate_damerau_levenshtein_distance('abcde', 'bac'),
                             3)
            self.assertEqual(calculate_damerau_levenshtein_distance('abcde', 'ba'),
                             4)
            self.assertEqual(SpellCheck(ProcessFiles('Inputfile').process_input(),
                                        ProcessFiles("Dictionaryfile").process_input()).read_dictionary(),
                             dict.fromkeys(['difficlt', 'documnt', 'words']).keys())"""

    #unit_testing = SpellCheckTesting()
    #unit_testing.test_spell_checking()


if __name__ == "__main__":
    main()
