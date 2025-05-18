import tkinter as tk
from tkinter import ttk
import random
import pandas as pd

def load_questions(filepath="data/questions.csv"):
    try:
        df = pd.read_csv(filepath)
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Failed to load questions: {e}")
        return []

def predict_difficulty(score, total_asked):
    if total_asked == 0:
        return 'easy'
    acc = score / total_asked
    if acc > 0.8: return 'hard'
    if acc > 0.5: return 'medium'
    return 'easy'

class QuizGUI:
    def __init__(self, master):
        self.master = master
        master.title("🎨 Quiz Game")

        master.geometry("600x520")
        master.configure(bg="#f8f9fa")  # Light pastel background

        self.questions = load_questions()
        self.score = 0
        self.total = 5
        self.asked = 0
        self.current_q = None

        self.title = tk.Label(master, text="🎯 Quiz Game 🎯", font=("Comic Sans MS", 22, "bold"),
                              fg="#2c3e50", bg="#f8f9fa")
        self.title.pack(pady=10)

        self.question_label = tk.Label(master, text="", wraplength=550, font=("Arial", 16, "bold"),
                                       fg="#2c3e50", bg="#f8f9fa")
        self.question_label.pack(pady=5)

        self.var = tk.IntVar()
        self.options = []
        self.option_colors = ["#f8d7da", "#d4edda", "#fff3cd", "#d1ecf1"]
        for i in range(4):
            rb = tk.Radiobutton(master, text="", variable=self.var, value=i+1,
                                font=("Arial", 14), fg="#2c3e50", bg=self.option_colors[i],
                                selectcolor="#b2dfdb", activebackground="#aed6f1",
                                width=50, anchor='w', padx=10, pady=6, relief='raised', bd=2)
            rb.pack(pady=5)
            rb.bind("<Enter>", lambda e, b=rb: b.config(bg="#e0f7fa"))
            rb.bind("<Leave>", lambda e, b=rb, col=self.option_colors[i]: b.config(bg=col))
            self.options.append(rb)

        self.result_label = tk.Label(master, text="", font=("Arial", 14), bg="#f8f9fa")
        self.result_label.pack(pady=5)

        self.button_frame = tk.Frame(master, bg="#f8f9fa")
        self.button_frame.pack(pady=10)

        self.submit_btn = tk.Button(self.button_frame, text="Submit Answer", command=self.submit_answer,
                                    font=("Arial", 13, "bold"), bg="#28a745", fg="white",
                                    activebackground="#218838", width=15)
        self.submit_btn.grid(row=0, column=0, padx=10)

        self.next_btn = tk.Button(self.button_frame, text="Next", command=self.next_question,
                                  font=("Arial", 13, "bold"), bg="#007bff", fg="white",
                                  activebackground="#0056b3", width=15)
        self.next_btn.grid(row=0, column=1, padx=10)
        self.next_btn.grid_remove()

        self.progress = ttk.Progressbar(master, orient='horizontal', length=550,
                                        mode='determinate', maximum=self.total)
        self.progress.pack(pady=10)

        self.next_question()

    def next_question(self):
        self.next_btn.grid_remove()
        self.submit_btn.grid()
        if self.asked >= self.total:
            self.show_final_score()
            return
        difficulty = predict_difficulty(self.score, self.asked)
        pool = [q for q in self.questions if q['difficulty'] == difficulty]
        if not pool:
            pool = self.questions
        self.current_q = random.choice(pool)
        self.questions.remove(self.current_q)

        self.question_label.config(
            text=f"Q{self.asked+1}: {self.current_q['question']} (Difficulty: {difficulty})")
        for i, opt in enumerate(['option1','option2','option3','option4']):
            self.options[i].config(text=self.current_q[opt], state='normal', bg=self.option_colors[i])
        self.var.set(0)
        self.result_label.config(text="")
        self.progress['value'] = self.asked

    def submit_answer(self):
        selected = self.var.get()
        if selected == 0:
            self.result_label.config(text="⚠️ Please select an answer before submitting.", fg="#c0392b")
            return
        self.submit_btn.grid_remove()
        self.next_btn.grid()

        correct = selected == self.current_q['answer']
        if correct:
            self.score += 1
            self.result_label.config(text="✅ Correct! 🎉", fg="#2e7d32")
            self.options[selected-1].config(bg="#abebc6")
        else:
            correct_idx = self.current_q['answer'] - 1
            correct_option_text = self.current_q[f"option{self.current_q['answer']}"]
            self.result_label.config(
                text=f"❌ Wrong! Correct answer: {correct_option_text}", fg="#c0392b"
            )
            self.options[selected-1].config(bg="#f5b7b1")
            self.options[correct_idx].config(bg="#abebc6")
        for opt in self.options:
            opt.config(state='disabled')

        self.asked += 1

    def show_final_score(self):
        self.submit_btn.grid_remove()
        self.next_btn.grid_remove()
        self.question_label.config(
            text=f"🏆 Quiz Completed! Your score: {self.score} / {self.total} 🏆", fg="#34495e")
        for opt in self.options:
            opt.pack_forget()
        self.result_label.pack_forget()
        self.progress.pack_forget()
    
    def show_final_score(self):
        self.submit_btn.grid_remove()
        self.next_btn.grid_remove()
        self.question_label.config(
            text=f"🏆 Quiz Completed! Your score: {self.score} / {self.total} 🏆", fg="#34495e")

        for opt in self.options:
            opt.pack_forget()

        self.result_label.pack_forget()
        self.progress.pack_forget()

        self.restart_btn = tk.Button(self.master, text="🔄 Restart Quiz", command=self.restart_quiz,
                                     font=("Arial", 14, "bold"), bg="#ffc107", fg="#212529",
                                     activebackground="#ffca28", relief='raised', bd=4)
        self.restart_btn.pack(pady=20)

    def restart_quiz(self):
        self.score = 0
        self.asked = 0
        self.questions = load_questions()

        # Reset UI
        self.restart_btn.pack_forget()
        for opt in self.options:
            opt.pack(pady=5)
            opt.config(state='normal')

        self.result_label.pack(pady=5)
        self.progress.pack(pady=10)

        self.next_question()

if __name__ == "__main__":
    root = tk.Tk()
    QuizGUI(root)
    root.mainloop()
