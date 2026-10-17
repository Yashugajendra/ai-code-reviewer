# 🤖 AI Code Reviewer

AI-powered web application that reviews source code and provides
feedback on bugs, security concerns, performance, and coding best
practices. It uses Google's Gemini API to generate structured review
results and presents them in a simple web interface.

## Live Demo

**Try it here:** https://ai-code-reviewer-jw10.onrender.com

> The app is hosted on Render's free instance, so the first request
> after inactivity may take a little longer while the service starts.

## Features

-   **AI-powered code review** using the Gemini API.
-   **Multiple languages:** Python, Java, JavaScript, and C++.
-   **Quality rating** with an overall score out of 10 and a review
    summary.
-   **Categorized feedback:** bugs, security issues, performance, and
    best practices.
-   **Issue details** including severity, line references when
    available, explanations, and suggestions.
-   **Review history** for the current browser.
-   **Dashboard statistics** for review counts, average score, detected
    issues, and language usage.
-   **Report exports** in TXT, Markdown, and JSON formats.
-   **Dark/light theme** and a code editor with line numbers and syntax
    highlighting.
-   **Input validation and rate limiting** to help protect the review
    endpoint.

## Tech Stack

  Area                           Technologies
  ------------------------------ ------------------------------------
  Backend                        Python, Flask
  AI integration                 Google Gemini API (`google-genai`)
  Structured output validation   Pydantic
  Frontend                       HTML, CSS, JavaScript
  Database                       SQLite
  Request rate limiting          Flask-Limiter
  Production server              Gunicorn
  Deployment                     Render

## How It Works

1.  Choose a programming language and paste your code into the editor.
2.  The Flask backend validates the input and prepares a numbered-code
    prompt.
3.  The Gemini API generates a structured review.
4.  The application displays the score, summary, and categorized
    findings.
5.  The review can be revisited through browser-specific history or
    exported as TXT, Markdown, or JSON.

AI feedback is advisory. Always review suggestions and test any changes
before using them in production code.

## Run Locally

### 1. Clone the repository

``` bash
git clone https://github.com/Yashugajendra/ai-code-reviewer.git
cd ai-code-reviewer
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt instead:

``` bat
venv\Scripts\activate.bat
```

**macOS/Linux:**

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

``` bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and add your own Gemini API key. Keep
`.env` private and never commit it to GitHub.

Example `.env` format:

``` env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_working_gemini_model_name
```
**Security note:** Never hardcode your API key in source code or commit your `.env` file to GitHub. Keep your credentials private.

Use a valid model name available to your Google AI Studio API key. Do
not use the example placeholders as actual values.

### 5. Start the application

``` bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Run Tests

Run the project's unit tests with:

``` bash
python -m unittest test_app.py
```

## Deployment

The application is deployed on Render using the following commands:

**Build command**

``` bash
pip install -r requirements.txt
```

**Start command**

``` bash
gunicorn app:app
```

Configure these environment variables in the Render service dashboard:

-   `GEMINI_API_KEY` --- your Gemini API key.
-   `GEMINI_MODEL` --- the Gemini model name that works with your API
    key.
**Security note:** Never hardcode your API key in source code or commit your `.env` file to GitHub. Keep your credentials private.

Do not place API keys in source code or commit them to the repository.

## Notes and Limitations

-   The free Render web service spins down after inactivity, so the
    first request can be slower.
-   Review history is stored in SQLite. Render's free instance does not
    provide a persistent disk, so local database contents may be lost
    after restarts or redeployments.
-   AI-generated feedback can be incomplete or incorrect ; verify
    important findings manually.
-   API availability and usage are subject to Google's Gemini API limits
    and terms.

## Project Structure

``` text
ai-code-reviewer/
├── templates/
│   └── index.html
├── app.py
├── requirements.txt
├── Procfile
├── .env.example
├── .gitignore
├── test_app.py
└── README.md
```

## 👨‍💻 Author
                  
**Yashwanth G**

Live Demo: https://ai-code-reviewer-jw10.onrender.com

GitHub: https://github.com/Yashugajendra/ai-code-reviewer