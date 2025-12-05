# M7Pro Grader - CTI-110 Automated Assessment System

## 🎯 Project Overview

M7Pro Grader is a modern, automated grading tool designed for CTI-110 programming modules. It features:

- **Batch grading** of Python submissions
- **Visual analytics** with charts and statistics
- **Detailed feedback** for each grading criterion
- **Dark mode UI** for comfortable viewing
- **Export options** (CSV and Excel with embedded charts)

## 📋 Supported Modules

- **M1** - Input Output
- **M2** - Collections (List, Dictionaries)
- **M3** - Decision Structures
- **M4** - Loops
- **M5** - Functions

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this project**

2. **Run the setup script (Windows)**
   ```bash
   create_venv.bat
   ```

   This will:
   - Create a virtual environment
   - Install all dependencies
   - Set up the project

3. **Activate the virtual environment** (if not already activated)
   ```bash
   venv\Scripts\activate
   ```

4. **Run the Flask application**
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## 📦 Project Structure

```
M7Pro_Grader/
│
├── app.py                    # Main Flask application
├── grader.py                 # Grading logic and criteria
├── functions.py              # Helper functions for code analysis
├── excel_export.py           # Excel file generation
├── dictionary_api.py         # Optional API for explanations
│
├── templates/
│   ├── base.html            # Base template with dark mode
│   ├── index.html           # Home page
│   ├── upload.html          # Upload interface
│   └── results.html         # Results and analytics
│
├── static/
│   └── style.css            # Modern dark mode styling
│
├── uploads/                 # Temporary storage for uploads
├── requirements.txt         # Python dependencies
├── create_venv.bat         # Windows setup script
└── dependencies.bat        # Dependency installer
```

## 📝 Usage Instructions

### Preparing Submission Files

1. **Collect all student Python files** (.py files)
2. **Place them in a single folder**
3. **Create a ZIP archive** of that folder
4. **Optionally prepare a solution file** for reference

### Grading Process

1. **Launch the application**
2. **Navigate to "Upload & Grade"**
3. **Select the module** (M1-M5)
4. **Upload the solution file** (optional)
5. **Upload the submissions ZIP file**
6. **Click "Grade Submissions"**
7. **View results, charts, and feedback**
8. **Download CSV or Excel** with results

## 🎨 Features

### Grading Criteria

Each module has specific weighted criteria:

- **M1**: Input (30%), Output (50%), Pseudocode (10%), Variables (10%)
- **M2**: Input (10%), Output (30%), Collections (45%), Pseudocode (10%), Variables (5%)
- **M3**: Input (15%), Decisions (25%), Output (45%), Pseudocode (10%), Variables (5%)
- **M4**: Loops & Decisions (40%), Output (40%), Pseudocode (10%), Variables (10%)
- **M5**: Loops & Decisions (30%), Output (40%), Functions (15%), Pseudocode (10%), Variables (5%)

### Automatic Failure Conditions

- **Syntax errors** → Grade: 1
- **while True loops** → Grade: 1 (creative feedback message)
- Both receive specific feedback explaining the issue

### Visual Analytics

- **Summary statistics** (average, highest, lowest grades, passing rate)
- **Criteria bar chart** showing average scores
- **Grade distribution histogram**
- **Color-coded grade cells** in results table

### Feedback System

- **Per-criterion feedback** with emojis and clear messages
- **Code snippets** showing first 400 characters
- **Expandable details** for each submission
- **General feedback** for special cases (syntax errors, while True)


**Happy Grading! 🎓✨**