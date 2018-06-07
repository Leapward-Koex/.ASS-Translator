# .ASS-Translator
A simple script that makes use of Google's translate API to translate an subtitle .ass file (Advanced SubStation Alpha)
The script works by extracting the dialogue lines from the file and parsing them though Google's translator, success of this script is thus dependant on Google's module co-operating with you.

This script outputs a translated version of the input file in the working directory with the tag [Translated] infront of it, select this as your subtitle file in place of the original to use the translated file.

As of now, the script won't translate lines that have text affects located in the middle of line of dialogue.
