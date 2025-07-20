# 🧠 documind ai - intelligent documentation assistant

a powerful rag (retrieval-augmented generation) system that enables semantic search and intelligent question-answering over documentation using vector embeddings and ai.

## ✨ features

- **🔍 semantic search**: advanced vector-based search using sentence transformers
- **⚡ lightning fast**: optimized with faiss for sub-second search performance
- **🤖 ai-powered**: integrated with google gemini flash for intelligent responses
- **📚 documentation scraping**: automated web scraping for documentation ingestion
- **💾 persistent storage**: vector embeddings cached for instant retrieval
- **🎨 modern ui**: clean react frontend with tailwind css
- **🚀 production ready**: fastapi backend with cors support

## 🏗️ how it works

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   react frontend │    │  fastapi backend │    │  vector store   │
│                 │────│                  │────│                 │
│ • chat interface│    │ • rag pipeline   │    │ • faiss index   │
│ • tailwind css │    │ • gemini flash   │    │ • embeddings    │
│ • vite build    │    │ • cors enabled   │    │ • metadata      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 getting started

### what you'll need

- python 3.8+
- node.js 16+
- google api key (for gemini flash)

### 1. grab the code

```bash
git clone <your-repo-url>
cd ai-dev-assistant
```

### 2. setup the backend

```bash
cd backend

# create and activate virtual environment
python -m venv venv
source venv/bin/activate  # on windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# set up environment variables
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

### 3. setup the frontend

```bash
cd ../frontend

# install dependencies
npm install

# start development server
npm run dev
```

### 4. run everything

**backend** (terminal 1):

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**frontend** (terminal 2):

```bash
cd frontend
npm run dev
```

visit `http://localhost:5173` to see your app! 🎉

## 📁 what's inside

```
ai-dev-assistant/
├── backend/
│   ├── main.py              # fastapi application
│   ├── embed_store.py       # vector embedding store
│   ├── scrape.py           # documentation scraper
│   ├── requirements.txt    # python dependencies
│   ├── .env               # environment variables
│   ├── faiss.index        # vector index (generated)
│   └── faiss_meta.pkl     # metadata cache (generated)
├── frontend/
│   ├── src/
│   │   ├── components/    # react components
│   │   ├── lib/          # api utilities
│   │   ├── App.tsx       # main application
│   │   └── main.tsx      # entry point
│   ├── public/           # static assets
│   ├── package.json      # node dependencies
│   └── tailwind.config.js # tailwind configuration
└── README.md             # this file
```

## ⚙️ configuration

### 4. Run the Application

**Backend** (Terminal 1):

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Frontend** (Terminal 2):

```bash
cd frontend
npm run dev
```

Visit `http://localhost:5173` to access the application!

## 📁 Project Structure

```
ai-dev-assistant/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── embed_store.py       # Vector embedding store
│   ├── scrape.py           # Documentation scraper
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Environment variables
│   ├── faiss.index        # Vector index (generated)
│   └── faiss_meta.pkl     # Metadata cache (generated)
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── lib/          # API utilities
│   │   ├── App.tsx       # Main application
│   │   └── main.tsx      # Entry point
│   ├── public/           # Static assets
│   ├── package.json      # Node dependencies
│   └── tailwind.config.js # Tailwind configuration
└── README.md             # This file
```

## 🔧 configuration

### backend environment

create a `.env` file in the `backend/` directory:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### customizing the vector store

edit `embed_store.py` to modify:

- **model**: change `paraphrase-MiniLM-L3-v2` to other sentence transformers
- **dimensions**: adjust `dim=384` based on your model
- **index type**: switch from `IndexFlatL2` to other faiss indices

### adding your own docs

use the scraper or add documents manually:

```python
from embed_store import EmbedStore

store = EmbedStore()
documents = ["your documentation content here..."]
store.add_texts(documents)
```

## 🔌 api stuff

### `POST /ask`

ask questions about the documentation.

**request:**

```json
{
  "question": "how do i authenticate with the api?"
}
```

**response:**

```json
{
  "answer": "based on the documentation, you can authenticate using..."
}
```

## ⚡ performance tweaks

## 🛠️ api endpoints

### `POST /ask`

Ask questions about the documentation.

**request:**

```json
{
  "question": "How do I authenticate with the API?"
}
```

**response:**

```json
{
  "answer": "Based on the documentation, you can authenticate using..."
}
```

## 🎯 performance optimizations

### vector store optimizations

- **query caching**: repeated queries are cached for instant results
- **fast model**: uses `paraphrase-MiniLM-L3-v2` for optimal speed/accuracy balance
- **efficient storage**: faiss provides sub-millisecond search times

### frontend optimizations

- **vite build**: lightning-fast development and build times
- **tailwind css**: optimized css with tree-shaking
- **component lazy loading**: efficient react component loading

## 🧪 development

### adding cool stuff

1. **backend**: add endpoints in `main.py`
2. **frontend**: create components in `src/components/`
3. **vector store**: extend `embed_store.py` for new functionality

### testing things out

```bash
cd backend
python embed_store.py  # test vector store
python scrape.py       # test documentation scraping
```

### development commands

```bash
# backend development
cd backend && uvicorn main:app --reload

# frontend development
cd frontend && npm run dev

# build for production
cd frontend && npm run build
```

## �️ tech stack

### Backend

- **FastAPI**: Modern, fast web framework
- **FAISS**: Vector similarity search
- **Sentence Transformers**: Text embeddings
- **Google Gemini**: Language model integration
- **BeautifulSoup**: Web scraping

### Frontend

- **React 19**: UI framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first styling
- **Vite**: Build tool and dev server
- **Lucide React**: Icon library

## 🚀 Deployment

### backend Deployment

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### frontend Deployment

```bash
# Build for production
npm run build

# Serve the dist/ folder with any static hosting service
```
