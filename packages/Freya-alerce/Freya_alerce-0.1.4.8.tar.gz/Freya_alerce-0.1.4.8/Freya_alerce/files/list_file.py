import fileinput #replace into files
import Freya_alerce.catalogs # __path__
import os

"""
Class to replace words in files.
"""
class Files():
    """
    Replace a 'word' for 'new word' in specific file.
    """
    def __init__(self,paths,raplace_word,word):
        self.list_path = paths
        self.replace_word = raplace_word
        self.word = word

    def replace_in_files(self):
        for file in self.list_path:
            with fileinput.FileInput(f'{file}', inplace=True) as file_:
                for line in file_:
                    print(line.replace(f'{self.replace_word}', f'{self.word}'), end='')
