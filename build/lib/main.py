import sys
import os
import json
import random
import logging
from typing import List
from dotenv import load_dotenv

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QLabel, QLineEdit, QPushButton, QProgressBar, QTextEdit, QComboBox,
    QStackedWidget, QRadioButton, QButtonGroup, QStatusBar, QAction, QGroupBox,
    QCheckBox, QMessageBox, QToolBar, QScrollArea
)
from PyQt5.QtCore import Qt, QRunnable, QObject, pyqtSignal, QThreadPool

# -------------- OPTIONAL: If you want to use the updated openai.OpenAI client --------------
# -------------- from openai >= 1.0.0, just as in your SpanishConjugationGUI ---------------
# import openai
# from openai import OpenAI
# ------------------------------------------------------------------------------------------
import openai

# Load environment variables
load_dotenv()

# Configure Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("subjunctive_practice.log", mode="a", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Set your OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")
# If using the newer client style: client = OpenAI()

# ---------------- Worker Classes for Asynchronous GPT Calls ----------------
class WorkerSignals(QObject):
    """Signals for worker threads."""
    result = pyqtSignal(str)


class GPTWorkerRunnable(QRunnable):
    """
    Worker thread for asynchronous calls to GPT.
    Provide a 'prompt' plus optional model, max_tokens, temperature, etc.
    """
    def __init__(self, prompt: str, model: str = "gpt-4", max_tokens: int = 500, temperature: float = 0.6):
        super().__init__()
        self.prompt = prompt
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.signals = WorkerSignals()

    def run(self) -> None:
        try:
            # Example usage with the "old" openai.Completion or ChatCompletion
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert Spanish tutor specializing in the subjunctive mood (all tenses) "
                            "in Latin American Spanish. You provide realistic contextual practice."
                        )
                    },
                    {
                        "role": "user",
                        "content": self.prompt
                    },
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            output = response.choices[0].message.content.strip()
            logging.info("GPT response received.")
        except Exception as e:
            output = f"Error: {str(e)}"
            logging.error("Error in GPTWorkerRunnable: %s", e)

        self.signals.result.emit(output)

# ---------------- Main GUI ----------------
class SpanishSubjunctivePracticeGUI(QMainWindow):
    """
    A specialized GUI for practicing all Spanish subjunctive forms and triggers.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Spanish Subjunctive Practice")
        self.setGeometry(100, 100, 1100, 700)

        # Data structures
        self.exercises: List[dict] = []
        self.current_exercise: int = 0
        self.total_exercises: int = 0
        self.correct_count: int = 0
        self.responses: List[dict] = []  # To store session details

        # Settings
        self.dark_mode = False
        self.show_translation = False
        self.threadpool = QThreadPool()

        self.initUI()

    def initUI(self) -> None:
        self.createToolBar()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # ----- Left Pane: Large Area for Subjunctive Indicators, Context, Stats -----
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        self.sentence_label = QLabel("Sentence will appear here.")
        self.sentence_label.setWordWrap(True)
        self.sentence_label.setStyleSheet("font-size: 20px; padding: 20px;")
        left_layout.addWidget(self.sentence_label)

        self.translation_label = QLabel("")
        self.translation_label.setWordWrap(True)
        self.translation_label.setStyleSheet("font-size: 16px; padding: 10px; color: gray;")
        self.translation_label.setVisible(False)
        left_layout.addWidget(self.translation_label)

        self.stats_label = QLabel("Exercises: 0 | Correct: 0")
        self.stats_label.setStyleSheet("font-size: 14px; color: gray; padding: 10px;")
        left_layout.addWidget(self.stats_label)

        # Subjunctive Trigger/Indicator Panel
        trigger_box = QGroupBox("Subjunctive Indicators & Context")
        trigger_layout = QVBoxLayout(trigger_box)

        # We can split triggers into categories (WEDDING: Wishes, Emotions, Doubt/Denial, etc.)
        # For example, let's create checkboxes for typical triggers:
        self.trigger_scroll_area = QScrollArea()
        self.trigger_scroll_area.setWidgetResizable(True)
        trigger_scroll_content = QWidget()
        sc_layout = QVBoxLayout(trigger_scroll_content)
        self.trigger_checkboxes = []

        typical_triggers = [
            "Wishes (querer que, desear que)", "Emotions (gustar que, sentir que)",
            "Impersonal expressions (es bueno que, es necesario que)",
            "Requests (pedir que, rogar que)",
            "Doubt/Denial (dudar que, no creer que)", "Negation (no pensar que, no es cierto que)",
            "Ojalá (ojalá que)", "Conjunctions (para que, antes de que, a menos que)",
            "Superlatives (el mejor ... que)", "Indefinite antecedents (busco a alguien que...)",
            "Nonexistent antecedents (no hay nadie que...)",
            # Add or remove more as needed
        ]
        for trig in typical_triggers:
            cb = QCheckBox(trig)
            sc_layout.addWidget(cb)
            self.trigger_checkboxes.append(cb)
        sc_layout.addStretch(1)
        self.trigger_scroll_area.setWidget(trigger_scroll_content)

        # Additional text inputs for context
        self.custom_context_input = QLineEdit()
        self.custom_context_input.setPlaceholderText("Optional additional context (e.g., polite request, uncertainty scenario)")

        trigger_layout.addWidget(self.trigger_scroll_area)
        trigger_layout.addWidget(self.custom_context_input)
        left_layout.addWidget(trigger_box)

        left_layout.addStretch()
        splitter.addWidget(left_widget)

        # ----- Right Pane: Answer Input, Feedback, Controls -----
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Tense / Person options for the subjunctive
        form_box = QGroupBox("Subjunctive Tenses / Persons")
        form_layout = QHBoxLayout(form_box)
        self.tense_combo = QComboBox()
        # Add multiple subjunctive tenses
        self.tense_combo.addItems([
            "Present Subjunctive", 
            "Imperfect Subjunctive (ra)", 
            "Imperfect Subjunctive (se)", 
            "Present Perfect Subjunctive", 
            "Pluperfect Subjunctive"
        ])
        self.person_combo = QComboBox()
        self.person_combo.addItems([
            "yo", "tú", "él/ella/usted", "nosotros", "vosotros", "ellos/ellas/ustedes"
        ])
        form_layout.addWidget(QLabel("Tense:"))
        form_layout.addWidget(self.tense_combo)
        form_layout.addWidget(QLabel("Person:"))
        form_layout.addWidget(self.person_combo)
        right_layout.addWidget(form_box)

        # Specific Verbs
        verb_box = QGroupBox("Specific Verbs (optional, comma-separated)")
        vb_layout = QHBoxLayout(verb_box)
        self.verbs_input = QLineEdit()
        self.verbs_input.setPlaceholderText("e.g., hablar, comer, vivir...")
        vb_layout.addWidget(self.verbs_input)
        right_layout.addWidget(verb_box)

        # The sentence mode: free response vs multiple choice
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Select Mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Free Response", "Multiple Choice"])
        self.mode_combo.currentIndexChanged.connect(self.switchMode)
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        right_layout.addLayout(mode_layout)

        # Input stack
        self.input_stack = QStackedWidget()
        # Page 1: Free response
        free_response_page = QWidget()
        fr_layout = QVBoxLayout(free_response_page)
        self.free_response_input = QLineEdit()
        self.free_response_input.setPlaceholderText("Type your answer here...")
        self.free_response_input.setStyleSheet("font-size: 18px; padding: 8px;")
        fr_layout.addWidget(self.free_response_input)
        self.input_stack.addWidget(free_response_page)
        # Page 2: Multiple choice
        mc_page = QWidget()
        mc_layout = QVBoxLayout(mc_page)
        self.mc_button_group = QButtonGroup(mc_page)
        self.mc_options_layout = QVBoxLayout()
        mc_layout.addLayout(self.mc_options_layout)
        self.input_stack.addWidget(mc_page)

        right_layout.addWidget(self.input_stack)

        # Buttons
        buttons_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.hint_button = QPushButton("Hint")
        self.submit_button = QPushButton("Submit")
        self.next_button = QPushButton("Next")
        for btn in (self.prev_button, self.hint_button, self.submit_button, self.next_button):
            btn.setStyleSheet("font-size: 16px; padding: 8px;")
        buttons_layout.addWidget(self.prev_button)
        buttons_layout.addWidget(self.hint_button)
        buttons_layout.addWidget(self.submit_button)
        buttons_layout.addWidget(self.next_button)
        right_layout.addLayout(buttons_layout)

        self.feedback_text = QTextEdit()
        self.feedback_text.setReadOnly(True)
        self.feedback_text.setStyleSheet("font-size: 16px; padding: 10px;")
        right_layout.addWidget(self.feedback_text)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("height: 25px;")
        right_layout.addWidget(self.progress_bar)

        splitter.addWidget(right_widget)
        splitter.setSizes([450, 650])

        # Button connections
        self.submit_button.clicked.connect(self.submitAnswer)
        self.next_button.clicked.connect(self.nextExercise)
        self.prev_button.clicked.connect(self.prevExercise)
        self.hint_button.clicked.connect(self.provideHint)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.updateStatus("Welcome to Subjunctive Practice! Generate new exercises to start.")

        # Initialize
        self.exercises = []
        self.total_exercises = 0
        self.updateStats()

    def createToolBar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        new_action = QAction("New Exercises", self)
        new_action.setToolTip("Generate new subjunctive exercises")
        new_action.triggered.connect(self.generateNewExercise)
        toolbar.addAction(new_action)

        reset_action = QAction("Reset Progress", self)
        reset_action.setToolTip("Reset your session progress")
        reset_action.triggered.connect(self.resetProgress)
        toolbar.addAction(reset_action)

        summary_action = QAction("Summary", self)
        summary_action.setToolTip("Generate session summary")
        summary_action.triggered.connect(self.generateSessionSummary)
        toolbar.addAction(summary_action)

        theme_action = QAction("Toggle Theme", self)
        theme_action.setToolTip("Toggle Light/Dark themes")
        theme_action.triggered.connect(self.toggleTheme)
        toolbar.addAction(theme_action)

        translation_action = QAction("Toggle Translation", self)
        translation_action.setToolTip("Show/hide English translation")
        translation_action.triggered.connect(self.toggleTranslation)
        toolbar.addAction(translation_action)

    def toggleTheme(self):
        if self.dark_mode:
            self.setStyleSheet("")
            self.dark_mode = False
            self.updateStatus("Switched to light theme.")
        else:
            dark_stylesheet = """
                QMainWindow { background-color: #2b2b2b; color: #ffffff; }
                QLabel, QGroupBox, QStatusBar, QToolBar { color: #ffffff; }
                QLineEdit, QTextEdit, QComboBox, QProgressBar { background-color: #3c3f41; color: #ffffff; }
                QPushButton { background-color: #3c3f41; color: #ffffff; }
                QPushButton:hover { background-color: #4c5052; }
            """
            self.setStyleSheet(dark_stylesheet)
            self.dark_mode = True
            self.updateStatus("Switched to dark theme.")

    def toggleTranslation(self):
        self.show_translation = not self.show_translation
        self.translation_label.setVisible(self.show_translation)
        self.updateExercise()
        self.updateStatus("Translation " + ("on" if self.show_translation else "off"))

    def updateStats(self):
        self.stats_label.setText(f"Exercises: {self.current_exercise + 1}/{self.total_exercises} | Correct: {self.correct_count}")

    def updateStatus(self, msg: str):
        self.status_bar.showMessage(msg, 4000)

    # ---------------- Exercises Management ----------------
    def generateNewExercise(self):
        # Gather selected triggers
        selected_triggers = [cb.text() for cb in self.trigger_checkboxes if cb.isChecked()]
        if not selected_triggers:
            selected_triggers = ["any typical subjunctive indicator"]
        triggers_text = "; ".join(selected_triggers)

        # Additional context
        additional_context = self.custom_context_input.text().strip()

        # Tense
        chosen_tense = self.tense_combo.currentText()
        # Person
        chosen_person = self.person_combo.currentText()

        # Specific verbs
        verbs_text = self.verbs_input.text().strip()
        if not verbs_text:
            verbs_text = "Any relevant verb"

        # We want multiple exercises that revolve specifically around practicing the subjunctive with these triggers
        # We'll ask GPT to produce a JSON array of exercises. Each object: { context, sentence, answer, choices, translation }
        prompt = (
            "You are an expert Spanish tutor focusing on subjunctive practice (any subjunctive tense). "
            "Generate 5 unique exercises that truly reflect real-life usage in Latin American Spanish. "
            "Each exercise includes:\n"
            "1) \"context\": 1-3 sentences of natural text giving a scenario that uses or implies a subjunctive trigger.\n"
            "2) \"sentence\": A short sentence that has a blank for a subjunctive verb. This sentence should incorporate one or more of these triggers:\n"
            f"   {triggers_text}\n\n"
            "3) \"answer\": The correct subjunctive conjugation to fill in the blank.\n"
            "4) \"choices\": An array of four plausible answers (including the correct one).\n"
            "5) \"translation\": An English translation of the Spanish sentence (keeping the blank).\n"
            "Ensure you use or hint at these triggers in a natural, realistic manner. If user context is provided, incorporate it:\n"
            f"Additional user context: {additional_context}\n\n"
            f"Requested Tense/Person in the blank (if feasible): {chosen_tense}, {chosen_person}\n"
            f"Specific verbs to use (if feasible): {verbs_text}\n"
            "Return a strictly valid JSON array of 5 objects, no markdown or code fences."
        )

        worker = GPTWorkerRunnable(prompt, max_tokens=800, temperature=0.7)
        worker.signals.result.connect(self.handleNewExerciseResult)
        self.threadpool.start(worker)
        self.updateStatus("Generating new exercises...")

    def handleNewExerciseResult(self, result: str):
        logging.info("Raw GPT response:\n%s", result)
        # Strip code fences if GPT includes them
        if result.startswith("```"):
            lines = result.splitlines()
            # remove lines that are triple backticks
            lines = [ln for ln in lines if not ln.strip().startswith("```")]
            result = "\n".join(lines).strip()

        try:
            new_exercises = json.loads(result)
        except json.JSONDecodeError as e:
            logging.error("Error parsing JSON from GPT: %s", e)
            QMessageBox.warning(self, "Parsing Error", "Failed to parse the JSON. Trying again.")
            self.generateNewExercise()
            return

        # Minimal validation
        if not isinstance(new_exercises, list) or len(new_exercises) == 0:
            QMessageBox.warning(self, "Error", "GPT returned an empty or invalid list. Try again.")
            return

        self.exercises = new_exercises
        self.total_exercises = len(self.exercises)
        self.current_exercise = 0
        self.correct_count = 0
        self.responses.clear()
        self.progress_bar.setMaximum(self.total_exercises)
        self.updateExercise()
        self.updateStats()
        self.updateStatus("New exercises generated.")

    def updateExercise(self):
        if self.total_exercises == 0 or self.current_exercise < 0 or self.current_exercise >= self.total_exercises:
            return
        exercise = self.exercises[self.current_exercise]
        full_text = exercise.get("context", "") + "\n\n" + exercise.get("sentence", "")
        self.sentence_label.setText(full_text)

        # Show translation if toggled on
        if self.show_translation:
            self.translation_label.setText(exercise.get("translation", ""))
        else:
            self.translation_label.setText("")

        self.feedback_text.clear()
        self.progress_bar.setValue(self.current_exercise + 1)
        self.updateStatus(f"Exercise {self.current_exercise + 1} of {self.total_exercises}")

        mode = self.mode_combo.currentText()
        if mode == "Free Response":
            self.free_response_input.clear()
            self.switchMode(force="Free")
        else:
            self.populateMultipleChoice(exercise.get("choices", []))
            self.switchMode(force="MC")

        self.updateStats()

    def switchMode(self, force=None):
        mode = self.mode_combo.currentText()
        if force == "Free":
            self.input_stack.setCurrentIndex(0)
        elif force == "MC":
            self.input_stack.setCurrentIndex(1)
        else:
            if mode == "Free Response":
                self.input_stack.setCurrentIndex(0)
            else:
                self.input_stack.setCurrentIndex(1)

    def populateMultipleChoice(self, choices: List[str]):
        # Clear layout
        while self.mc_options_layout.count():
            child = self.mc_options_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Re-create button group
        self.mc_button_group = QButtonGroup()
        random.shuffle(choices)
        for choice in choices:
            rb = QRadioButton(choice)
            self.mc_button_group.addButton(rb)
            self.mc_options_layout.addWidget(rb)

        # Optionally pre-check first
        buttons = self.mc_button_group.buttons()
        if buttons:
            buttons[0].setChecked(True)

    def getUserAnswer(self):
        mode = self.mode_combo.currentText()
        if mode == "Free Response":
            return self.free_response_input.text().strip().lower()
        else:
            for btn in self.mc_button_group.buttons():
                if btn.isChecked():
                    return btn.text().strip().lower()
        return ""

    def submitAnswer(self):
        if self.total_exercises == 0:
            self.updateStatus("No exercises available. Generate new ones first.")
            return

        user_answer = self.getUserAnswer()
        if not user_answer:
            self.updateStatus("Please provide an answer.")
            return

        exercise = self.exercises[self.current_exercise]
        correct_answer = exercise.get("answer", "").strip().lower()
        if user_answer == correct_answer:
            is_correct = True
            base_feedback = "Correct! Excellent use of the subjunctive."
            self.correct_count += 1
        else:
            is_correct = False
            base_feedback = f"Incorrect. The correct answer is '{correct_answer}'."

        # Optional: get sentence for context
        sentence_for_gpt = exercise.get("sentence", "")
        self.generateGPTExplanationAsync(user_answer, correct_answer, is_correct, sentence_for_gpt, base_feedback)

    def generateGPTExplanationAsync(self, user_ans: str, correct_ans: str, is_correct: bool, sentence: str, base_feedback: str):
        # We'll ask GPT to briefly explain why it's correct/incorrect. 
        # We keep it strictly about grammar or nuance.
        prompt = (
            "You are an expert Spanish tutor focusing on the subjunctive. "
            f"Sentence: \"{sentence}\"\n"
            f"User's Answer: {user_ans}\n"
            f"Correct Answer: {correct_ans}\n"
            "Is the user's answer correct? " + ("Yes" if is_correct else "No") + "\n\n"
            "Briefly explain in LATAM Spanish the reason behind the correct use of subjunctive (or why it is incorrect), "
            "without filler or excess praise."
        )
        worker = GPTWorkerRunnable(prompt, max_tokens=150, temperature=0.5)
        worker.signals.result.connect(lambda result: self.handleExplanationResult(result, base_feedback))
        self.threadpool.start(worker)

    def handleExplanationResult(self, gpt_response: str, base_feedback: str):
        full_feedback = base_feedback + "\n\n" + gpt_response
        self.feedback_text.setText(full_feedback)

        self.responses.append({
            "exercise_index": self.current_exercise,
            "sentence": self.exercises[self.current_exercise].get("sentence", ""),
            "translation": self.exercises[self.current_exercise].get("translation", ""),
            "user_answer": self.getUserAnswer(),
            "correct": base_feedback.startswith("Correct"),
            "explanation": gpt_response
        })
        self.updateStats()

    def provideHint(self):
        if self.total_exercises == 0:
            self.updateStatus("No exercise available.")
            return

        # We can prompt GPT for a hint
        exercise = self.exercises[self.current_exercise]
        sentence = exercise.get("sentence", "")
        correct_ans = exercise.get("answer", "")
        hint_prompt = (
            "You are an expert Spanish tutor focusing on the subjunctive. "
            f"Sentence: \"{sentence}\"\n"
            f"Correct Subjunctive Form: {correct_ans}\n\n"
            "Provide a subtle hint in Spanish that nudges the student toward the correct subjunctive form, "
            "without revealing the answer directly."
        )
        worker = GPTWorkerRunnable(hint_prompt, max_tokens=100, temperature=0.5)
        worker.signals.result.connect(self.handleHintResult)
        self.threadpool.start(worker)

    def handleHintResult(self, result: str):
        self.feedback_text.setText("Hint: " + result)
        self.updateStatus("Hint provided.")

    def nextExercise(self):
        if self.total_exercises == 0:
            self.updateStatus("No exercises available. Generate new ones first.")
            return
        if self.current_exercise < self.total_exercises - 1:
            self.current_exercise += 1
            self.updateExercise()
        else:
            self.updateStatus("You are at the last exercise.")
        self.updateStats()

    def prevExercise(self):
        if self.total_exercises == 0:
            self.updateStatus("No exercises available.")
            return
        if self.current_exercise > 0:
            self.current_exercise -= 1
            self.updateExercise()
        else:
            self.updateStatus("You are at the first exercise.")
        self.updateStats()

    def resetProgress(self):
        self.current_exercise = 0
        self.correct_count = 0
        self.responses.clear()
        self.updateExercise()
        self.updateStatus("Progress reset.")
        self.updateStats()

    def generateSessionSummary(self):
        if not self.responses:
            QMessageBox.information(self, "Summary", "No data to summarize yet.")
            return

        session_data = "\n".join(
            f"Exercise {r['exercise_index']+1} - Sentence: {r['sentence']}\n"
            f"  Your answer: {r['user_answer']} | Correct: {r['correct']}\n"
            f"  Explanation: {r['explanation']}\n"
            for r in self.responses
        )

        summary_prompt = (
            "You are an expert Spanish tutor summarizing a student's practice on Spanish subjunctive. "
            "Here are the details:\n"
            f"{session_data}\n\n"
            "Please provide a concise summary in Spanish that highlights strengths, correct uses of the subjunctive, "
            "common errors, and suggestions for improvement. Avoid being overly long or repetitive."
        )
        worker = GPTWorkerRunnable(summary_prompt, max_tokens=200, temperature=0.5)
        worker.signals.result.connect(self.handleSummaryResult)
        self.threadpool.start(worker)

    def handleSummaryResult(self, result: str):
        QMessageBox.information(self, "Session Summary", result)
        self.updateStatus("Session summary generated.")

    def closeEvent(self, event):
        # Save to a log file if you wish
        try:
            with open("subjunctive_session_log.txt", "a", encoding="utf-8") as f:
                f.write("\n=== Subjunctive Session Log ===\n")
                for r in self.responses:
                    f.write(
                        f"Exercise {r['exercise_index']+1}\n"
                        f"  Sentence: {r['sentence']}\n"
                        f"  Translation: {r['translation']}\n"
                        f"  User answer: {r['user_answer']}\n"
                        f"  Correct: {r['correct']}\n"
                        f"  Explanation: {r['explanation']}\n\n"
                    )
                f.write("=== End of Session ===\n\n")
            logging.info("Subjunctive practice session log saved.")
        except Exception as e:
            logging.error("Error writing log: %s", e)

        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpanishSubjunctivePracticeGUI()
    window.show()
    sys.exit(app.exec_())
