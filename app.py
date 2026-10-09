from flask import Flask, request
import random
import string

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    password = ""

    if request.method == "POST":
        strength = request.form["strength"]
        length = int(request.form["length"])

        if strength == "easy":
            characters = string.ascii_lowercase
        elif strength == "medium":
            characters = string.ascii_letters + string.digits
        else:
            characters = string.ascii_letters + string.digits + "!@#$%"

        password = "".join(
            random.choice(characters) for _ in range(length)
        )

    return """
    <h1>My Password Generator</h1>
    <form method="post">
        <label>Password strength:</label>
        <select name="strength">
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
        </select>
        <br><br>
        <label>Characters (5-10):</label>
        <input type="number" name="length" min="5" max="10" value="8" required>
        <br><br>
        <button type="submit">Generate Password</button>
    </form>
    <h2>Password: """ + password + """</h2>
    """

if __name__ == "__main__":
    app.run(debug=True)