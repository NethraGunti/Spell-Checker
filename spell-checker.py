from collections import Counter
import re

class SpellChecker:
    def __init__(self, word, W=10):
        self.word = word
        self.W=W
        self.candidates = []
        self.dictionary = {}
        self.N = 0
        self.suggestions = []
    
    def priorOfWord(self, word):
        """
        Language Model Probability
        """
        return self.dictionary[word]/self.N
    
    def likelihoodOfWord(self):
        """
        Channel Model Probability
        """
        return 1/len(self.candidates)
    
    def probabilityOfWord(self, word):
        """
        Noisy Channel Probability
        """
        return self.likelihoodOfWord() * self.priorOfWord(word)
    
    def wordInDict(self, word_list):
        """
        Remove the words from a list that are not in the Dictionary
        """
        for word in word_list:
            if word in self.dictionary:
                yield word
    
    def splitKgrams(self, word):
        """
        Split the word in kgrams for k=1->len(word)
        """
        return [(word[:i], word[i:]) for i in range(len(self.word))]

    def deleteMethod(self, kgrams):
        """
        Generate all candidates that occur after deleting a character
        """
        return [x + y[1:] for x,y in kgrams if y]
    
    def transposeMethod(self, kgrams):
        """
        Generate all candidates that occur after transposing 2 consequent characters
        """
        return [x + y[1] + y[0] + y[2:] for x, y in kgrams if len(y)>1]
    
    def substituteMethod(self, kgrams, alpha):
        """
        Generate all candidates that occur after replacing a charactor with one from the alphabet set
        """
        return [x + c + y[1:] for x, y in kgrams if y for c in alpha]
    
    def insertMethod(self, kgrams, alpha):
        """
        Generate all candidates that occur after inserting a charactor from the alphabet set
        """
        return [x + c + y for x, y in kgrams for c in alpha]
    
    def get_1editWords(self, word):
        """
        Generate all candidates at edit distance 1
        """
        alpha = 'abcdefghijklmnopqrstuvwxyz'
        edited_words = []
        kgrams = self.splitKgrams(word)
        edited_words.extend(self.deleteMethod(kgrams))
        edited_words.extend(self.transposeMethod(kgrams))
        edited_words.extend(self.substituteMethod(kgrams, alpha))
        edited_words.extend(self.insertMethod(kgrams, alpha))
        return edited_words
    
    def get_2editWords(self):
        """
        Generate all candidates at edit distance 2
        This is done by finding candidates for candidates at edit distance 1
        """
        edit2_candidates = [y for x in self.get_1editWords(self.word) for y in self.get_1editWords(word=x)]
        return list(set(edit2_candidates))
    
    def getCandidates(self):
        """
        Finalize the list of candidates by the decided priority (edit distance 1 > edit distance 2)
        """
        self.candidates = list(self.wordInDict(self.get_1editWords(self.word))) or \
                            list(self.wordInDict(self.get_2editWords())) or [self.word]
    
    def extractWords(self, line):
        """
        Extract all words from the read document
        """
        return re.findall(r'\w+', line)
    
    def extractWordIntoDict(self):
        """
        Create a dictionary with all the terms and their term frequencies
        """
        self.dictionary = Counter(self.extractWords(open('data.txt').read().lower()))
        self.N = sum(self.dictionary.values())
    
    def runSpellCorrector(self):
        """
        Starting point for the spell checker
        Extracts words, generated candidates and returns W number of suggestions
        """
        self.extractWordIntoDict()
        self.getCandidates()
        if len(self.candidates)>self.W:
            self.suggestions = sorted(self.candidates, key=lambda x: self.probabilityOfWord(x), reverse=True)[:self.W]
        else:
            self.suggestions = sorted(self.candidates, key=lambda x: self.probabilityOfWord(x), reverse=True)


if __name__ == "__main__":
    word = input("Enter a mispelled word: ").lower()
    spellChecker = SpellChecker(word)
    spellChecker.runSpellCorrector()
    if word in spellChecker.suggestions:
        print("Best Possible Correct Word: ", word)
        spellChecker.suggestions.remove(word)
    else:
        print("Best Possible Correct Word: ", spellChecker.suggestions.pop(0))
    if spellChecker.suggestions:
        print("Suggested Words: ", end=" ")
        for word in spellChecker.suggestions:
            print(word, end=" ")
    else:
        print("No other suggestions")
    print()
