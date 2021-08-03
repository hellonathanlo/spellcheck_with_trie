# OICR_interview_takehome

## Overview

This is a spell checking script which operates through command line.

The script accepts two files, one for input and another for dictionary checking.
The file contents are then read to determine whether the dictionary file is formatted correctly.
After this determination, the words from each file are collected into dictionaries.
The dictionary is then used as the reference Trie to determine which words within the input
file are "incorrect". A Trie structure was implemented in order to effectively search through
all possible completions of the input words against the dictionary Trie.

Once the dictionary Trie is initialized, the input file is processed and checked against
the dictionary's Trie structure to search for matching words.
By navigating through the Trie for each word from the dictionary, the input file's words which
can't be found within the dictionary can safely be concluded as "incorrect" (i.e. not existing within 
the dictinoary) words. 

Additionally, command_line_help() provides user guidance if spellcheck.py is called with a -h or --help tag. Usage information is detailed once it is called.

## Usage

```python
python spellcheck.py InputFile DictionaryFile
```
