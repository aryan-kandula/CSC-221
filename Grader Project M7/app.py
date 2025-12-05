import matplotlib
matplotlib.use("Agg")   # 🔥 CRITICAL FIX for Flask + EXE + headless mode

import os, zipfile, shutil, sys
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import pandas as pd
import requests
import base64
from io import BytesIO
import matplotlib.pyplot as plt

from grader import grade_folder, CRITERIA_MAP, get_local_explanation
from excel_export import make_excel_from_df

app = Flask(__name__)
app.secret_key = "m7pro-flask-secret-2025"

# 🔥 FIX FOR EXE: Use user's home directory instead of temp folder
if getattr(sys, 'frozen', False):
    # Running as EXE - use a permanent location
    UPLOAD_DIR = Path.home() / "M7Pro_Grader_Data" / "uploads"
else:
    # Running as Python script - use local folder
    UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

DICT_API_URL = "http://127.0.0.1:8000/explain/"

# Module display names
MODULE_NAMES = {
    "M1": "M1 - Input Output",
    "M2": "M2 - Collections (List, Dictionaries)",
    "M3": "M3 - Decision Structures",
    "M4": "M4 - Loops",
    "M5": "M5 - Functions"
}


def try_explain(criterion):
    """Try external API → fallback to local explanation."""
    try:
        r = requests.get(DICT_API_URL + criterion, timeout=1.2)
        if r.status_code == 200:
            return r.json()["explanation"]
    except:
        pass
    return get_local_explanation(criterion)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        module = request.form.get("module")
        sol = request.files.get("solution_file")
        zip_file = request.files.get("submissions_zip")

        if module not in CRITERIA_MAP:
            flash("❌ Invalid module selection")
            return redirect(request.url)

        if not zip_file:
            flash("📁 Please upload a submissions ZIP file")
            return redirect(request.url)

        # Save solution (optional)
        solution_path = None
        if sol and sol.filename:
            solution_path = UPLOAD_DIR / f"solution{Path(sol.filename).suffix}"
            sol.save(solution_path)

        # Save ZIP
        zip_path = UPLOAD_DIR / "submissions.zip"
        zip_file.save(zip_path)

        # Extract ZIP
        extract_dir = UPLOAD_DIR / "extracted"
        if extract_dir.exists():
            shutil.rmtree(extract_dir)
        extract_dir.mkdir()

        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_dir)

        flash(f"✅ Successfully uploaded and extracted files for {MODULE_NAMES[module]}")
        return redirect(url_for("results", module=module))

    return render_template("upload.html", modules=CRITERIA_MAP.keys(), module_names=MODULE_NAMES)


@app.route("/results")
def results():
    module = request.args.get("module")
    criteria = CRITERIA_MAP[module]

    extract_dir = UPLOAD_DIR / "extracted"
    df, feedback = grade_folder(str(extract_dir), criteria)

    # Add explanation text
    for fb in feedback:
        for crit in criteria.keys():
            if crit not in fb["feedback"]:
                fb["feedback"][crit] = try_explain(crit)

    # === Create CSV + Excel ===
    csv_filename = f"M7Pro_{module}_grades.csv"
    excel_filename = f"M7Pro_{module}_grades.xlsx"

    df.to_csv(UPLOAD_DIR / csv_filename, index=False)
    excel_bytes = make_excel_from_df(df, module, feedback)
    with open(UPLOAD_DIR / excel_filename, "wb") as f:
        f.write(excel_bytes)

    # ========== Matplotlib Charts (Base64 Embedded) ==========
    crit_cols = [c for c in df.columns if c not in ["file", "total_grade"]]

    plt.style.use('seaborn-v0_8-darkgrid')
    
    # 1 – CHART 1: Bar chart plotting criteria (average scores)
    plot_criteria = None
    if crit_cols:
        img = BytesIO()
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336']
        df[crit_cols].mean().plot(kind="bar", color=colors[:len(crit_cols)], ax=ax, edgecolor='black', linewidth=1.2)
        ax.set_title("Average Score by Criteria", fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel("Weighted Score (0–100)", fontsize=12)
        ax.set_xlabel("Criteria", fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(img, format="png", dpi=100, facecolor='white')
        plt.close()
        img.seek(0)
        plot_criteria = base64.b64encode(img.getvalue()).decode()

    # 2 – CHART 2: Bar chart showing students with grade 1 vs other grades
    grade_1_count = (df["total_grade"] == 1).sum()
    other_count = len(df) - grade_1_count
    total_students = len(df)
    
    grade_1_pct = (grade_1_count / total_students * 100) if total_students > 0 else 0
    other_pct = (other_count / total_students * 100) if total_students > 0 else 0
    
    img2 = BytesIO()
    fig, ax = plt.subplots(figsize=(10, 5))
    categories = ['Grade = 1\n(Failed)', 'Other Grades\n(Passed)']
    counts = [grade_1_count, other_count]
    colors_bar = ['#ef4444', '#10b981']
    
    bars = ax.bar(categories, counts, color=colors_bar, edgecolor='black', linewidth=1.2, alpha=0.8)
    
    # Add count and percentage labels on bars
    for bar, count, pct in zip(bars, counts, [grade_1_pct, other_pct]):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{count} students\n({pct:.1f}%)',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_title("Students with Grade 1 vs Other Grades", fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel("Number of Students", fontsize=12)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(img2, format="png", dpi=100, facecolor='white')
    plt.close()
    img2.seek(0)
    plot_grade1 = base64.b64encode(img2.getvalue()).decode()

    # 3 - Summary Statistics
    stats = {
        'total_submissions': len(df),
        'average_grade': round(df['total_grade'].mean(), 2),
        'highest_grade': round(df['total_grade'].max(), 2),
        'lowest_grade': round(df['total_grade'].min(), 2),
        'passing_rate': round((df['total_grade'] >= 70).sum() / len(df) * 100, 1) if len(df) > 0 else 0,
        'grade_1_count': grade_1_count  # Add this for the stat card
    }

    return render_template(
        "results.html",
        module=module,
        module_name=MODULE_NAMES[module],
        df=df,
        feedback=feedback,
        csv_filename=csv_filename,
        excel_filename=excel_filename,
        plot_criteria=plot_criteria,  # FIXED: was plot_avg
        plot_grade1=plot_grade1,      # FIXED: was plot_hist
        stats=stats
    )


@app.route("/download/<filename>")
def download(filename):
    path = UPLOAD_DIR / filename
    if not path.exists():
        flash("❌ File not found")
        return redirect(url_for("index"))
    return send_file(path, as_attachment=True)


@app.route("/shutdown", methods=["POST"])
def shutdown():
    """Gracefully shutdown the Flask server"""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        # For production servers, we need a different approach
        import os
        import signal
        os.kill(os.getpid(), signal.SIGINT)
    else:
        func()
    return "Server shutting down..."


if __name__ == "__main__":
    app.run(debug=True)