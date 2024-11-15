import customtkinter as ctk

class ForcaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Jogo da Forca")
        self.geometry("800x600")
        self.resizable(False, False)

        self.text_size = 20
        self.fullscreen = False

        self.questions = [
            {"question": "Qual é a interseção dos conjuntos A = {1, 2, 3} e B = {2, 3, 4}?", "answer": ["2", "3"]},
            {"question": "Qual é a união dos conjuntos A = {5, 6} e B = {6, 7}?", "answer": ["5", "6", "7"]},
            {"question": "Qual é a diferença entre os conjuntos A = {1, 2, 3} e B = {3, 4, 5}?", "answer": ["1", "2"]},
            {"question": "Qual é a interseção dos conjuntos A = {a, b, c} e B = {b, c, d}?", "answer": ["b", "c"]},
            {"question": "Qual é a união dos conjuntos A = {x, y} e B = {y, z}?", "answer": ["x", "y", "z"]},
            {"question": "Qual é a diferença simétrica entre os conjuntos A = {1, 2, 3} e B = {2, 3, 4}?", "answer": ["1", "4"]},
            {"question": "Qual é a união dos conjuntos A = {1, 2} e B = {2, 3}?", "answer": ["1", "2", "3"]},
            {"question": "Qual é a interseção dos conjuntos A = {p, q, r} e B = {q, r, s}?", "answer": ["q", "r"]},
            {"question": "Qual é a diferença entre os conjuntos A = {7, 8, 9} e B = {9, 10, 11}?", "answer": ["7", "8"]},
            {"question": "Qual é a união dos conjuntos A = {10, 11, 12} e B = {12, 13, 14}?", "answer": ["10", "11", "12", "13", "14"]},
            {"question": "Qual é a interseção dos conjuntos A = {a, b, c, d} e B = {c, d, e, f}?", "answer": ["c", "d"]},
            {"question": "Qual é a diferença simétrica entre os conjuntos A = {1, 2, 3, 4} e B = {3, 4, 5, 6}?", "answer": ["1", "2", "5", "6"]},
            {"question": "Qual é a união dos conjuntos A = {a, b, c} e B = {b, c, d, e}?", "answer": ["a", "b", "c", "d", "e"]},
            {"question": "Qual é a interseção dos conjuntos A = {m, n, o} e B = {o, p, q}?", "answer": ["o"]},
            {"question": "Qual é a diferença entre os conjuntos A = {1, 2, 3} e B = {1, 3, 5}?", "answer": ["2"]},
            {"question": "Qual é a diferença simétrica entre os conjuntos A = {1, 2, 3} e B = {2, 3, 4}?", "answer": ["1", "4"]}
        ]

        self.current_question_index = 0
        self.correct_answers = []
        self.incorrect_guesses = []
        self.hangman_parts = 0

        self.frames = {}
        self.create_frames()
        self.show_frame("Inicio")

    def create_frames(self):
        for F in (Inicio, ComoJogar, Jogo, Configuracoes, ProximaPergunta):
            frame = F(self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def reset_game(self):
        self.correct_answers = []
        self.incorrect_guesses = []
        self.hangman_parts = 0
        self.current_question_index = 0
        self.frames["Jogo"].update_question()
        self.frames["Jogo"].reset_hangman()

    def next_question_or_end(self):
        if self.current_question_index + 1 < len(self.questions):
            self.current_question_index += 1
            self.frames["Jogo"].update_question()
            self.frames["Jogo"].reset_hangman()
            self.show_frame("Jogo")
        else:
            self.show_frame("Historico")

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)


class Inicio(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Jogo da Forca", font=("Arial", 30)).pack(pady=20)
        ctk.CTkButton(self, text="Iniciar", command=lambda: parent.show_frame("Jogo")).pack(pady=10)
        ctk.CTkButton(self, text="Como Jogar?", command=lambda: parent.show_frame("ComoJogar")).pack(pady=10)
        ctk.CTkButton(self, text="Configurações", command=lambda: parent.show_frame("Configuracoes")).pack(pady=10)
        ctk.CTkButton(self, text="Sair", command=parent.quit).pack(pady=10)


class ComoJogar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Como Jogar", font=("Arial", 30)).pack(pady=20)
        ctk.CTkLabel(self, text=( 
            "O jogo consiste em responder perguntas sobre conjuntos.\n"
            "Você pode tentar chutar as respostas, e erros adicionam partes ao boneco na forca.\n"
            "Respostas parcialmente corretas são aceitas."
        ), wraplength=700, justify="left").pack(pady=20)
        ctk.CTkButton(self, text="Voltar", command=lambda: parent.show_frame("Inicio")).pack(pady=10)


class Jogo(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.question_label = ctk.CTkLabel(self, text="", font=("Arial", 20), wraplength=700, justify="center")
        self.question_label.pack(pady=20)

        self.guess_entry = ctk.CTkEntry(self, placeholder_text="Digite seu chute aqui")
        self.guess_entry.pack(pady=10)

        self.submit_button = ctk.CTkButton(self, text="Enviar Chute", command=self.submit_guess)
        self.submit_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self, text="Voltar", command=lambda: parent.show_frame("Inicio"))
        self.back_button.pack(pady=10)

        self.canvas = ctk.CTkCanvas(self, width=300, height=400, bg="white")
        self.canvas.pack(pady=10)
        self.draw_gallows()

        self.correct_label = ctk.CTkLabel(self, text="Respostas corretas: []", wraplength=700, justify="left")
        self.correct_label.pack(pady=10)

        self.incorrect_label = ctk.CTkLabel(self, text="Respostas erradas: []", wraplength=700, justify="left")
        self.incorrect_label.pack(pady=10)

        self.update_question()

    def update_question(self):
        question = self.parent.questions[self.parent.current_question_index]["question"]
        self.question_label.configure(text=f"Pergunta: {question}")

    def submit_guess(self):
        guess = self.guess_entry.get().strip()
        self.guess_entry.delete(0, ctk.END)

        if not guess:
            return

        question = self.parent.questions[self.parent.current_question_index]
        if guess in question["answer"]:
            if guess not in self.parent.correct_answers:
                self.parent.correct_answers.append(guess)
            self.correct_label.configure(text=f"Respostas corretas: {self.parent.correct_answers}")
        else:
            if guess not in self.parent.incorrect_guesses:
                self.parent.incorrect_guesses.append(guess)
                self.parent.hangman_parts += 1
                self.draw_hangman()
            self.incorrect_label.configure(text=f"Respostas erradas: {self.parent.incorrect_guesses}")

        if len(self.parent.correct_answers) == len(question["answer"]):
            self.parent.show_frame("ProximaPergunta")
        elif self.parent.hangman_parts >= 6:
            self.parent.show_frame("ProximaPergunta")

    def draw_gallows(self):
        self.canvas.create_line(50, 350, 250, 350, width=2)
        self.canvas.create_line(150, 350, 150, 50, width=2)
        self.canvas.create_line(150, 50, 250, 50, width=2)
        self.canvas.create_line(250, 50, 250, 100, width=2)

    def draw_hangman(self):
        parts = [
            lambda: self.canvas.create_oval(230, 100, 270, 140, width=2),  # Cabeça
            lambda: self.canvas.create_line(250, 140, 250, 240, width=2),  # Corpo
            lambda: self.canvas.create_line(250, 160, 230, 200, width=2),  # Braço esquerdo
            lambda: self.canvas.create_line(250, 160, 270, 200, width=2),  # Braço direito
            lambda: self.canvas.create_line(250, 240, 230, 280, width=2),  # Perna esquerda
            lambda: self.canvas.create_line(250, 240, 270, 280, width=2),  # Perna direita
        ]
        if self.parent.hangman_parts <= len(parts):
            parts[self.parent.hangman_parts - 1]()

    def reset_hangman(self):
        self.canvas.delete("all")
        self.draw_gallows()


class ProximaPergunta(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Pergunta Finalizada!", font=("Arial", 30)).pack(pady=20)
        ctk.CTkButton(self, text="Próxima Pergunta", command=parent.next_question_or_end).pack(pady=10)


class Configuracoes(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Configurações", font=("Arial", 30)).pack(pady=20)
        ctk.CTkButton(self, text="Modo de Tela Cheia", command=parent.toggle_fullscreen).pack(pady=10)
        ctk.CTkButton(self, text="Voltar", command=lambda: parent.show_frame("Inicio")).pack(pady=10)


if __name__ == "__main__":
    app = ForcaApp()
    app.mainloop()
