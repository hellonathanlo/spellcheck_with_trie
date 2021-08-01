# OICR_interview_takehome

## Overview

This is a spell checking script which operates through command line.

The script accepts two files, one for input and another for dictionary checking.
The file contents are then read to determine whether the dictionary file is formatted correctly.
After this determination, the words from each file are collected into dictionaries.
The dictionaries are organized by alphabetical keys which correspond to words starting with the same letter.
By organizing these word lists in alphabetical order, the script can then scan through both word lists according to the same key (i.e. letter).
To account for words starting with letters which aren't found in the dictionary dataset, a set subtraction is performed on the input and dictionary keys
to filter for the remaining input keys. The "missing key" values are then output, finishing the execution of the file.

Additionally, command_line_help() supports usage if spellcheck.py is called with a -h tag. Usage information is detailed once it is called.
