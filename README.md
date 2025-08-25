# Spanish Subjunctive Practice

A desktop application for practicing Spanish subjunctive forms with AI-powered exercises and explanations.

## Features

- **Practice Modes**
  - **Traditional Grammar**: All subjunctive tenses with customizable triggers
  - **TBLT Scenarios**: Real-world communicative tasks (workplace, travel, social)
  - **Mood Contrast**: Compare indicative vs subjunctive usage
  - Free response and multiple choice formats
  - Adaptive difficulty levels (Beginner, Intermediate, Advanced)

- **Pedagogical Approach**
  - Task-Based Language Teaching (TBLT) methodology
  - Communicative language teaching principles
  - Focus on real-world language use
  - Context-rich situational exercises
  - Stem-changing verb support
  - Sequence of tenses rules
  - Spaced repetition algorithm for retention

- **Learning Tools**
  - GPT-powered contextual explanations (optimized for speed)
  - Smart error analysis with personalized tips
  - Adaptive difficulty adjustment
  - Real-time accuracy tracking
  - Session statistics and analytics
  - Export sessions to CSV
  - Progress monitoring with detailed metrics

- **Motivation & Analytics**
  - Daily practice streak tracking
  - Achievement system with goals
  - Weakness identification and targeted practice
  - Performance-based difficulty adaptation
  - Progress visualization and reports

- **User Experience**
  - Keyboard shortcuts (Enter to submit, Arrow keys to navigate, H for hint)
  - Light/Dark theme support
  - English translations toggle
  - Session persistence and logging
  - Error recovery and input validation

## Setup

### Requirements
- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/subjunctive_practice.git
cd subjunctive_practice
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. Run the application:
```bash
python main.py
```

## Usage

### Basic Practice
1. Select subjunctive triggers (wishes, emotions, doubt, etc.)
2. Choose tenses to practice
3. Select persons (yo, tú, él/ella, etc.)
4. Choose practice type:
   - **Traditional Grammar**: Classic exercises
   - **TBLT Scenarios**: Real-world tasks
   - **Mood Contrast**: Indicative vs subjunctive
   - **Review Mode**: Practice missed questions
5. Click "New Exercises" to generate practice
6. Answer using free response or multiple choice
7. Get instant contextual feedback

### Keyboard Shortcuts
- `Enter` - Submit answer
- `←/→` - Navigate exercises
- `H` - Get hint
- `Ctrl+R` - Conjugation reference

### Progress Tracking
- Save/load sessions for continuity
- Review mistakes automatically
- Daily streak tracking with motivational messages
- Smart error analysis with personalized suggestions
- Adaptive difficulty based on performance
- Achievement system and practice goals
- Export detailed analytics to CSV

## Building Executable

To create a standalone executable:

```bash
python build.py
```

The executable will be created in the `dist/` folder.

## License

MIT License - see pyproject.toml for details