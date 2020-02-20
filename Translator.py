#VM Translator

import TranslationDictionary

dictionary = TranslationDictionary.Dictionary()
sourceFile = "source.vm"


if(__name__ == "__main__"):
    source = open(sourceFile, "r").readlines()
    for line in source:
        print(line)
    print(dictionary.push(2))
