import os
import pickle
import sys
import time
import threading
from os import system
class StickyNotesApp:
    def __init__(self):
        self.notes_file = "sticky_notes.pkl"
        self.notes = self.load_notes()
        self.max_line_length = 80  # Maximum line length for side-by-side notes
        self.choice_lock = threading.Lock()
        self.choice = None
        system("title " + f"stkii v1.0 by Typhoonz0 on Github")
        self.format_text = {"--red": "\033[91m",
                            "--yellow": "\033[93m",
                            "--green": "\033[92m",
                            "--blue": "\033[94m",
                            "--purple": "\033[95m",
                            "--bold": "\033[1m",
                            "--reset": "\033[0m"}

    def load_notes(self):
        if os.path.exists(self.notes_file):
            with open(self.notes_file, 'rb') as file:
                return pickle.load(file)
        return []

    def save_notes(self):
        with open(self.notes_file, 'wb') as file:
            pickle.dump(self.notes, file)

    def add_note(self):
        print("Creating a new note. Type '--add' to save and add the note.")
        print("Type '--del' to delete the last line, '--delall' to delete the note altogether.")
        print("Press ENTER to continue.")
        system("pause>nul")
        note_lines = []
        while True:
            self.clear_screen()
            self.view_notes_inediting()
            print("New note starts here:")
            self.print_note_box(note_lines)
            line = input("> ")
            if line == "--add":
                self.notes.append("\n".join(note_lines))
                self.notes.append("\033[0m")
                self.save_notes()
                print("Note added!")
                break
            elif line == "--del":
                if note_lines:
                    note_lines.pop()
                    print("Deleted last line.")
                else:
                    print("No lines to delete.")
            elif line == "--delall":
                note_lines.clear()
                print("Note cleared.")
            elif line in self.format_text:
                note_lines.append(self.format_text[line])
            else:
                note_lines.append(line)

    def print_note_box(self, lines, max_width=None):
        if not lines:
            return

        if max_width is None:
            max_width = max(len(line) for line in lines) + 2
        box = []
        box.append("+" + "-" * max_width + "+")
        for line in lines:
            if line in self.format_text.values():
                box.append(line)
            else:
                box.append(f"| {line.ljust(max_width - 2)} |")
        box.append("+" + "-" * max_width + "+")
        for line in box:
            print(line)

    def view_notes(self, show_numbers=False):
        self.clear_screen()
        if not self.notes:
            print("No notes found.")
        else:
            all_boxes = []
            max_width = max(len(line) for note in self.notes for line in note.split("\n")) + 2
            for idx, note in enumerate(self.notes, 1):
                box = self.print_note_box(note.split("\n"), max_width)
                if show_numbers:
                    print(f"Note {idx}:")
                all_boxes.append(box)
            input("Press ENTER to continue.")
    
    def view_notes_inediting(self, show_numbers=False):
        if not self.notes:
            print("No notes found.")
        else:
            print("Sticky Notes:")
            all_boxes = []
            max_width = max(len(line) for note in self.notes for line in note.split("\n")) + 2
            for idx, note in enumerate(self.notes, 1):
                box = self.print_note_box(note.split("\n"), max_width)
                if show_numbers:
                    print(f"Note {idx}:")
                all_boxes.append(box)

    def delete_note_by_index(self, index):
        if 0 <= index < len(self.notes):
            self.notes.pop(index)
            self.save_notes()
            print("Note deleted!")
        else:
            print("Invalid note number.")

    def delete_note(self):
        self.view_notes(show_numbers=True)
        try:
            note_index = int(input("Enter the number of the note to delete: "))
            if 1 <= note_index <= len(self.notes):
                self.delete_note_by_index(note_index - 1)
            else:
                print("Invalid note number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def delete_all_notes(self):
        confirm = input("Are you sure you want to delete all notes? (yes/no): ")
        if confirm.lower() == 'yes':
            self.notes.clear()
            self.save_notes()
            print("All notes deleted!")
        else:
            print("Deletion cancelled.")

    def edit_note_by_index(self, index):
        if 0 <= index < len(self.notes):
            note_lines = self.notes[index].split("\n")
            print("Editing note. Type '--add' to save changes.")
            print("Type '--del' to delete the last line, '--delall' to delete the note altogether.")
            print("Press ENTER to continue.")
            system("pause>nul")
            while True:
                self.clear_screen()
                self.view_notes_inediting()
                self.print_note_box(note_lines)
                line = input("Enter a line (or '--add' to save changes): ")
                if line == "--add":
                    self.notes[index] = "\n".join(note_lines)
                    self.save_notes()
                    print("Note edited!")
                    break
                elif line == "--del":
                    if note_lines:
                        note_lines.pop()
                        print("Deleted last line.")
                    else:
                        print("No lines to delete.")
                elif line == "--delall":
                    note_lines.clear()
                    print("Note cleared.")
                elif line in self.format_text:
                    note_lines.append(self.format_text[line])
                else:
                    note_lines.append(line)
        else:
            print("Invalid note number.")

    def edit_note(self):
        self.view_notes(show_numbers=True)
        try:
            note_index = int(input("Enter the number of the note to edit: "))
            if 1 <= note_index <= len(self.notes):
                self.edit_note_by_index(note_index - 1)
            else:
                print("Invalid note number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def get_user_choice(self):
        while True:
            choice = input("choice > ")
            if choice in ["1", "2", "3", "4", "5", "6"]:
                with self.choice_lock:
                    self.choice = choice
                break
            else:
                print("Invalid choice. Please try again.")

    def run(self):
        while True:
            self.clear_screen()
            print("""\033[1;34m
   ▄████████     ███        ▄█   ▄█▄  ▄█   ▄█ 
  ███    ███ ▀█████████▄   ███ ▄███▀ ███  ███ 
  ███    █▀     ▀███▀▀██   ███▐██▀   ███▌ ███▌
  ███            ███   ▀  ▄█████▀    ███▌ ███▌
▀███████████     ███     ▀▀█████▄    ███▌ ███▌
         ███     ███       ███▐██▄   ███  ███ 
   ▄█    ███     ███       ███ ▀███▄ ███  ███ 
 ▄████████▀     ▄████▀     ███   ▀█▀ █▀   █▀  
                           ▀                  
                  1 - add note
                  2 - view note
                  3 - delete note
                  4 - delete all notes
                  5 - edit note
                  6 - exit  \033[0m""")
            choice = input("choice > ")

            if choice == "1":
                self.add_note()
            elif choice == "2":
                self.view_notes()
            elif choice == "3":
                self.delete_note()
            elif choice == "4":
                self.delete_all_notes()
            elif choice == "5":
                self.edit_note()
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please try again.")

    def clear_screen(self):
        if sys.platform.startswith('win'):
            os.system('cls')
        else:
            os.system('clear')

if __name__ == "__main__":

    app = StickyNotesApp()
    app.run()

