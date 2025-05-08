import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import json
import xml.etree.ElementTree as ET

class QuizSlideCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Slide")
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(True, True)

        self.quiz_data = []

        # Create question entry
        self.question_label = tk.Label(root, text="Enter Quiz Question:")
        self.question_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.question_entry = tk.Entry(root, width=50)
        self.question_entry.grid(row=0, column=1, padx=10, pady=5)

        # Question Type Dropdown
        self.question_type_label = tk.Label(root, text="Select Question Type:")
        self.question_type_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.question_type_var = tk.StringVar(value="multiple_choice")
        self.question_type_menu = tk.OptionMenu(root, self.question_type_var, "multiple_choice", "true_false", "fill_in_the_blank", command=self.update_ui_for_question_type)
        self.question_type_menu.grid(row=1, column=1, padx=10, pady=5)

        # Difficulty Level Dropdown
        self.difficulty_level_label = tk.Label(root, text="Select Difficulty Level:")
        self.difficulty_level_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.difficulty_level_var = tk.StringVar(value="Easy")
        self.difficulty_level_menu = tk.OptionMenu(root, self.difficulty_level_var, "Easy", "Medium", "Hard")
        self.difficulty_level_menu.grid(row=2, column=1, padx=10, pady=5)

        # Create options entry (only for multiple choice and true/false)
        self.options_label = tk.Label(root, text="Enter Options (Separate by commas):")
        self.options_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.options_entry = tk.Entry(root, width=50)
        self.options_entry.grid(row=3, column=1, padx=10, pady=5)

        # Create correct answers checkboxes (only for multiple choice or true/false)
        self.correct_answers_label = tk.Label(root, text="Select Correct Answers:")
        self.correct_answers_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.correct_answers_var = []
        self.checkbuttons = []
        for i in range(4):  # For up to 4 options (A, B, C, D)
            var = tk.BooleanVar()
            self.correct_answers_var.append(var)
            checkbutton = tk.Checkbutton(root, text=f"Option {chr(65 + i)}", variable=var)
            self.checkbuttons.append(checkbutton)

        # Position checkboxes for options A, B, C, D in the grid
        row = 5
        col = 0
        for i, checkbutton in enumerate(self.checkbuttons):
            checkbutton.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            col += 1
            if col > 1:  # Move to the next row after two options per row
                col = 0
                row += 1

        # Add input fields for fill-in-the-blank type (hidden by default)
        self.blank_answer_label = tk.Label(root, text="Enter the Correct Answer for Fill-in-the-Blank Question:")
        self.blank_answer_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.blank_answer_entry = tk.Entry(root, width=50)
        self.blank_answer_entry.grid(row=6, column=1, padx=10, pady=5)

        # Preview Section for Question
        self.preview_label = tk.Label(root, text="Preview Question:")
        self.preview_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.preview_text = tk.Label(root, text="", width=50, height=3, relief="solid", anchor="w", justify="left")
        self.preview_text.grid(row=7, column=1, padx=10, pady=5)

        # Button to add quiz
        self.add_quiz_button = tk.Button(root, text="Add Quiz", command=self.add_quiz_slide)
        self.add_quiz_button.grid(row=8, columnspan=2, padx=10, pady=10)

        # Input field for URL (save directory selection)
        self.url_label = tk.Label(root, text="Save Directory:")
        self.url_label.grid(row=10, column=0, padx=10, pady=5, sticky="w")
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.grid(row=10, column=1, padx=10, pady=5)
        
        # Button to generate HTML file
        self.generate_html_button = tk.Button(root, text="Generate HTML", command=self.generate_html)
        self.generate_html_button.grid(row=9, column=0, padx=10, pady=10)



        # Button to export quizzes as JSON or XML
        self.export_button = tk.Button(root, text="Export Quizzes", command=self.export_quizzes)
        self.export_button.grid(row=11, column=1, padx=10, pady=10)

        # Button to clear all fields
        self.clear_button = tk.Button(root, text="Clear All", command=self.reset_fields)
        self.clear_button.grid(row=12, columnspan=2, padx=10, pady=10)

        # Button to upload quizzes from CSV file
        self.upload_button = tk.Button(root, text="Upload Quizzes from CSV", command=self.upload_quizzes_from_csv)
        self.upload_button.grid(row=13, columnspan=2, padx=10, pady=10)

        # Update UI based on question type
        self.update_ui_for_question_type(self.question_type_var.get())


    def update_ui_for_question_type(self, question_type):
        # Hide or show fields based on selected question type
        if question_type == "fill_in_the_blank":
            self.blank_answer_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
            self.blank_answer_entry.grid(row=6, column=1, padx=10, pady=5)
            for cb in self.checkbuttons:
                cb.grid_forget()  # Hide checkboxes for this question type
            self.preview_text.config(text=f"Fill in the blank: {self.question_entry.get()}")
        else:
            self.blank_answer_label.grid_forget()
            self.blank_answer_entry.grid_forget()
            row = 5
            col = 0
            for i, cb in enumerate(self.checkbuttons):
                cb.grid(row=row, column=col, padx=10, pady=5, sticky="w")
                col += 1
                if col > 1:  # Move to the next row after two options per row
                    col = 0
                    row += 1
            self.preview_text.config(text=f"Multiple choice: {self.question_entry.get()}")

    def add_quiz_slide(self):
        question = self.question_entry.get().strip()
        options = [option.strip() for option in self.options_entry.get().split(',')]
        correct_answers = [i for i, var in enumerate(self.correct_answers_var) if var.get()]
        question_type = self.question_type_var.get()
        difficulty_level = self.difficulty_level_var.get()

        if not question:
            messagebox.showerror("Invalid Input", "Please enter a quiz question.")
            return

        if question_type != "fill_in_the_blank" and (not options or len(options) < 2):
            messagebox.showerror("Invalid Input", "Please enter at least two options for multiple choice questions.")
            return

        if question_type == "fill_in_the_blank":
            correct_answer = self.blank_answer_entry.get().strip()
            if not correct_answer:
                messagebox.showerror("Invalid Input", "Please enter the correct answer for the fill-in-the-blank question.")
                return
            self.quiz_data.append({
                "question": question,
                "options": None,
                "correct_answer": correct_answer,
                "question_type": question_type,
                "difficulty_level": difficulty_level
            })
        else:
            if not correct_answers:
                messagebox.showerror("Invalid Input", "Please select at least one correct answer.")
                return

            self.quiz_data.append({
                "question": question,
                "options": options,
                "correct_answers": correct_answers,
                "question_type": question_type,
                "difficulty_level": difficulty_level
            })

        messagebox.showinfo("Quiz Added", "The quiz slide has been added.")
        self.reset_fields()

    def reset_fields(self):
        self.question_entry.delete(0, tk.END)
        self.options_entry.delete(0, tk.END)
        for var in self.correct_answers_var:
            var.set(False)
        self.preview_text.config(text="")

    def create_html(self):
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Quiz Page</title>
            <script>
                let quizData = [];
            </script>
        </head>
        <body>
            <h1>Quiz</h1>
        """

        if not self.quiz_data:
            print("No quiz data to generate HTML!")

        for quiz_item in self.quiz_data:
            question = quiz_item['question']
            html_content += f"<h2>{question}</h2>\n"

            if quiz_item["question_type"] == "fill_in_the_blank":
                html_content += f"""
                    <label for="answer_{question}">Your Answer:</label>
                    <input type="text" id="answer_{question}" name="answer_{question}">
                """
            else:
                for idx, option in enumerate(quiz_item["options"]):
                    html_content += f"""
                    <input type="radio" name="answer_{question}" value="{option}" id="option_{idx}">
                    <label for="option_{idx}">{option}</label><br>
                    """

            html_content += f"""
                <script>
                    let quizItem = {{
                        "question": "{question}",
                        "type": "{quiz_item['question_type']}",
            """

            if quiz_item["question_type"] == "fill_in_the_blank":
                html_content += f"""
                        "correctAnswer": "{quiz_item['correct_answer']}",
                """
            else:
                html_content += f"""
                        "options": {quiz_item['options']},
                        "correctAnswers": {quiz_item['correct_answers']},
                """

            html_content += f"""
                        "difficultyLevel": "{quiz_item['difficulty_level']}",
                    }};
                    quizData.push(quizItem);
                </script>
            """

        html_content += """
            <script>
                function checkQuiz() {
                    let score = 0;
                    for (let i = 0; i < quizData.length; i++) {
                        let question = quizData[i];
                        let userAnswer = null;
                        if (question.type === "fill_in_the_blank") {
                            userAnswer = document.getElementById(`answer_${question.question}`).value;
                        } else {
                            let radioButtons = document.getElementsByName(`answer_${question.question}`);
                            for (let j = 0; j < radioButtons.length; j++) {
                                if (radioButtons[j].checked) {
                                    userAnswer = radioButtons[j].value;
                                    break;
                                }
                            }
                        }
                        if (userAnswer === question.correctAnswer || question.correctAnswers.includes(question.options.indexOf(userAnswer))) {
                            score++;
                        }
                    }
                    alert(`Your score is ${score} out of ${quizData.length}`);
                }
            </script>
            <button onclick="checkQuiz()">Submit Quiz</button>
        </body>
        </html>
        """

        return html_content

    def save_html(self):
        html_content = self.create_html()
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(html_content)
            messagebox.showinfo("Success", f"HTML file saved successfully at {file_path}.")

    def generate_html(self):
        if not self.quiz_data:
            messagebox.showerror("Error", "No quiz data available to generate HTML.")
        else:
            self.save_html()

    def export_quizzes_as_json(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "w") as file:
                json.dump(self.quiz_data, file)
            messagebox.showinfo("Success", f"JSON file saved successfully at {file_path}.")

    def export_quizzes_as_xml(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML Files", "*.xml")])
        if file_path:
            root = ET.Element("quizzes")
            for quiz_item in self.quiz_data:
                quiz = ET.SubElement(root, "quiz")
                question = ET.SubElement(quiz, "question")
                question.text = quiz_item["question"]
                question_type = ET.SubElement(quiz, "type")
                question_type.text = quiz_item["question_type"]
                if quiz_item["question_type"] == "fill_in_the_blank":
                    correct_answer = ET.SubElement(quiz, "correct_answer")
                    correct_answer.text = quiz_item["correct_answer"]
                else:
                    options = ET.SubElement(quiz, "options")
                    for option in quiz_item["options"]:
                        option_element = ET.SubElement(options, "option")
                        option_element.text = option
                    correct_answers = ET.SubElement(quiz, "correct_answers")
                    for correct_answer in quiz_item["correct_answers"]:
                        correct_answer_element = ET.SubElement(correct_answers, "correct_answer")
                        correct_answer_element.text = str(correct_answer)
                difficulty_level = ET.SubElement(quiz, "difficulty_level")
                difficulty_level.text = quiz_item["difficulty_level"]
            tree = ET.ElementTree(root)
            tree.write(file_path)
            messagebox.showinfo("Success", f"XML file saved successfully at {file_path}.")

    def export_quizzes(self):
        export_type = filedialog.askstring("Export Type", "Enter 'json' or 'xml':")
        if export_type.lower() == "json":
            self.export_quizzes_as_json()
        elif export_type.lower() == "xml":
            self.export_quizzes_as_xml()
        else:
            messagebox.showerror("Invalid Input", "Please enter 'json' or 'xml'.")

    def upload_quizzes_from_csv(self):
        file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    question = row["question"]
                    question_type = row["type"]
                    difficulty_level = row["difficulty_level"]
                    if question_type == "fill_in_the_blank":
                        correct_answer = row["correct_answer"]
                        self.quiz_data.append({
                            "question": question,
                            "options": None,
                            "correct_answer": correct_answer,
                            "question_type": question_type,
                            "difficulty_level": difficulty_level
                        })
                    else:
                        options = [option.strip() for option in row["options"].split(',')]
                        correct_answers = [int(answer.strip()) for answer in row["correct_answers"].split(',')]
                        self.quiz_data.append({
                            "question": question,
                            "options": options,
                            "correct_answers": correct_answers,
                            "question_type": question_type,
                            "difficulty_level": difficulty_level
                        })
            messagebox.showinfo("Success", f"Quizzes uploaded successfully from {file_path}.")


