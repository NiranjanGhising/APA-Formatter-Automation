# APA 7th Edition Formatter

Transform messy academic documents into properly formatted APA 7th edition documents.

![APA Formatter](https://img.shields.io/badge/APA-7th%20Edition-blue)
![React](https://img.shields.io/badge/React-18-61dafb)
![Python](https://img.shields.io/badge/Python-FastAPI-009688)

## Features

- 📄 **Title Page Generation** - Proper APA title page with centered elements
- 📑 **5-Level Heading System** - Automatic heading reformatting
- 📝 **Citation Fixing** - In-text citation detection and correction
- 📚 **Reference Formatting** - Sort and format reference lists
- 📏 **Document Styling** - Double-spacing, Times New Roman 12pt, 1" margins
- 🤖 **AI Enhancement** - Optional AI-powered tone improvement (requires OpenAI key)

## Tech Stack

- **Frontend**: React + TypeScript + Vite + Tailwind CSS
- **Backend**: Python + FastAPI
- **Document Processing**: python-docx
- **AI**: OpenAI API (optional)

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- pip

### Installation

1. **Clone the repository**
   ```bash
   cd "APA Formatter"
   ```

2. **Set up the Python backend**
   ```bash
   cd server
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional, for AI features)
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

4. **Set up the React frontend**
   ```bash
   cd ../client
   npm install
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   cd server
   .\venv\Scripts\activate  # Windows
   uvicorn app.main:app --reload --port 8000
   ```

2. **Start the frontend** (in a new terminal)
   ```bash
   cd client
   npm run dev
   ```

3. **Open your browser** at http://localhost:5173

## Usage

1. **Upload** your .docx document
2. **Select** formatting options (title page, headings, citations, references)
3. **Click** "Format Document"
4. **Download** the formatted document

## APA 7th Edition Reference

### Document Format
- 1" margins on all sides
- Double-spaced throughout
- Times New Roman 12pt (or Calibri 11pt, Arial 11pt)
- 0.5" first-line paragraph indent

### Heading Levels
| Level | Format |
|-------|--------|
| 1 | Centered, Bold, Title Case |
| 2 | Flush Left, Bold, Title Case |
| 3 | Flush Left, Bold Italic, Title Case |
| 4 | Indented, Bold, Title Case, Period. |
| 5 | Indented, Bold Italic, Title Case, Period. |

### In-Text Citations
- Parenthetical: `(Smith, 2023)`
- With page: `(Smith, 2023, p. 15)`
- Narrative: `Smith (2023) states...`
- Multiple authors: `(Smith & Jones, 2023)`
- 3+ authors: `(Smith et al., 2023)`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload` | Upload a document |
| POST | `/api/format/{file_id}` | Format an uploaded document |
| GET | `/api/download/{output_id}` | Download formatted document |
| POST | `/api/analyze` | Analyze document without formatting |
| GET | `/api/ai-status` | Check AI enhancement availability |

## Project Structure

```
APA Formatter/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── App.tsx       # Main app
│   │   └── main.tsx      # Entry point
│   └── package.json
│
├── server/                 # Python backend
│   ├── app/
│   │   ├── main.py       # FastAPI app
│   │   ├── routers/      # API routes
│   │   ├── services/     # Business logic
│   │   └── models/       # Data models
│   └── requirements.txt
│
└── apa-formatter.agent.md  # AI agent definition
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for your academic work!

---

Built with ❤️ for students and researchers
