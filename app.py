from flask import Flask, render_template, request
import re
import math

app = Flask(__name__)

def calculate_strength(password):
    """Evaluates password and returns its strength score & feedback."""
    score = 0
    feedback = []

    # Check password composition
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Include numbers.")

    if re.search(r"[@$!%*?&]", password):
        score += 1
    else:
        feedback.append("Add special characters like @, $, !, %, *, ? or &.")

    # Calculate entropy for more realistic strength
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"[0-9]", password): charset += 10
    if re.search(r"[^a-zA-Z0-9]", password): charset += 32
    entropy = len(password) * math.log2(charset) if charset else 0

    # Determine strength
    if entropy < 28 or score <= 2:
        strength = "Weak"
        color = "red"
    elif entropy < 45 or score == 3:
        strength = "Moderate"
        color = "orange"
    else:
        strength = "Strong"
        color = "green"

    return strength, entropy, feedback, color

@app.route("/", methods=["GET", "POST"])
def index():
    strength = None
    entropy = 0
    feedback = []
    color = "gray"

    if request.method == "POST":
        password = request.form["password"]
        strength, entropy, feedback, color = calculate_strength(password)

    return render_template("index.html",
                           strength=strength,
                           entropy=round(entropy, 2),
                           feedback=feedback,
                           color=color)

if __name__ == "__main__":
    app.run(debug=True)
