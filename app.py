
from flask import Flask, request, render_template_string
import string
import secrets

app = Flask(__name__)

SPECIAL_CHARS = "!@#$%&*?"


def get_strength_meter(password):
    score = 0

    if len(password) >= 12:
        score += 1
    if any(c.islower() for c in password) and any(c.isupper() for c in password):
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


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Free Password Generator | Custom Random Passwords</title>
    <meta name="description" content="Generate random passwords from 5 to 25 characters. Choose your password type, check password strength, and copy your password instantly.">
    <meta name="robots" content="index, follow">
    <meta name="theme-color" content="#0f172a">

    <meta name="google-site-verification" content="5iMg0IsWd16Ain6f7A1289I_mOG8PaDKDfBjyF7uig4" />

    <link rel="icon" type="image/svg+xml" href="/static/logo.svg">

    <style>
        * {
            box-sizing: border-box;
        }

        :root {
            color-scheme: dark;
            --background: #0f172a;
            --card: #1e293b;
            --text: #f8fafc;
            --muted: #94a3b8;
            --input: #0f172a;
            --border: #334155;
            --accent: #38bdf8;
            --button-text: #082f49;
            --track: #334155;
        }

        body.light {
            color-scheme: light;
            --background: #f1f5f9;
            --card: #ffffff;
            --text: #0f172a;
            --muted: #64748b;
            --input: #f8fafc;
            --border: #cbd5e1;
            --accent: #0284c7;
            --button-text: #ffffff;
            --track: #e2e8f0;
        }

        body {
            margin: 0;
            min-height: 100vh;
            padding: 18px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            background: var(--background);
            color: var(--text);
            transition: background 0.2s, color 0.2s;
        }

        .container {
            width: 100%;
            max-width: 414px;
            padding: 25px;
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 18px;
            display: flex;
            flex-direction: column;
            gap: 11px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
        }

        .top-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            width: 52px;
            height: 52px;
            object-fit: contain;
        }

        .theme-switch {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            color: var(--muted);
        }

        .switch {
            position: relative;
            display: inline-block;
            width: 42px;
            height: 24px;
            flex-shrink: 0;
        }

        .switch input {
            position: absolute;
            opacity: 0;
            width: 1px;
            height: 1px;
        }

        .switch-track {
            position: absolute;
            inset: 0;
            cursor: pointer;
            border-radius: 24px;
            background: #64748b;
            transition: 0.2s;
        }

        .switch-track::before {
            content: "";
            position: absolute;
            width: 18px;
            height: 18px;
            left: 3px;
            top: 3px;
            background: white;
            border-radius: 50%;
            transition: 0.2s;
        }

        .switch input:checked + .switch-track {
            background: var(--accent);
        }

        .switch input:checked + .switch-track::before {
            transform: translateX(18px);
        }

        .switch input:focus-visible + .switch-track {
            outline: 2px solid var(--accent);
            outline-offset: 3px;
        }

        h1 {
            font-size: 27px;
            text-align: center;
            margin: 0 0 5px;
        }

        form {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        label {
            font-size: 14px;
            font-weight: 600;
        }

        select,
        input[type="text"] {
            width: 100%;
            min-width: 0;
            padding: 10px;
            border: 1px solid var(--border);
            border-radius: 8px;
            background: var(--input);
            color: var(--text);
            font-size: 15px;
        }

        select {
            cursor: pointer;
        }

        .length-heading {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }

        #length-value {
            color: var(--accent);
            font-weight: bold;
            font-size: 16px;
        }

        input[type="range"] {
            width: 100%;
            margin: 5px 0 0;
            accent-color: var(--accent);
            cursor: pointer;
        }

        .range-labels {
            display: flex;
            justify-content: space-between;
            color: var(--muted);
            font-size: 12px;
            margin-top: -3px;
        }

        button {
            padding: 11px 13px;
            border: none;
            border-radius: 8px;
            background: var(--accent);
            color: var(--button-text);
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
            transition: opacity 0.2s, transform 0.1s;
        }

        button:hover {
            opacity: 0.85;
        }

        button:active {
            transform: scale(0.98);
        }

        .password-row {
            display: flex;
            align-items: stretch;
            gap: 7px;
        }

        .password-row input {
            flex: 1;
            font-family: Consolas, monospace;
            font-size: 14px;
        }

        .password-row button {
            padding: 10px 12px;
        }

        #copy-status {
            min-height: 0;
            margin: 4px 0 0;
            font-size: 12px;
            color: var(--muted);
        }

        .strength-section {
            margin-top: 3px;
        }

        .strength-heading {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            margin-bottom: 7px;
            font-size: 14px;
        }

        #strength-label {
            font-weight: bold;
            text-align: right;
        }

        .strength-track {
            height: 8px;
            width: 100%;
            background: var(--track);
            border-radius: 10px;
            overflow: hidden;
        }

        #strength-bar {
            height: 100%;
            width: 0%;
            border-radius: 10px;
            transition: width 0.25s;
        }

        .weak {
            color: #f87171;
        }

        #strength-bar.weak {
            background: #ef4444;
        }

        .medium {
            color: #fbbf24;
        }

        #strength-bar.medium {
            background: #f59e0b;
        }

        .strong {
            color: #4ade80;
        }

        #strength-bar.strong {
            background: #22c55e;
        }

        @media (max-height: 700px) {
            body {
                padding: 10px;
            }

            .container {
                padding: 18px;
                gap: 8px;
            }

            .logo {
                width: 44px;
                height: 44px;
            }

            h1 {
                font-size: 24px;
            }

            form {
                gap: 6px;
            }
        }

        @media (max-width: 360px) {
            .container {
                padding: 18px;
            }

            h1 {
                font-size: 23px;
            }
        }
    </style>
</head>

<body>
    <main class="container">
        <div class="top-row">
            <img class="logo" src="/static/logo.svg"
                 alt="Password Generator logo">

            <div class="theme-switch">
                <span id="theme-label">Dark mode</span>

                <label class="switch" aria-label="Toggle light or dark mode">
                    <input type="checkbox" id="theme-toggle">
                    <span class="switch-track"></span>
                </label>
            </div>
        </div>

        <h1>Free Password Generator</h1>

        <form method="post">
            <label for="strength">Password type</label>

            <select name="strength" id="strength">
                <option value="easy"
                    {% if strength == "easy" %}selected{% endif %}>
                    Easy
                </option>
                <option value="medium"
                    {% if strength == "medium" %}selected{% endif %}>
                    Medium
                </option>
                <option value="hard"
                    {% if strength == "hard" %}selected{% endif %}>
                    Hard
                </option>
            </select>

            <div class="length-heading">
                <label for="length">Password length</label>
                <span id="length-value">{{ length }}</span>
            </div>

            <input
                type="range"
                name="length"
                id="length"
                min="5"
                max="25"
                value="{{ length }}"
            >

            <div class="range-labels">
                <span>5 characters</span>
                <span>25 characters</span>
            </div>

            <button type="submit">Generate Password</button>
        </form>

        <div class="result">
            <label for="password-output">Your password</label>

            <div class="password-row">
                <input
                    id="password-output"
                    type="text"
                    value="{{ password }}"
                    readonly
                    autocomplete="off"
                >

                <button type="button" id="copy-button"
                        onclick="copyPassword()">Copy</button>
            </div>

            <p id="copy-status" aria-live="polite"></p>
        </div>

        <div class="strength-section">
            <div class="strength-heading">
                <span>Password strength</span>
                <span id="strength-label" class="{{ meter_class }}">
                    {{ meter_label }}
                </span>
            </div>

            <div class="strength-track">
                <div
                    id="strength-bar"
                    class="{{ meter_class }}"
                    style="width: {{ meter_width }}"
                ></div>
            </div>
        </div>
    </main>

    <script>
        const lengthSlider = document.getElementById("length");
        const lengthValue = document.getElementById("length-value");

        lengthSlider.addEventListener("input", function () {
            lengthValue.textContent = lengthSlider.value;
        });

        const themeToggle = document.getElementById("theme-toggle");
        const themeLabel = document.getElementById("theme-label");

        function setTheme(isLight) {
            document.body.classList.toggle("light", isLight);
            themeToggle.checked = isLight;
            themeLabel.textContent = isLight ? "Light mode" : "Dark mode";
        }

        try {
            const savedTheme = localStorage.getItem(
                "password-generator-theme"
            );
            setTheme(savedTheme === "light");
        } catch (error) {
            setTheme(false);
        }

        themeToggle.addEventListener("change", function () {
            const theme = themeToggle.checked ? "light" : "dark";
            setTheme(theme === "light");

            try {
                localStorage.setItem("password-generator-theme", theme);
            } catch (error) {
                // Theme switching still works if storage is unavailable.
            }
        });

        async function copyPassword() {
            const field = document.getElementById("password-output");
            const status = document.getElementById("copy-status");
            const button = document.getElementById("copy-button");

            if (!field.value) {
                status.textContent = "Generate a password first.";
                return;
            }

            try {
                await navigator.clipboard.writeText(field.value);
                status.textContent = "Password copied!";
                button.textContent = "Copied!";

                setTimeout(function () {
                    button.textContent = "Copy";
                    status.textContent = "";
                }, 2000);
            } catch (error) {
                field.select();
                status.textContent =
                    "Automatic copying failed. Press Ctrl+C to copy.";
            }
        }

        const password = document.getElementById("password-output").value;
        const label = document.getElementById("strength-label");
        const bar = document.getElementById("strength-bar");

        if (password) {
            let score = 0;

            if (password.length >= 12) score++;
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


@app.route("/", methods=["GET", "POST"])
def home():
    password = ""
    strength = "medium"
    length = 12

    if request.method == "POST":
        strength = request.form.get("strength", "medium")

        if strength not in ("easy", "medium", "hard"):
            strength = "medium"

        try:
            length = max(5, min(25, int(request.form.get("length", 12))))
        except (ValueError, TypeError):
            length = 12

        if strength == "easy":
            characters = string.ascii_lowercase
            password_chars = [
                secrets.choice(characters) for _ in range(length)
            ]

        elif strength == "medium":
            characters = string.ascii_letters + string.digits
            password_chars = [
                secrets.choice(string.ascii_uppercase),
                secrets.choice(string.ascii_lowercase),
                secrets.choice(string.digits)
            ]

            password_chars.extend(
                secrets.choice(characters) for _ in range(length - 3)
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
                secrets.choice(characters) for _ in range(length - 4)
            )

        secrets.SystemRandom().shuffle(password_chars)
        password = "".join(password_chars)

    meter_label = "Generate a password"
    meter_class = ""
    meter_width = "0%"

    if password:
        meter_label, meter_class, meter_width = get_strength_meter(password)

    return render_template_string(
        HTML,
        password=password,
        strength=strength,
        length=length,
        meter_label=meter_label,
        meter_class=meter_class,
        meter_width=meter_width
    )


if __name__ == "__main__":
    app.run(debug=True)
