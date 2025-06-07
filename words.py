import csv 

# Read in the words from the file
def read_words(file_path):
    words = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            words.append(row[0])
    return words

class Wordle:
    def __init__(self, words):
        self.words = words
        self.included_letters = []
        self.excluded_letters = []
        self.included_positions = {}
        self.included_not_positions = {}
        self.initial_words = words.copy()  # Store the initial list of words
        
    def __str__(self):
        return f'Included letters: {self.included_letters}\nExcluded letters: {self.excluded_letters}\nIncluded positions: {self.included_positions}'
   
    def reset(self):
        # Reset the words to the initial list
        self.words = self.initial_words.copy()
        # Clear all rules
        self.included_letters = []
        self.excluded_letters = []
        self.included_positions = {}
        self.included_not_positions = {}
        return self.words
    
    def __update_rules__(self, excluded_letters=None, included_letters=None, included_positions=None, included_not_positions=None):
        
        if excluded_letters:
            for letter in excluded_letters:
                # add it, if not already in the list
                if letter not in self.excluded_letters:
                    self.excluded_letters.append(letter)
                # remove it from the included letters, if there
                if letter in self.included_letters:
                    self.included_letters.remove(letter)

        if included_letters:
            for letter in included_letters:
                #add it, if not already in the list
                if letter not in self.included_letters:
                    self.included_letters.append(letter)
                # remove it from the excluded letters, if there
                if letter in self.excluded_letters:
                    self.excluded_letters.remove(letter)
        
        if included_positions:
            for pos, letter in included_positions.items():
                #add it, if not already in the list
                if pos not in self.included_positions:
                    self.included_positions[pos] = letter
                # remove it from the included not positions, if there
                if pos in self.included_not_positions and self.included_not_positions[pos] == letter:
                    del self.included_not_positions[pos]
        
        if included_not_positions:
            for pos, letter in included_not_positions.items():
                #add it, if not already in the list
                if pos not in self.included_not_positions:
                    self.included_not_positions[pos] = letter
                # remove it from the included positions, if there
                if pos in self.included_positions and self.included_positions[pos] == letter:
                    del self.included_positions[pos]
        return None
    
    # Specify the letters that cannot be used in the word
    def exclude_letters(self, excluded_letters):
        # add the excluded letter(s) to the existing excluded letters IF not already in the list
        self.__update_rules__(excluded_letters=excluded_letters)
        # check that the letter is not in the word
        self.words = [word for word in self.words if not any(letter in word for letter in excluded_letters)]
        return self.words
    
    # Specify the letters that must be used in the word
    def include_letters(self, included_letters):
        # add the included letter(s) to the existing included letters IF not already in the list
        self.__update_rules__(included_letters=included_letters)
        # check that the letter is in the word
        self.words = [word for word in self.words if all(letter in word for letter in included_letters)]
        return self.words
    
    # Specify the letters that must be in certain positions in the word
    def include_letter_position(self, included_positions: dict):
        # add the included letter(s) and positions to rules IF not already in them
        self.__update_rules__(included_letters=list(included_positions.values()))
        self.__update_rules__(included_positions=included_positions)
        # check that the letter is in the specified position
        self.words = [word for word in self.words if all(word[pos] == letter for pos, letter in included_positions.items())]
        return self.words
    
    def include_letter_not_position(self, included_not_positions: dict):
        self.__update_rules__(included_letters=list(included_not_positions.values()))
        self.__update_rules__(included_not_positions=included_not_positions)
        # check that the letter is in the word, but not in the specified position
        self.words = [word for word in self.words if all(word[pos] != letter and letter in word for pos, letter in included_not_positions.items())]
        return self.words


if __name__ == "__main__":
    words = read_words("Wordle_words.txt")
    #words = ['weedy', 'weepy', 'wendy']
    wordle = Wordle(words)
    excluded_letters = ['p','e','a','c','h','i','s','f','l']
    # included_letters = ['e', 'y', 'd']
    letter_positions = {2:'o',3:"u"}
    included_not_positions = {4:'r'}
    wordle.exclude_letters(excluded_letters)
    # wordle.include_letters(ncluded_letters)
    wordle.include_letter_position(letter_positions)
    wordle.include_letter_not_position(included_not_positions)
    print(wordle)  
    print(wordle.words)
