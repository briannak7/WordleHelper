import tkinter as tk
from tkinter import messagebox
from words import Wordle, read_words

# Assuming you have the words in a file
WORDS = "Wordle_words.txt"
words = read_words(WORDS)
wordle = Wordle(words)

# GUI using Tkinter
class WordleGUI:
    def __init__(self, root, wordle):
        self.wordle = wordle
        self.root = root
        self.root.title("Wordle Helper")
        self.root.geometry("700x500")  # Increased window size
        
        # Display for filtered words
        self.words_label = tk.Label(root, text="Possible Words: ", font=("Helvetica", 12))
        self.words_label.pack(pady=10)

        self.words_text = tk.Text(root, height=10, width=50)
        self.words_text.pack(pady=5)

        # Section to show included and excluded letters and positions
        self.info_frame = tk.Frame(root)
        self.info_frame.pack(pady=10)

        self.included_letters_label = tk.Label(self.info_frame, text="Included Letters: ", font=("Helvetica", 10))
        self.included_letters_label.grid(row=0, column=0, padx=5, sticky="w")
        self.included_letters_display = tk.Label(self.info_frame, text="None", font=("Helvetica", 10))
        self.included_letters_display.grid(row=0, column=1)

        self.excluded_letters_label = tk.Label(self.info_frame, text="Excluded Letters: ", font=("Helvetica", 10))
        self.excluded_letters_label.grid(row=1, column=0, padx=5, sticky="w")
        self.excluded_letters_display = tk.Label(self.info_frame, text="None", font=("Helvetica", 10))
        self.excluded_letters_display.grid(row=1, column=1)

        self.included_positions_label = tk.Label(self.info_frame, text="Included Positions: ", font=("Helvetica", 10))
        self.included_positions_label.grid(row=2, column=0, padx=5, sticky="w")
        self.included_positions_display = tk.Label(self.info_frame, text="None", font=("Helvetica", 10))
        self.included_positions_display.grid(row=2, column=1)

        self.included_not_positions_label = tk.Label(self.info_frame, text="Excluded Positions: ", font=("Helvetica", 10))
        self.included_not_positions_label.grid(row=3, column=0, padx=5, sticky="w")
        self.included_not_positions_display = tk.Label(self.info_frame, text="None", font=("Helvetica", 10))
        self.included_not_positions_display.grid(row=3, column=1)

        # Labels for the input fields
        self.create_label_and_entry(root, "Excluded Letters (comma separated)", 0)
        self.create_label_and_entry(root, "Included Letters (comma separated)", 1)
        self.create_label_and_entry(root, "Included Positions (e.g. 0:w, 1:e)", 2)
        self.create_label_and_entry(root, "Excluded Positions (e.g. 0:w, 2:r)", 3)

        # Apply Filter Button
        self.apply_button = tk.Button(root, text="Apply Filters", command=self.apply_filters)
        self.apply_button.pack(pady=10)

        # Reset Button
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_filters)
        self.reset_button.pack(pady=5)

    def create_label_and_entry(self, root, label_text, row):
        label = tk.Label(root, text=label_text, font=("Helvetica", 10))
        label.pack(pady=5, anchor="w")

        entry = tk.Entry(root, width=50)
        entry.pack(pady=5)
        entry.insert(0, "")  # Blank placeholder text
        setattr(self, f"entry_{row}", entry)  # Store the entry widget for later use

    def apply_filters(self):
        # Get the inputs
        excluded_letters = self.entry_0.get().split(",")
        excluded_letters = [letter.strip() for letter in excluded_letters]

        included_letters = self.entry_1.get().split(",")
        included_letters = [letter.strip() for letter in included_letters]

        included_positions = self.parse_positions(self.entry_2.get())
        included_not_positions = self.parse_positions(self.entry_3.get())

        # Apply the filters
        self.wordle.exclude_letters(excluded_letters)
        self.wordle.include_letters(included_letters)
        self.wordle.include_letter_position(included_positions)
        self.wordle.include_letter_not_position(included_not_positions)

        # Update the displayed words
        self.update_words_text()
        # Update the info display
        self.update_info_display()

    def reset_filters(self):
        # Reset the wordle object and GUI inputs
        self.wordle.reset()
        self.entry_0.delete(0, tk.END)
        self.entry_1.delete(0, tk.END)
        self.entry_2.delete(0, tk.END)
        self.entry_3.delete(0, tk.END)
        self.update_words_text()
        # Reset the info display
        self.update_info_display()

    def update_words_text(self):
        # Display the possible words in the text box
        self.words_text.delete(1.0, tk.END)
        for word in self.wordle.words:
            self.words_text.insert(tk.END, word + "\n")

    def update_info_display(self):
        # Update the info labels with the current values
        self.included_letters_display.config(text=", ".join(self.wordle.included_letters) if self.wordle.included_letters else "None")
        self.excluded_letters_display.config(text=", ".join(self.wordle.excluded_letters) if self.wordle.excluded_letters else "None")
        self.included_positions_display.config(text=", ".join([f"{pos}:{letter}" for pos, letter in self.wordle.included_positions.items()]) if self.wordle.included_positions else "None")
        self.included_not_positions_display.config(text=", ".join([f"{pos}:{letter}" for pos, letter in self.wordle.included_not_positions.items()]) if self.wordle.included_not_positions else "None")

    def parse_positions(self, position_string):
        # Parse the positions input, e.g. "0:w, 1:e" to a dictionary
        positions = {}
        if position_string:
            for pair in position_string.split(","):
                pos, letter = pair.split(":")
                positions[int(pos)] = letter.strip()
        return positions


if __name__ == "__main__":
    root = tk.Tk()
    gui = WordleGUI(root, wordle)
    root.mainloop()
