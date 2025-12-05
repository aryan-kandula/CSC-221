# M7Pro Grader - Quick Start Guide 🚀

## 📁 Complete File List

Here are all the files you need (copy-paste ready):

### Python Files (Root Directory)
1. **app.py** - Main Flask application
2. **grader.py** - Grading logic and criteria
3. **functions.py** - Code analysis helper functions
4. **excel_export.py** - Excel file generation
5. **dictionary_api.py** - (Optional) External API for explanations

### Template Files (templates/ folder)
6. **base.html** - Base template with dark mode
7. **index.html** - Home page
8. **upload.html** - Upload interface
9. **results.html** - Results and analytics page

### Static Files (static/ folder)
10. **style.css** - Modern dark mode styling

### Configuration Files (Root Directory)
11. **requirements.txt** - Python dependencies
12. **create_venv.bat** - Virtual environment setup
13. **dependencies.bat** - Dependency installer
14. **launch.bat** - Easy application launcher
15. **build_exe.bat** - Executable builder

---

## ⚡ Super Quick Start (3 Steps)

### Step 1: Setup (One-Time)
```bash
create_venv.bat
```
This installs everything automatically!

### Step 2: Launch
```bash
launch.bat
```

### Step 3: Grade!
1. Go to **Upload & Grade**
2. Select a module
3. Upload your ZIP file
4. Get results!

---

## 🎨 Key Features

### Dark Mode Interface ✨
- Modern, professional design
- Easy on the eyes
- Color-coded grades (green = A, red = F)

### Smart Feedback 💬
- Emoji-enhanced messages
- Specific improvement suggestions
- Code snippets for reference
- Fun messages for `while True` detection!

### Visual Analytics 📊
- Summary statistics dashboard (6 stat cards)
- **TWO Dashboard Charts (as per wireframe):**
  1. Bar chart plotting criteria (average scores)
  2. Bar chart showing number and % of students with grade "1"
- Color-coded grade tables
- Excel file with results in one sheet and BOTH plots in another sheet

### Export Options 📥
- **CSV**: Simple spreadsheet with all grades
- **Excel**: Fancy spreadsheet with embedded charts

---

## 🧪 Testing Your Setup


**Last Updated**: December 5 2025 Aryan Kandula
**Version**: 1.0  
**Status**: Production Ready ✨