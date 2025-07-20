from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import google.generativeai as genai
from embed_store import EmbedStore

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

@app.post("/ask")
async def ask(request: Request):
    try:
        print("1. Starting ask endpoint")
        data = await request.json()
        question = data.get("question", "")
        print(f"2. Got question: {question}")
        
        if not question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        print("3. About to search embed_store")
        # retrieve relevant docs from faiss
        context_chunks = embed_store.search(question, top_k=5)
        print(f"4. Got {len(context_chunks)} context chunks")
        
        if not context_chunks:
            return {"answer": "I don't have enough context to answer that question. Please make sure the knowledge base is initialized."}
        
        print("5. Building context and prompt")
        context = "\n\n".join(context_chunks)

        # build prompt with context
        prompt = f"""answer the question based on the context below
        
        context: {context}
        question: {question}
        """

        print("6. Calling Gemini API")
        response = model.generate_content(prompt)  
        print("7. Got response from Gemini")
        return {"answer": response.text}
        
    except Exception as e:
        print(f"Error in ask endpoint: {str(e)}")
        import traceback
        traceback.print_exc()  # This will show the full stack trace
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/initialize")
async def initialize():
    """Initialize the knowledge base with scraped data"""
    try:
        from scrape import scrape_stripe_docs
        
        print("Scraping Stripe documentation...")
        chunks = scrape_stripe_docs()
        
        if not chunks:
            raise HTTPException(status_code=500, detail="Failed to scrape documentation")
        
        print(f"Adding {len(chunks)} chunks to embedding store...")
        embed_store.add_texts(chunks)
        
        return {"message": f"Knowledge base initialized with {len(chunks)} chunks"}
        
    except Exception as e:
        print(f"Error initializing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to initialize: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)