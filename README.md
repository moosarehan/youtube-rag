# YouTube RAG Chat Application

A Retrieval-Augmented Generation (RAG) application that allows users to chat with YouTube videos by extracting transcripts and using AI to answer questions based on the video content.

## 🎯 Features

- **YouTube Video Ingestion**: Extract transcripts from any YouTube video with available captions
- **Intelligent Q&A**: Ask questions about video content and get accurate, context-aware answers
- **Multi-language Support**: Works with videos in any language (not limited to English)
- **Persistent Storage**: Video data persists across server restarts using ChromaDB
- **Modern UI**: Clean, responsive interface built with Next.js and Tailwind CSS
- **Real-time Processing**: Fast retrieval and answer generation using advanced RAG techniques

## 🏗️ Architecture

### Tech Stack

#### Frontend
- **Framework**: Next.js 16.3.4 (React 19)
- **Styling**: Tailwind CSS
- **Language**: TypeScript
- **Build Tool**: Turbopack

#### Backend
- **Framework**: FastAPI (Python)
- **LLM**: Google Gemini 3.6 Flash
- **Vector Database**: ChromaDB
- **Embeddings**: HuggingFace Sentence Transformers
- **Orchestration**: LangChain

### RAG Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        INGESTION PHASE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  YouTube URL → Video ID Extraction → Transcript Fetch          │
│                                                                 │
│  ↓                                                              │
│                                                                 │
│  Document Loader (YouTube Transcript)                          │
│                                                                 │
│  ↓                                                              │
│                                                                 │
│  RecursiveCharacterTextSplitter                                │
│  - Chunk Size: 1000 characters                                 │
│  - Chunk Overlap: 200 characters                               │
│                                                                 │
│  ↓                                                              │
│                                                                 │
│  Embedding Generation (HuggingFace Sentence Transformers)      │
│                                                                 │
│  ↓                                                              │
│                                                                 │
│  ChromaDB Vector Store (Persistent Storage)                    │
│  - Session-based collections                                    │
│  - Metadata: video_id, title, timestamp, chunk_index           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        RETRIEVAL PHASE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Question → Embedding Generation                          │
│                                                                 │
│  ↓                                                              │
│                                                                 │
│  Vector Similarity Search (MMR Strategy)                       │
│  - Search Type: Maximal Marginal Relevance (MMR)              │
│  - Lambda: 0.5 (balance relevance & diversity)                │
│  - K: 4 documents                                              │
│                                                                 │
│  ↓                                                              │
│                                                                 │
│  Retrieved Context Chunks                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      AUGMENTATION PHASE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  System Prompt + Context + Question → Gemini 3.6 Flash        │
│                                                                 │
│  Prompt Engineering:                                            │
│  - Grounded responses only from provided context               │
│  - Concise and accurate answers                                │
│  - "I don't know" if answer not in context                     │
│                                                                 │
│  ↓                                                              │
│                                                                 │
│  Generated Answer + Source Citations                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

- **Python**: 3.11+
- **Node.js**: 18.17+ or 20.10+
- **Google API Key**: For Gemini 3.6 Flash model
- **HuggingFace Account**: For embedding models (optional, uses public models)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/moosarehan/youtube-rag.git
cd youtube-rag
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Add your Google API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

## 🎮 Running the Application

### Start Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### Start Frontend Server

```bash
cd frontend
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## 💡 Usage

1. **Open the application** in your browser: `http://localhost:3000`

2. **Ingest a YouTube video**:
   - Paste a YouTube URL in the input field
   - Click "Ingest Video"
   - Wait for processing to complete
   - You'll receive a session ID

3. **Ask questions**:
   - Type your question in the chat input
   - Press Enter or click "Send"
   - Receive AI-generated answers based on video content
   - View source citations with timestamps

4. **Persistent sessions**:
   - Ingested videos are stored in `backend/chroma_store/`
   - Sessions persist across server restarts
   - Each video gets a unique session ID

## 📁 Project Structure

```
youtube-rag/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes_chat.py      # Chat endpoint
│   │   │   └── routes_ingest.py    # Video ingestion endpoint
│   │   ├── chains/
│   │   │   ├── ingestion_chain.py  # Video processing pipeline
│   │   │   ├── rag_chain.py        # RAG orchestration
│   │   │   ├── retrieval_chain.py  # Vector search logic
│   │   │   └── prompts.py          # LLM prompts
│   │   ├── services/
│   │   │   ├── youtube.py          # YouTube transcript fetching
│   │   │   └── vector_store.py     # ChromaDB operations
│   │   ├── config.py               # App configuration
│   │   └── main.py                 # FastAPI application
│   ├── tests/
│   │   └── test_video_parsing.py   # Unit tests
│   ├── chroma_store/               # Vector database storage
│   ├── requirements.txt            # Python dependencies
│   └── .env                        # Environment variables
│
├── frontend/
│   ├── src/
│   │   └── app/
│   │       ├── page.tsx            # Main chat UI
│   │       ├── layout.tsx          # App layout
│   │       ├── globals.css         # Global styles
│   │       └── favicon.ico         # App icon
│   ├── public/                     # Static assets
│   ├── package.json                # Node dependencies
│   ├── tsconfig.json               # TypeScript config
│   ├── next.config.ts              # Next.js config
│   ├── postcss.config.mjs          # PostCSS config
│   └── eslint.config.mjs           # ESLint config
│
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 🔧 Configuration

### Backend Configuration (`backend/app/config.py`)

```python
llm_provider: str = "google"              # LLM provider
llm_model: str = "gemini-3.6-flash"      # Model name
chroma_persist_directory: str             # Vector DB storage path
backend_cors_origins: str                 # Allowed CORS origins
```

### Environment Variables (`backend/.env`)

```env
GOOGLE_API_KEY=your_google_api_key_here
HUGGINGFACEHUB_API_TOKEN=your_hf_token_here  # Optional
```

## 🧠 RAG Components Explained

### 1. Document Loader
- **Purpose**: Fetches YouTube video transcripts
- **Library**: `youtube-transcript-api`
- **Features**: 
  - Supports multiple languages
  - Handles auto-generated captions
  - Extracts timestamps

### 2. Text Splitter
- **Type**: RecursiveCharacterTextSplitter
- **Chunk Size**: 1000 characters
- **Overlap**: 200 characters
- **Why**: Maintains context while creating manageable chunks for embedding

### 3. Embeddings
- **Model**: HuggingFace Sentence Transformers
- **Dimension**: 384 (default for all-MiniLM-L6-v2)
- **Purpose**: Convert text chunks into dense vector representations

### 4. Vector Store
- **Database**: ChromaDB
- **Storage**: Persistent on-disk storage
- **Collections**: One per video session
- **Metadata**: video_id, title, timestamp, chunk_index

### 5. Retriever
- **Strategy**: MMR (Maximal Marginal Relevance)
- **Lambda**: 0.5 (balances relevance and diversity)
- **K**: 4 documents retrieved per query
- **Why MMR**: Reduces redundancy in retrieved documents

### 6. LLM
- **Model**: Google Gemini 3.6 Flash
- **Provider**: LangChain Google GenAI
- **Prompt**: Grounded, context-aware system prompt
- **Output**: Structured answers with source citations

## 🔒 API Endpoints

### Health Check
```http
GET /api/health
```

### Ingest Video
```http
POST /api/ingest
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
```json
{
  "session_id": "unique_session_id",
  "video_id": "VIDEO_ID",
  "title": "Video Title",
  "chunk_count": 42
}
```

### Chat
```http
POST /api/chat
Content-Type: application/json

{
  "session_id": "session_id_from_ingest",
  "question": "What is this video about?",
  "history": []
}
```

**Response:**
```json
{
  "answer": "This video discusses...",
  "sources": [
    {
      "url": "https://youtube.com/watch?v=VIDEO_ID&t=123",
      "snippet": "Relevant transcript excerpt...",
      "title": "Video Title"
    }
  ]
}
```

## 🧪 Testing

```bash
cd backend
pytest tests/
```

## 📊 Performance Considerations

- **Embedding Generation**: ~2-3 seconds for average video
- **Query Response**: ~1-2 seconds per question
- **Memory Usage**: ~500MB base + ~50MB per ingested video
- **Storage**: ~1-2MB per video in ChromaDB

## 🛠️ Troubleshooting

### Backend won't start
- Ensure Python 3.11+ is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that `.env` file exists with valid `GOOGLE_API_KEY`

### Frontend build errors
- Delete `node_modules` and reinstall: `npm install`
- Clear Next.js cache: `rm -rf .next`

### Video ingestion fails
- Verify the video has captions/transcripts enabled
- Check if the video is public or unlisted (private videos won't work)
- Ensure YouTube URL format is correct

### "Session not found" error
- The session may have been deleted from `chroma_store/`
- Re-ingest the video to create a new session

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) - RAG orchestration
- [ChromaDB](https://github.com/chroma-core/chroma) - Vector database
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Next.js](https://nextjs.org/) - Frontend framework
- [Google Gemini](https://ai.google.dev/) - LLM provider
- [HuggingFace](https://huggingface.co/) - Embedding models

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

Made with ❤️ by [moosarehan](https://github.com/moosarehan)
