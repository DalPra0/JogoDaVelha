import customtkinter as ctk
import tkinter as tk
from random import choice

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Forca")
        self.root.geometry("820x615")

        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.main_frame, text="Jogo da Forca", font=("Arial", 24))
        self.title_label.pack(pady=20)

        self.start_button = ctk.CTkButton(self.main_frame, text="Iniciar", command=self.start_game)
        self.start_button.pack(pady=10)

        self.how_to_play_button = ctk.CTkButton(self.main_frame, text="Como Jogar?", command=self.show_how_to_play)
        self.how_to_play_button.pack(pady=10)

        self.history_button = ctk.CTkButton(self.main_frame, text="Histórico", command=self.show_history)
        self.history_button.pack(pady=10)

        self.settings_button = ctk.CTkButton(self.main_frame, text="Configurações", command=self.show_settings)
        self.settings_button.pack(pady=10)

        self.exit_button = ctk.CTkButton(self.main_frame, text="Sair", command=root.quit)
        self.exit_button.pack(pady=10)

        self.how_to_play_frame = None
        self.history_frame = None
        self.settings_frame = None
        self.game_frame = None

        self.questions = [
            ("Qual é a união de A e B, se A = {1,2} e B = {2,3}?", "1,2,3"),
            ("Qual é a interseção de A e B, se A = {1,2} e B = {2,3}?", "2"),
            ("Se A é subconjunto de B, e B = {1,2,3}, qual poderia ser A?", "1,2"),
        ]
        self.current_question = None
        self.guesses = []

    def start_game(self):
        self.main_frame.pack_forget()
        self.game_frame = ctk.CTkFrame(self.root)
        self.game_frame.pack(fill="both", expand=True)

        self.current_question, self.answer = choice(self.questions)
        self.guesses = ["_"] * len(self.answer)

        self.question_label = ctk.CTkLabel(self.game_frame, text=f"Pergunta: {self.current_question}", font=("Arial", 18))
        self.question_label.pack(pady=10)

        self.guess_label = ctk.CTkLabel(self.game_frame, text=" ".join(self.guesses), font=("Arial", 24))
        self.guess_label.pack(pady=10)

        self.letter_entry = ctk.CTkEntry(self.game_frame, width=200, placeholder_text="Digite uma letra")
        self.letter_entry.pack(pady=10)

        self.submit_button = ctk.CTkButton(self.game_frame, text="Adivinhar", command=self.make_guess)
        self.submit_button.pack(pady=10)

        self.reset_button = ctk.CTkButton(self.game_frame, text="Reiniciar", command=self.reset_game)
        self.reset_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self.game_frame, text="Voltar", command=self.back_to_main_menu)
        self.back_button.pack(pady=10)

    def make_guess(self):
        letter = self.letter_entry.get().strip()
        if len(letter) == 1 and letter in self.answer:
            for i, char in enumerate(self.answer):
                if char == letter:
                    self.guesses[i] = letter
            self.guess_label.configure(text=" ".join(self.guesses))
        self.letter_entry.delete(0, tk.END)

    def reset_game(self):
        self.game_frame.pack_forget()
        self.start_game()

    def back_to_main_menu(self):
        self.game_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

    def show_how_to_play(self):
        pass

    def show_history(self):
        pass

    def show_settings(self):
        pass

root = ctk.CTk()
app = HangmanGame(root)
root.mainloop()
