# WordleSolver

Welcome to **WordleSolver**!

This tool helps you narrow down possible solutions for your daily Wordle puzzle, based on the letters you've already guessed. It's designed to improve your gameplay and reduce frustration, especially when faced with obscure words that seem unfair.

## Features

- **Word List**: Contains all possible valid Wordle words, alphabetized for easy reference.
- **Word Constraints**: Uses the rules of Wordle to filter possible words based on:
  - Correct letters in specific positions
  - Correct letters not in specific positions
  - Letters in the word, but not in certain positions
  - Letters that should not appear in the word at all
- **Possible Words Output**: Displays a list of words that match the current known conditions.

## TODO

- [x] Gather list of all valid Wordle words and alphabetize them - found list here: https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93
- [x] Implement rules to filter based on guessed letters (correct positions, incorrect positions, and excluded letters)
- [x] Output possible word suggestions
- [ ] Improve GUI for better usability and aesthetics

## Motivation

I created this tool because some of the words used in Wordle puzzles, like "aalii", can feel unfair and frustrating. It's easy to feel cheated when you're expected to guess obscure words that don’t seem like common choices. With **WordleSolver**, you can have a clearer path to find words that fit the puzzle while still maintaining a fun challenge.

## Disclaimer

This tool aims to enhance the Wordle experience by suggesting possible words based on your inputs. It doesn’t aim to give you an unfair advantage, just a more informed way to make your guesses.
