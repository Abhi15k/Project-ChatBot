# PDF Chatbot

This project is a FastAPI application that provides a web interface for uploading PDF files, extracting text from PDFs, and performing question answering using OpenAI.

## Features

- Upload PDF files
- Extract text from uploaded PDFs
- Perform question answering related with pdf using OpenAI
- Real-time communication via WebSocket

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Abhi15k/Project-ChatBot.git
   cd Project-ChatBot
   ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:

    Create a .env file in the root directory.

    Add the following environment variables:
    ```bash
    OPENAI_API_KEY=your_openai_api_key
    ```
## Usage

1. Access the web interface:

    -Open your browser and go to http://localhost:8000.

2. Upload PDF files:

    -Click on the "Upload PDF" button and select a PDF file to upload.<br>
    -Note: It will take some little time to upload pdf so please wait..

3. Perform question answering:

    -Enter your question in the input box and click on the "Send" button.<br>
    -Note: It will take some little time to reply pdf so please wait..

4. Real-time communication:

    -Connect to the WebSocket endpoint at ws://localhost:8000/ws for real-time communication.

## API Endpoints

1. GET /: Render the web interface.
2. POST /upload-pdf/: Upload a PDF file and extract text.
3. POST /send-message/: Send a message for question answering.
4. WebSocket /ws: WebSocket endpoint for real-time communication.

## Project Structure

1. main.py: Main FastAPI application code.
2. templates/: Directory containing HTML templates.
3. static/: Directory containing static files (e.g., CSS, JavaScript).
4. requirements.txt: List of Python dependencies.
5. .gitignore: File specifying which files and directories to ignore in version control.
6. README.md: This file.

