import tkinter as tk
from tkinter import messagebox
from words import Wordle, read_words

# Load words from file
WORDS = "Wordle_words.txt"
words = read_words(WORDS)
print(f"Loaded {len(words)} words")  # Debug info
wordle = Wordle(words)

class WordleGUI:
    def __init__(self, root, wordle):
        self.wordle = wordle
        self.root = root
        self.root.title("Wordle Helper")
        self.root.geometry("700x550")

        # Display for filtered words
        self.words_label = tk.Label(root, text="Possible Words: ", font=("Helvetica", 12))
        self.words_label.pack(pady=10)

        self.words_text = tk.Text(root, height=10, width=50)
        self.words_text.pack(pady=5)

        # Info display
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

        # Input fields
        self.create_label_and_entry(root, "Excluded Letters (comma separated)", 0)
        self.create_label_and_entry(root, "Included Letters (comma separated)", 1)
        self.create_label_and_entry(root, "Included Positions (e.g. 0:w, 1:e)", 2)
        self.create_label_and_entry(root, "Excluded Positions (e.g. 0:w, 2:r)", 3)

        # Buttons
        self.apply_button = tk.Button(root, text="Apply Filters", command=self.apply_filters)
        self.apply_button.pack(pady=10)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_filters)
        self.reset_button.pack(pady=5)

        # Initial word display
        self.update_words_text()

    def create_label_and_entry(self, root, label_text, row):
        label = tk.Label(root, text=label_text, font=("Helvetica", 10))
        label.pack(pady=5, anchor="w")

        entry = tk.Entry(root, width=50)
        entry.pack(pady=5)
        setattr(self, f"entry_{row}", entry)

    def apply_filters(self):
        self.wordle.reset()  # Start from full list on each apply

        # Gather and sanitize inputs
        excluded_letters = [l.strip() for l in self.entry_0.get().split(",") if l.strip()]
        included_letters = [l.strip() for l in self.entry_1.get().split(",") if l.strip()]
        included_positions = self.parse_positions(self.entry_2.get(), allow_multiple=False)
        included_not_positions = self.parse_positions(self.entry_3.get(), allow_multiple=True)


        # Apply filters only if input exists
        if excluded_letters:
            self.wordle.exclude_letters(excluded_letters)
        if included_letters:
            self.wordle.include_letters(included_letters)
        if included_positions:
            self.wordle.include_letter_position(included_positions)
        if included_not_positions:
            self.wordle.include_letter_not_position(included_not_positions)

        # Update display
        self.update_words_text()
        self.update_info_display()

    def reset_filters(self):
        self.wordle.reset()
        for i in range(4):
            getattr(self, f"entry_{i}").delete(0, tk.END)
        self.update_words_text()
        self.update_info_display()

    def update_words_text(self):
        self.words_text.delete(1.0, tk.END)
        if not self.wordle.words:
            self.words_text.insert(tk.END, "No words match your filters.")
        else:
            for word in self.wordle.words:
                self.words_text.insert(tk.END, word + "\n")

    def update_info_display(self):
        self.included_letters_display.config(
            text=", ".join(self.wordle.included_letters) if self.wordle.included_letters else "None")
        self.excluded_letters_display.config(
            text=", ".join(self.wordle.excluded_letters) if self.wordle.excluded_letters else "None")
        self.included_positions_display.config(
            text=", ".join(f"{k}:{v}" for k, v in self.wordle.included_positions.items()) if self.wordle.included_positions else "None")
        self.included_not_positions_display.config(
            text=", ".join(f"{k}:{v}" for k, v in self.wordle.included_not_positions.items()) if self.wordle.included_not_positions else "None")

    def parse_positions(self, position_string, allow_multiple=False):
        positions = {}
        if position_string:
            for pair in position_string.split(","):
                if ":" in pair:
                    pos, letter = pair.split(":")
                    pos = int(pos.strip())
                    letter = letter.strip()
                    # Always assign single letters, no sets
                    positions[pos] = letter
        return positions




if __name__ == "__main__":
    root = tk.Tk()
    gui = WordleGUI(root, wordle)
    root.mainloop()
