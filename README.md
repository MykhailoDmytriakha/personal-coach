# Personal Coach

Personal Coach is an AI-powered mobile application designed to assist users in personal development, project management, financial planning, communication skills improvement, and spiritual growth through a prayer diary feature.

## Features

- **AI-powered Coaching**: Utilizes AI agents for personalized recommendations and adaptive notifications.
- **Thought Diary**: Record and analyze your thoughts and ideas.
- **Project Management**: Manage tasks and projects with integration to Google Calendar and Microsoft OneNote.
- **Financial Planning**: Track personal finances and financial projects.
- **Communication Skills**: Improve social interaction and communication abilities.
- **Prayer Diary**: Maintain a spiritual journal for reflections and prayer requests.
- **Voice Input**: Record your thoughts using voice input with automatic transcription.
- **Task Extraction**: Automatically extract tasks from your diary entries.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/personal-coach.git
   cd personal-coach
   ```

2. Create a virtual environment:
   ```
   python3 -m venv .venv
   ```

3. Activate the virtual environment:
   - On Linux/macOS:
     ```
     source .venv/bin/activate
     ```
   - On Windows:
     ```
     .venv\Scripts\activate
     ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_GPT_MODEL=gpt-4
   OPENAI_GPT_MODEL_SMALL=gpt-4-mini
   OPENAI_WHISPER_MODEL=whisper-1
   DEBUG_MODE=False
   DEFAULT_LANGUAGE=en
   ```

### Running the Application

To start the Personal Coach application, run:

```
python main.py
```

## Usage

1. **Recording Thoughts**: Click the "Start Recording" button to begin voice input. Click "Stop Recording" when finished.
2. **Viewing Transcriptions**: Transcribed text will appear in the Chat tab.
3. **AI Responses**: The AI will provide responses and suggestions based on your input.
4. **Task Management**: Extracted tasks will appear in the Tasks tab.
5. **Diary Entries**: View your diary entries in the Diary Entries tab.
6. **Settings**: Click the gear icon to access language settings.

## Project Structure

- `src/`: Source code directory
  - `ai/`: AI-related modules (chat, task extraction)
  - `audio/`: Audio recording and transcription
  - `data/`: Data management (diary entries, user profile)
  - `ui/`: User interface components
  - `utils/`: Utility functions and configuration
- `main.py`: Application entry point
- `requirements.txt`: List of Python dependencies

## Contributing

Contributions to the Personal Coach project are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the GPT and Whisper models
- The Python community for the excellent libraries used in this project