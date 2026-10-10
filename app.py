
from flask import Flask, request
import string
import secrets
import html

app = Flask(__name__)

SPECIAL_CHARS = "!@#$%&*?"


def get_strength_meter(password):
    score = 0

    if len(password) >= 8:
        score += 1

    if any(c.islower() for c in password) and any(
        c.isupper() for c in password
    ):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(c in SPECIAL_CHARS for c in password):
        score += 1

    if score == 0:
        return "Super weak", "weak", "10%"
    elif score == 1:
        return "Weak", "weak", "25%"
    elif score == 2:
        return "Normal", "medium", "45%"
    elif score == 3:
        return "Good", "medium", "70%"
    else:
        return "Very good", "strong", "100%"


@app.route("/", methods=["GET", "POST"])
def home():
    password = ""
    strength = "medium"
    length = 8

    if request.method == "POST":
        strength = request.form.get("strength", "medium")

        if strength not in ("easy", "medium", "hard"):
            strength = "medium"

        try:
            length = max(
                5, min(10, int(request.form.get("length", 8)))
            )
        except (ValueError, TypeError):
            length = 8

        if strength == "easy":
            characters = string.ascii_lowercase

            password_chars = [
                secrets.choice(characters)
                for _ in range(length)
            ]

        elif strength == "medium":
            characters = string.ascii_letters + string.digits

            password_chars = [
                secrets.choice(string.ascii_uppercase),
                secrets.choice(string.ascii_lowercase),
                secrets.choice(string.digits)
            ]

            password_chars.extend(
                secrets.choice(characters)
                for _ in range(length - 3)
            )

        else:
            characters = (
                string.ascii_letters
                + string.digits
                + SPECIAL_CHARS
            )

            password_chars = [
                secrets.choice(string.ascii_uppercase),
                secrets.choice(string.ascii_lowercase),
                secrets.choice(string.digits),
                secrets.choice(SPECIAL_CHARS)
            ]

            password_chars.extend(
                secrets.choice(characters)
                for _ in range(length - 4)
            )

        secrets.SystemRandom().shuffle(password_chars)
        password = "".join(password_chars)

    safe_password = html.escape(password, quote=True)

    if password:
        meter_label, meter_class, meter_width = (
            get_strength_meter(password)
        )
    else:
        meter_label = "Generate a password"
        meter_class = ""
        meter_width = "0%"

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Password Generator</title>
        <link rel="icon" type="image/svg+xml" href="/static/logo.svg">
        <link rel="stylesheet" href="/static/style.css">

        <style>
            body {
                padding: 12px;
            }

            .container {
                width: 100%;
                max-width: 360px;
                padding: 22px;
                gap: 10px;
            }

            .container img {
                width: 56px;
                height: auto;
            }

            h1 {
                font-size: 24px;
                margin: 4px 0 8px;
            }

            form {
                gap: 6px;
            }

            label {
                font-size: 13px;
                margin-bottom: 2px;
            }

            select,
            input {
                padding: 9px;
                font-size: 14px;
            }

            button {
                padding: 10px 12px;
                font-size: 14px;
            }

            .result {
                margin-top: 4px;
            }

            .password-row {
                gap: 6px;
            }

            #copy-status {
                min-height: 0;
                margin: 3px 0;
                font-size: 12px;
            }

            .strength-section {
                margin-top: 4px;
            }

            .strength-heading {
                font-size: 13px;
                margin-bottom: 6px;
            }

            .strength-track {
                height: 7px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <img src="/static/logo.svg" alt="Logo" width="56">
            <h1>Password Generator</h1>

            <form method="post">
                <label for="strength">Password strength</label>
                <select name="strength" id="strength">
                    <option value="easy" """ + (
                        'selected' if strength == 'easy' else ''
                    ) + """>Easy</option>
                    <option value="medium" """ + (
                        'selected' if strength == 'medium' else ''
                    ) + """>Medium</option>
                    <option value="hard" """ + (
                        'selected' if strength == 'hard' else ''
                    ) + """>Hard</option>
                </select>

                <label for="length">Password length (5–10)</label>
                <input type="number" name="length" id="length"
                       min="5" max="10" value=\"""" + str(length) + """\" required>

                <button type="submit">Generate Password</button>
            </form>

            <div class="result" id="result">
                <label for="password-output">Your password</label>
                <div class="password-row">
                    <input id="password-output" type="text"
                           value=\"""" + safe_password + """\"
                           readonly>
                    <button type="button" id="copy-button"
                            onclick="copyPassword()">Copy</button>
                </div>
                <p id="copy-status" aria-live="polite"></p>
            </div>

            <div class="strength-section" id="strength-meter">
                <div class="strength-heading">
                    <span>Password strength</span>
                    <span id="strength-label" class=\"""" + meter_class + """\">""" + meter_label + """</span>
                </div>
                <div class="strength-track">
                    <div id="strength-bar" class=\"""" + meter_class + """\"
                         style="width: """ + meter_width + """"></div>
                </div>
            </div>
        </div>

        <script>
            function copyPassword() {
                const field = document.getElementById("password-output");
                const status = document.getElementById("copy-status");
                const button = document.getElementById("copy-button");

                if (!field.value) {
                    status.textContent = "Generate a password first.";
                    return;
                }

                navigator.clipboard.writeText(field.value)
                    .then(() => {
                        status.textContent = "Password copied!";
                        button.textContent = "Copied!";

                        setTimeout(() => {
                            button.textContent = "Copy";
                            status.textContent = "";
                        }, 2000);
                    })
                    .catch(() => {
                        field.select();
                        status.textContent =
                            "Automatic copying failed. Press Ctrl+C to copy.";
                    });
            }

            const password = document.getElementById("password-output").value;
            const label = document.getElementById("strength-label");
            const bar = document.getElementById("strength-bar");

            if (password) {
                let score = 0;

                if (password.length >= 8) score++;
                if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
                if (/[0-9]/.test(password)) score++;
                if (/[^a-zA-Z0-9]/.test(password)) score++;

                let level, cssClass, width;

                if (score === 0) {
                    level = "Super weak";
                    cssClass = "weak";
                    width = "10%";
                } else if (score === 1) {
                    level = "Weak";
                    cssClass = "weak";
                    width = "25%";
                } else if (score === 2) {
                    level = "Normal";
                    cssClass = "medium";
                    width = "45%";
                } else if (score === 3) {
                    level = "Good";
                    cssClass = "medium";
                    width = "70%";
                } else {
                    level = "Very good";
                    cssClass = "strong";
                    width = "100%";
                }

                label.textContent = level;
                label.className = cssClass;
                bar.className = cssClass;
                bar.style.width = width;
            }
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
