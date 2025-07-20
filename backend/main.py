from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import google.generativeai as genai
from embed_store import EmbedStore
from tools import get_enabled_tools, get_tool_config
from typing import List, Optional

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev only
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

embed_store = EmbedStore.get_instance()

@app.get("/")
async def root():
    """Root endpoint to avoid 404 errors"""
    return {"message": "AI Dev Assistant API is running"}

@app.get("/tools")
async def get_available_tools():
    # get list of available tools
    tools = get_enabled_tools()
    return {"tools": {
        name: {
            "name": config.name,
            "type": config.tool_type.value,
            "enabled": config.enabled
        }
        for name, config in tools.items()
    }}

@app.post("/ask")
async def ask(request: Request):
    try:
        print("1. Starting ask endpoint")
        data = await request.json()
        question = data.get("question", "")
        tool_filter = data.get("tools", None)  # Optional: filter by specific tools
        print(f"2. Got question: {question}")
        
        if not question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        print("3. About to search embed_store")
        # Retrieve relevant docs from vector store - get more results for source tracking
        search_results = embed_store.search_with_metadata(question, top_k=5)
        print(f"4. Got {len(search_results)} context chunks")
        
        if not search_results:
            return {
                "answer": "I don't have enough context to answer that question. Please make sure the knowledge base is initialized with '/initialize' or '/initialize/{tool_name}'.",
                "sources": []
            }
        
        print("5. Building context and extracting sources")
        context_chunks = []
        sources = []
        
        for result in search_results:
            context_chunks.append(result['content'])
            
            # Extract source info from the content (assuming our scraper adds it)
            source_info = extract_source_info(result['content'])
            if source_info:
                sources.append(source_info)
        
        context = "\n\n".join(context_chunks)

        # Enhanced prompt that handles multiple tools
        prompt = f"""You are an AI assistant specializing in developer tools and frameworks. Answer the question based on the provided context from various documentation sources.

Context from documentation:
{context}

Question: {question}

Instructions:
- Provide accurate, practical answers based on the context
- If the answer involves code, include relevant examples
- Mention which tool/framework you're referencing when relevant
- If you need to reference multiple tools, organize your answer clearly
- Be concise but thorough
"""

        print("6. Calling Gemini API")
        response = model.generate_content(prompt)  
        print("7. Got response from Gemini")
        
        return {
            "answer": response.text,
            "sources": sources
        }
        
    except Exception as e:
        print(f"Error in ask endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def extract_source_info(content: str) -> dict:
    """Extract source information from scraped content"""
    lines = content.split('\n')
    source_info = {
        "tool": "Unknown",
        "title": "",
        "url": "",
        "snippet": ""
    }
    
    for i, line in enumerate(lines[:10]):  # Check first 10 lines for metadata
        if line.startswith("Source:"):
            # Extract tool name from "Source: Tool Name - Title"
            source_line = line.replace("Source:", "").strip()
            if " - " in source_line:
                tool_and_title = source_line.split(" - ", 1)
                source_info["tool"] = tool_and_title[0].strip()
                source_info["title"] = tool_and_title[1].strip()
            else:
                source_info["tool"] = source_line
                
        elif line.startswith("URL:"):
            source_info["url"] = line.replace("URL:", "").strip()
        elif i > 2 and line.strip() and not line.startswith(("Source:", "URL:")):
            # First substantial content line becomes the snippet
            source_info["snippet"] = line.strip()
            break
    
    return source_info if source_info["tool"] != "Unknown" else None

@app.post("/initialize")
async def initialize():
    """Initialize the knowledge base with all enabled tools"""
    try:
        from scrape import UniversalScraper
        
        print("Initializing scraper...")
        scraper = UniversalScraper()
        
        print("Scraping all documentation...")
        all_chunks = scraper.scrape_all_tools()  # This returns a flat list
        
        if not all_chunks:
            raise HTTPException(status_code=500, detail="Failed to scrape any documentation")
        
        print(f"Got {len(all_chunks)} total chunks from all tools")
        print(f"First chunk preview: {all_chunks[0][:100] if all_chunks else 'No chunks'}...")
        
        print(f"Adding {len(all_chunks)} chunks to embedding store...")
        embed_store.add_texts(all_chunks)
        
        return {"message": f"Knowledge base initialized with {len(all_chunks)} chunks from all tools"}
        
    except Exception as e:
        print(f"Error initializing: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to initialize: {str(e)}")

@app.post("/initialize/{tool_name}")
async def initialize_tool(tool_name: str):
    """Initialize the knowledge base with a specific tool"""
    try:
        from scrape import UniversalScraper
        
        print(f"Initializing scraper for {tool_name}...")
        scraper = UniversalScraper()
        
        # Check if tool exists
        available_tools = list(get_enabled_tools().keys())
        if tool_name not in available_tools:
            raise HTTPException(
                status_code=400, 
                detail=f"Tool '{tool_name}' not found. Available tools: {', '.join(available_tools)}"
            )
        
        print(f"Scraping {tool_name} documentation...")
        chunks = scraper.scrape_tool(tool_name)
        
        if not chunks:
            raise HTTPException(status_code=500, detail=f"Failed to scrape {tool_name} documentation - no content found")
        
        print(f"Adding {len(chunks)} chunks from {tool_name} to embedding store...")
        embed_store.add_texts(chunks)
        
        return {"message": f"Knowledge base initialized with {len(chunks)} chunks from {tool_name}"}
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        print(f"Error initializing {tool_name}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to initialize {tool_name}: {str(e)}")

@app.get("/status")
async def get_status():
    """Get the current status of the knowledge base"""
    try:
        available_tools = list(get_enabled_tools().keys())
        return {
            "status": "running",
            "knowledge_base": "initialized" if embed_store else "not_initialized",
            "available_tools": available_tools,
            "available_endpoints": [
                "GET /tools - List available tools",
                "POST /initialize - Initialize all tools", 
                "POST /initialize/{tool_name} - Initialize specific tool",
                "POST /ask - Ask questions",
                "GET /status - Get API status"
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)