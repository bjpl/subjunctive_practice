import sys
import os
import json
import random
import logging
from typing import List
from dotenv import load_dotenv
import re

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QLabel, QLineEdit, QPushButton, QProgressBar, QTextEdit, QStackedWidget,
    QRadioButton, QButtonGroup, QStatusBar, QAction, QGroupBox, QCheckBox,
    QMessageBox, QToolBar, QScrollArea, QComboBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QRunnable, QObject, pyqtSignal, QThreadPool

import openai

# Load environment variables (ensure your OPENAI_API_KEY is set correctly)
load_dotenv()

# Configure Logging: logs will go to both file and console.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("subjunctive_practice.log", mode="a", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Set your OpenAI key (update your .env file with a valid key)
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")

# ---------------- Worker Classes for Asynchronous GPT Calls ----------------
class WorkerSignals(QObject):
    """Signals for worker threads."""
    result = pyqtSignal(str)

class GPTWorkerRunnable(QRunnable):
    """
    Worker thread for calling GPT asynchronously using OpenAI's ChatCompletion interface.
    """
    def __init__(self, prompt: str, model: str = "gpt-4", max_tokens: int = 600, temperature: float = 0.5):
        super().__init__()
        self.prompt = prompt
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.signals = WorkerSignals()

    def run(self) -> None:
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": ("You are an expert Spanish tutor specializing in LATAM Spanish. "
                                    "Your guidance should always reflect real-life conversational tone, "
                                    "using authentic expressions and culturally relevant details.")
                    },
                    {"role": "user", "content": self.prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
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
    Selections for triggers, tenses, and persons are required (no defaults are set).
    """
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Spanish Subjunctive Practice")
        self.setGeometry(100, 100, 1100, 700)

        # Set a global stylesheet for improved beauty and readability.
        self.setStyleSheet("""
            QMainWindow, QWidget, QGroupBox, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QProgressBar {
                font-family: Arial, sans-serif;
                font-size: 18px;
                padding: 6px;
                margin: 6px;
            }
            QCheckBox, QRadioButton {
                font-family: Arial, sans-serif;
                font-size: 20px;
                padding: 10px;
                margin: 10px;
            }
            QGroupBox {
                font-size: 20px;
                font-weight: bold;
                border: 1px solid #ccc;
                border-radius: 8px;
                margin: 8px;
                padding: 8px;
            }
            QPushButton {
                background-color: #007ACC;
                color: white;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #005F9E;
            }
            QComboBox {
                min-width: 200px;
                padding: 6px;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px;
            }
            QScrollArea {
                border: none;
            }
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
            }
        """)

        # Data structures for session management
        self.exercises: List[dict] = []
        self.current_exercise: int = 0
        self.total_exercises: int = 0
        self.correct_count: int = 0
        self.responses: List[dict] = []  # Session details

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
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Create the main splitter to hold left and right panes
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # ----- Left Pane: Indicators, Context, Stats -----
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(10)

        self.sentence_label = QLabel("Sentence will appear here.")
        self.sentence_label.setWordWrap(True)
        left_layout.addWidget(self.sentence_label)

        self.translation_label = QLabel("")
        self.translation_label.setWordWrap(True)
        self.translation_label.setStyleSheet("color: gray;")
        self.translation_label.setVisible(False)
        left_layout.addWidget(self.translation_label)

        self.stats_label = QLabel("Exercises: 0 | Correct: 0")
        self.stats_label.setStyleSheet("color: gray;")
        left_layout.addWidget(self.stats_label)

        # Subjunctive Triggers and Additional Context
        trigger_box = QGroupBox("Subjunctive Indicators & Context")
        trigger_layout = QVBoxLayout(trigger_box)
        trigger_layout.setSpacing(8)
        self.trigger_scroll_area = QScrollArea()
        self.trigger_scroll_area.setWidgetResizable(True)
        self.trigger_scroll_area.setMinimumHeight(150)
        trigger_scroll_content = QWidget()
        sc_layout = QVBoxLayout(trigger_scroll_content)
        sc_layout.setContentsMargins(5, 5, 5, 5)
        sc_layout.setSpacing(5)
        self.trigger_checkboxes = []
        typical_triggers = [
            "Wishes (querer que, desear que)", "Emotions (gustar que, sentir que)",
            "Impersonal expressions (es bueno que, es necesario que)",
            "Requests (pedir que, rogar que)",
            "Doubt/Denial (dudar que, no creer que)", "Negation (no pensar que, no es cierto que)",
            "Ojalá (ojalá que)", "Conjunctions (para que, antes de que, a menos que)",
            "Superlatives (el mejor ... que)", "Indefinite antecedents (busco a alguien que...)",
            "Nonexistent antecedents (no hay nadie que...)"
        ]
        for trig in typical_triggers:
            cb = QCheckBox(trig)
            sc_layout.addWidget(cb)
            self.trigger_checkboxes.append(cb)
        sc_layout.addStretch(1)
        self.trigger_scroll_area.setWidget(trigger_scroll_content)
        self.custom_context_input = QLineEdit()
        self.custom_context_input.setPlaceholderText("Enter additional context (e.g., polite request, uncertainty scenario)")
        trigger_layout.addWidget(self.trigger_scroll_area)
        trigger_layout.addWidget(self.custom_context_input)
        left_layout.addWidget(trigger_box)
        left_layout.addStretch()

        splitter.addWidget(left_widget)

        # ----- Right Pane: Answer Input, Feedback, Controls -----
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(10)

        # Tense and Person selections using checkboxes (no defaults)
        selection_box = QGroupBox("Select Tense(s) and Person(s)")
        sel_layout = QHBoxLayout(selection_box)
        sel_layout.setContentsMargins(10, 10, 10, 10)
        sel_layout.setSpacing(20)

        # -- Tense(s) box --
        tense_box = QGroupBox("Tense(s)")
        tense_layout = QVBoxLayout(tense_box)
        tense_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.tense_checkboxes = {}
        tenses = [
            "Present Subjunctive",
            "Imperfect Subjunctive (ra)",
            "Imperfect Subjunctive (se)",
            "Present Perfect Subjunctive",
            "Pluperfect Subjunctive",
        ]
        for tense in tenses:
            cb = QCheckBox(tense)
            self.tense_checkboxes[tense] = cb
            tense_layout.addWidget(cb)
        tense_box.setLayout(tense_layout)

        # -- Person(s) box --
        person_box = QGroupBox("Person(s)")
        person_layout = QVBoxLayout(person_box)
        person_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.person_checkboxes = {}
        persons = ["yo", "tú", "él/ella/usted", "nosotros", "vosotros", "ellos/ellas/ustedes"]
        for person in persons:
            cb = QCheckBox(person)
            self.person_checkboxes[person] = cb
            person_layout.addWidget(cb)
        person_box.setLayout(person_layout)

        sel_layout.addWidget(tense_box, 1)
        sel_layout.addWidget(person_box, 1)
        sel_layout.addStretch()
        right_layout.addWidget(selection_box)

        # Specific Verbs (optional)
        verb_box = QGroupBox("Specific Verbs (optional, comma-separated)")
        vb_layout = QHBoxLayout(verb_box)
        self.verbs_input = QLineEdit()
        self.verbs_input.setPlaceholderText("e.g., hablar, comer, vivir")
        vb_layout.addWidget(self.verbs_input)
        right_layout.addWidget(verb_box)

        # Sentence mode selection: Free Response vs. Multiple Choice
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Select Mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Free Response", "Multiple Choice"])
        self.mode_combo.currentIndexChanged.connect(self.switchMode)
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        right_layout.addLayout(mode_layout)

        # Input stack for answer entry
        self.input_stack = QStackedWidget()
        free_response_page = QWidget()
        fr_layout = QVBoxLayout(free_response_page)
        self.free_response_input = QLineEdit()
        self.free_response_input.setPlaceholderText("Type your answer here...")
        fr_layout.addWidget(self.free_response_input)
        self.input_stack.addWidget(free_response_page)
        mc_page = QWidget()
        mc_layout = QVBoxLayout(mc_page)
        self.mc_button_group = QButtonGroup(mc_page)
        self.mc_options_layout = QHBoxLayout()  # Horizontal arrangement for multiple choice options
        mc_layout.addLayout(self.mc_options_layout)
        self.input_stack.addWidget(mc_page)
        right_layout.addWidget(self.input_stack)

        # Navigation Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        self.prev_button = QPushButton("Previous")
        self.hint_button = QPushButton("Hint")
        self.submit_button = QPushButton("Submit")
        self.next_button = QPushButton("Next")
        for btn in (self.prev_button, self.hint_button, self.submit_button, self.next_button):
            btn.setStyleSheet("padding: 8px;")
        buttons_layout.addWidget(self.prev_button)
        buttons_layout.addWidget(self.hint_button)
        buttons_layout.addWidget(self.submit_button)
        buttons_layout.addWidget(self.next_button)
        right_layout.addLayout(buttons_layout)

        # --- Feedback Text (Explanations) with Scrollability ---
        self.feedback_text = QTextEdit()
        self.feedback_text.setReadOnly(True)
        self.feedback_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        feedback_scroll = QScrollArea()
        feedback_scroll.setWidgetResizable(True)
        feedback_scroll.setWidget(self.feedback_text)
        right_layout.addWidget(feedback_scroll)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        right_layout.addWidget(self.progress_bar)

        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        # Connect buttons
        self.submit_button.clicked.connect(self.submitAnswer)
        self.next_button.clicked.connect(self.nextExercise)
        self.prev_button.clicked.connect(self.prevExercise)
        self.hint_button.clicked.connect(self.provideHint)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.updateStatus("Welcome! Please make all required selections and generate new exercises.")

        # Initialize exercise data
        self.exercises = []
        self.total_exercises = 0
        self.updateStats()
        logger.info("Application initialized.")

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
            logger.info("Switched to light theme.")
        else:
            dark_stylesheet = """
                QMainWindow, QWidget, QGroupBox, QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QTextEdit, QProgressBar {
                    font-family: Arial, sans-serif;
                    font-size: 18px;
                    color: #ffffff;
                    background-color: #3c3f41;
                }
                QGroupBox {
                    border: 1px solid #666;
                    border-radius: 8px;
                    padding: 8px;
                    margin: 8px;
                }
                QPushButton {
                    background-color: #4c5052;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #60666c;
                }
            """
            self.setStyleSheet(dark_stylesheet)
            self.dark_mode = True
            self.updateStatus("Switched to dark theme.")
            logger.info("Switched to dark theme.")

    def toggleTranslation(self):
        self.show_translation = not self.show_translation
        self.translation_label.setVisible(self.show_translation)
        self.updateExercise()
        self.updateStatus("Translation " + ("on" if self.show_translation else "off"))
        logger.info("Translation toggled %s", "on" if self.show_translation else "off")

    def updateStats(self):
        self.stats_label.setText(f"Exercises: {self.current_exercise + 1}/{self.total_exercises} | Correct: {self.correct_count}")

    def updateStatus(self, msg: str):
        self.status_bar.showMessage(msg, 4000)
        logger.info("Status update: %s", msg)

    def getSelectedTriggers(self) -> List[str]:
        return [cb.text() for cb in self.trigger_checkboxes if cb.isChecked()]

    def getSelectedTenses(self) -> List[str]:
        return [tense for tense, cb in self.tense_checkboxes.items() if cb.isChecked()]

    def getSelectedPersons(self) -> List[str]:
        return [person for person, cb in self.person_checkboxes.items() if cb.isChecked()]

    def generateNewExercise(self):
        selected_triggers = self.getSelectedTriggers()
        if not selected_triggers:
            QMessageBox.warning(self, "Selection Required", "Please select at least one subjunctive trigger.")
            return
        selected_tenses = self.getSelectedTenses()
        if not selected_tenses:
            QMessageBox.warning(self, "Selection Required", "Please select at least one tense.")
            return
        selected_persons = self.getSelectedPersons()
        if not selected_persons:
            QMessageBox.warning(self, "Selection Required", "Please select at least one person.")
            return

        triggers_text = "; ".join(selected_triggers)
        tenses_text = ", ".join(selected_tenses)
        persons_text = ", ".join(selected_persons)
        additional_context = self.custom_context_input.text().strip()
        verbs_text = self.verbs_input.text().strip() or "Any relevant verb"

        # Revised prompt with explicit JSON instructions:
        prompt = (
            "You are an expert Spanish tutor focusing on subjunctive practice (any subjunctive tense). "
            "Generate 5 unique exercises that reflect real-life, authentic language usage in Latin American Spanish. "
            "Each exercise must include the following keys exactly: \"context\", \"sentence\", \"answer\", \"choices\", and \"translation\". "
            "All values should be strings (or an array of strings for \"choices\") that are appropriate for everyday conversation. "
            "IMPORTANT: Return ONLY a strictly valid JSON array of 5 objects, with no additional text, no markdown formatting, and no extra commentary.\n\n"
            "Incorporate these required selections:\n"
            f"   Tense(s): {tenses_text}\n"
            f"   Person(s): {persons_text}\n"
            f"   Specific Verb(s): {verbs_text}\n"
            "If additional context is provided, incorporate it as well:\n"
            f"   Additional Context: {additional_context}\n\n"
            "The JSON output must be strictly valid."
        )

        worker = GPTWorkerRunnable(prompt, max_tokens=800, temperature=0.7)
        worker.signals.result.connect(self.handleNewExerciseResult)
        self.threadpool.start(worker)
        self.updateStatus("Generating new exercises...")
        logger.info("Generating new exercises with prompt: %s", prompt)

    def handleNewExerciseResult(self, result: str):
        logger.info("Raw GPT response received:\n%s", result)
        result = result.replace("```", "").replace("`", "").strip()
        start_index = result.find("[")
        end_index = result.rfind("]")
        if start_index != -1 and end_index != -1:
            json_str = result[start_index:end_index+1]
        else:
            json_str = result
        logger.info("Extracted JSON substring:\n%s", json_str)
        def remove_trailing_commas(s: str) -> str:
            return re.sub(r',\s*([\]}}])', r'\1', s)
        old_str = None
        while old_str != json_str:
            old_str = json_str
            json_str = remove_trailing_commas(json_str)
        logger.info("After removing trailing commas:\n%s", json_str)
        if not json_str.endswith("]"):
            json_str += "]"
            logger.info("Appended closing bracket:\n%s", json_str)
        try:
            new_exercises = json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error("Error parsing JSON from GPT: %s", e)
            QMessageBox.warning(self, "Parsing Error", "Failed to parse the JSON. Please try generating new exercises.")
            return
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
        logger.info("New exercises generated successfully.")

    def updateExercise(self) -> None:
        if self.total_exercises == 0 or self.current_exercise < 0 or self.current_exercise >= self.total_exercises:
            return
        exercise = self.exercises[self.current_exercise]
        if "context" in exercise and exercise["context"]:
            full_text = exercise["context"] + "\n\n" + exercise.get("sentence", "")
        else:
            full_text = exercise.get("sentence", "")
        self.sentence_label.setText(full_text)
        self.sentence_label.adjustSize()
        self.sentence_label.update()
        if self.show_translation and "translation" in exercise:
            self.translation_label.setText(exercise["translation"])
        else:
            self.translation_label.setText("")
        self.translation_label.adjustSize()
        self.translation_label.update()
        self.feedback_text.clear()
        self.progress_bar.setValue(self.current_exercise + 1)
        self.updateStatus(f"Exercise {self.current_exercise + 1} of {self.total_exercises}")
        mode = self.mode_combo.currentText()
        if mode == "Free Response":
            self.input_stack.setCurrentIndex(0)
            self.free_response_input.clear()
            self.free_response_input.update()
        elif mode == "Multiple Choice":
            self.input_stack.setCurrentIndex(1)
            choices = list(exercise["choices"])
            random.shuffle(choices)
            self.populateMultipleChoice(choices)
        self.updateStats()
        self.repaint()

    def switchMode(self, force=None):
        mode = self.mode_combo.currentText()
        if force == "Free":
            self.input_stack.setCurrentIndex(0)
        elif force == "MC":
            self.input_stack.setCurrentIndex(1)
        else:
            self.input_stack.setCurrentIndex(0 if mode == "Free Response" else 1)

    def populateMultipleChoice(self, choices: List[str]) -> None:
        while self.mc_options_layout.count():
            item = self.mc_options_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.mc_button_group = QButtonGroup()
        for choice in choices:
            radio = QRadioButton(choice)
            self.mc_button_group.addButton(radio)
            self.mc_options_layout.addWidget(radio)
        self.mc_options_layout.addStretch()
        buttons = self.mc_button_group.buttons()
        if buttons:
            buttons[0].setChecked(True)
        current_widget = self.input_stack.currentWidget()
        current_widget.adjustSize()
        current_widget.update()
        current_widget.repaint()

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
        sentence_for_gpt = exercise.get("sentence", "")
        self.generateGPTExplanationAsync(user_answer, correct_answer, is_correct, sentence_for_gpt, base_feedback)
        logger.info("Submitted answer '%s' for exercise %d", user_answer, self.current_exercise + 1)

    def generateGPTExplanationAsync(self, user_ans: str, correct_ans: str, is_correct: bool, sentence: str, base_feedback: str):
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
        logging.info("Generating explanation with prompt: %s", prompt)

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
        logging.info("Explanation provided for exercise %d", self.current_exercise + 1)

    def provideHint(self):
        if self.total_exercises == 0:
            self.updateStatus("No exercise available.")
            return
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
        logging.info("Providing hint for exercise %d", self.current_exercise + 1)

    def handleHintResult(self, result: str):
        self.feedback_text.setText("Hint: " + result)
        self.updateStatus("Hint provided.")
        logging.info("Hint provided: %s", result)

    def nextExercise(self):
        if self.total_exercises == 0:
            self.updateStatus("No exercises available. Generate new ones first.")
            return
        if self.current_exercise < self.total_exercises - 1:
            self.current_exercise += 1
            self.updateExercise()
            logging.info("Moved to next exercise: %d", self.current_exercise + 1)
        else:
            self.updateStatus("You are at the last exercise.")
            logging.info("Already at the last exercise.")
        self.updateStats()

    def prevExercise(self):
        if self.total_exercises == 0:
            self.updateStatus("No exercises available.")
            return
        if self.current_exercise > 0:
            self.current_exercise -= 1
            self.updateExercise()
            logging.info("Moved to previous exercise: %d", self.current_exercise + 1)
        else:
            self.updateStatus("You are at the first exercise.")
            logging.info("Already at the first exercise.")
        self.updateStats()

    def resetProgress(self):
        self.current_exercise = 0
        self.correct_count = 0
        self.responses.clear()
        self.updateExercise()
        self.updateStatus("Progress reset.")
        self.updateStats()
        logging.info("Progress reset.")

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
        logging.info("Generating session summary.")

    def handleSummaryResult(self, result: str):
        QMessageBox.information(self, "Session Summary", result)
        self.updateStatus("Session summary generated.")
        logging.info("Session summary generated.")

    def closeEvent(self, event):
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
