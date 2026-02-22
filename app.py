from flask import Flask, render_template, request
import sys
import io

app = Flask(__name__)

# 🔍 Smart beginner-friendly checker
def beginner_check(code):
    # Check brackets
    if code.count("(") != code.count(")"):
        return "It looks like you forgot to close a bracket ')'. Check your parentheses."

    # Check double quotes
    if code.count('"') % 2 != 0:
        return 'You forgot to close a double quote (").'

    # Check single quotes
    if code.count("'") % 2 != 0:
        return "You forgot to close a single quote (')."

    # Check colon for if/for/while/def
    lines = code.split("\n")
    for line in lines:
        if line.strip().startswith(("if ", "for ", "while ", "def ")) and not line.strip().endswith(":"):
            return "You forgot to add ':' at the end of your statement."

    return None


def explain_python_error(e):
    error_type = type(e).__name__

    if error_type == "NameError":
        return "You are using something that is not defined yet."

    elif error_type == "TypeError":
        return "You are mixing different types of data (like number + text)."

    elif error_type == "ZeroDivisionError":
        return "You cannot divide a number by zero."

    elif error_type == "IndentationError":
        return "Your spacing is not correct. Python needs proper alignment."

    else:
        return "There is a mistake in your code. Please check carefully."


@app.route("/", methods=["GET", "POST"])
def home():
    output = ""
    explanation = ""

    if request.method == "POST":
        user_code = request.form["code"]

        # First check simple beginner mistakes
        simple_problem = beginner_check(user_code)

        if simple_problem:
            explanation = simple_problem
        else:
            # Capture print output
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()

            try:
                exec(user_code)
                output = buffer.getvalue()
                if output == "":
                    output = "Code ran successfully!"
            except Exception as e:
                explanation = explain_python_error(e)
            finally:
                sys.stdout = old_stdout

    return render_template("index.html", output=output, explanation=explanation)


if __name__ == "__main__":
    app.run(debug=True)