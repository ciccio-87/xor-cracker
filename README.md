# xor-cracker

A very simple (and probably not so effective) multibyte XOR cypher cracker,
slightly inspired by https://github.com/ThomasHabets/xor-analyze.

It depicts the most basic techniques to solve a vigenere-like cypher:

- detect the key length by coincidences analysis
- solve n (= key length) resulting caesar cyphers with frequency analysis

For the second stage, xor-cracker needs a frequency file, and two
precomputed ones are provided (one with frequencies from Linux 4.1 sources
and the other extracted from the file collection of http://textfiles.com).

You can use freq.py utility to compute your own (just pipe file paths into it).


