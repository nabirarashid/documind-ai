# 🧠 documind ai - intelligent documentation assistant

a powerful rag (retrieval-augmented generation) system that enables semantic search and intelligent question-answering across multiple developer tool documentations using vector embeddings and ai.

## ✨ features

- **🔍 multi-source search**: semantic search across stripe, react, next.js, tailwind css, and vercel docs
- **⚡ lightning fast**: optimized with chromadb for sub-second search performance  
- **🤖 ai-powered**: integrated with google gemini flash for intelligent responses
- **📚 source attribution**: shows relevant documentation sources for each answer
- **💾 persistent storage**: vector embeddings cached with chromadb for instant retrieval
- **🎨 modern ui**: clean react frontend with tailwind css
- **🚀 production ready**: fastapi backend with cors support
- **🛠️ developer focused**: covers payment apis, ui frameworks, deployment, and styling

## 🏗️ how it works

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   react frontend │    │  fastapi backend │    │   chromadb      │
│                 │────│                  │────│                 │
│ • chat interface│    │ • rag pipeline   │    │ • vector store  │
│ • tailwind css │    │ • gemini flash   │    │ • embeddings    │
│ • vite build    │    │ • cors enabled   │    │ • persistence   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📚 supported documentation

- **💳 stripe**: payment apis, checkout, billing, connect
- **⚛️ react**: components, hooks, state management, routing  
- **🔗 next.js**: app router, pages, api routes, deployment
- **🎨 tailwind css**: utility classes, responsive design, dark mode
- **☁️ vercel**: deployment, functions, storage, cli

## 🚀 getting started

### what you'll need

- python 3.8+
- node.js 16+
- google api key (for gemini flash)

### 1. grab the code

```bash
git clone https://github.com/nabirarashid/ai-dev-tool.git
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
```

### 4. initialize the documentation

```bash
# start the backend first
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# in another terminal, initialize docs (this will scrape all enabled documentation)
curl -X POST http://localhost:8000/initialize
```

### 5. run the frontend

```bash
cd frontend
npm run dev
```

visit `http://localhost:5173` to start asking questions! 🎉

## 📁 what's inside

```
ai-dev-assistant/
├── backend/
│   ├── main.py              # fastapi application with rag endpoints
│   ├── embed_store.py       # chromadb vector store wrapper  
│   ├── tools.py            # documentation source configurations
│   ├── scrape.py           # multi-source documentation scraper
│   ├── requirements.txt    # python dependencies
│   ├── .env               # environment variables
│   └── chroma_store/      # persistent chromadb storage (generated)
├── frontend/
│   ├── src/
│   │   ├── components/    # react components (chat, messages, sources)
│   │   ├── App.tsx       # main application
│   │   └── main.tsx      # entry point
│   ├── package.json      # node dependencies
│   ├── postcss.config.js # tailwind configuration
│   └── tailwind.config.js # tailwind styling
└── README.md             # this file
```

## 🔧 configuration

### backend environment

create a `.env` file in the `backend/` directory:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### adding new documentation sources

edit `tools.py` to add new documentation sources:

```python
"your_tool": ToolConfig(
    name="Your Tool",
    tool_type=ToolType.YOUR_CATEGORY,
    base_url="https://your-tool.com/docs",
    scrape_paths=["/api", "/guides"],
    selectors={"content": "article", "title": "h1"}
)
```

### customizing the vector store

the project uses chromadb with sentence transformers (`all-MiniLM-L6-v2`). you can modify `embed_store.py` to:

- change the embedding model
- adjust similarity thresholds  
- modify collection settings

## �️ api endpoints

### `POST /ask`

ask questions about any of the supported documentation sources.

**request:**
```json
{
  "question": "how do i setup stripe checkout with react?"
}
```

**response:**
```json
{
  "answer": "based on the documentation, you can set up stripe checkout...",
  "sources": [
    {
      "title": "Stripe Checkout Guide",
      "url": "https://stripe.com/docs/checkout"
    }
  ]
}
```

### `POST /initialize`

scrape and index all enabled documentation sources.

**response:**
```json
{
  "message": "successfully initialized with X documents"
}
```

## 🎯 performance optimizations

### vector store optimizations

- **chromadb persistence**: automatic disk persistence for embeddings
- **sentence transformers**: optimized `all-MiniLM-L6-v2` model for speed/accuracy balance
- **efficient retrieval**: chromadb's optimized similarity search

### frontend optimizations

- **vite build**: lightning-fast development and build times
- **tailwind css**: optimized css with tree-shaking
- **component architecture**: efficient react component loading

## 🧪 development

### adding new features

1. **backend**: add endpoints in `main.py`
2. **frontend**: create components in `src/components/`  
3. **documentation sources**: extend `tools.py` with new configs

### testing the setup

```bash
# test the vector store
cd backend && python embed_store.py

# test documentation scraping  
cd backend && python scrape.py

# test specific tool scraping
cd backend && python -c "from scrape import scrape_react_docs; print(len(scrape_react_docs()))"
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

## 🔧 tech stack

### backend

- **fastapi**: modern, fast web framework
- **chromadb**: vector database for embeddings
- **sentence transformers**: text embeddings (`all-MiniLM-L6-v2`)
- **google gemini**: language model integration
- **beautifulsoup**: web scraping

### frontend

- **react 18**: ui framework  
- **typescript**: type safety
- **tailwind css**: utility-first styling
- **vite**: build tool and dev server
- **lucide react**: icon library

## 🚀 deployment

### backend deployment

```bash
# install production dependencies
pip install gunicorn

# run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### frontend deployment

```bash
# build for production
npm run build

# serve the dist/ folder with any static hosting service
```

## 💡 example queries

- "how do i create a stripe payment intent?"
- "what's the difference between app router and pages router in next.js?"
- "how do i make a responsive grid with tailwind?"
- "how do i deploy a react app to vercel?"
- "what are react hooks and how do i use usestate?"

---

built with ❤️ for developers who love good documentation
