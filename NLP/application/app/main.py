from fastapi import FastAPI
import PyPDF2
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")
index = None
chunk_list = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def read_pdf(file_bytes):
    text = ""
    reader = PyPDF2.PdfReader(file_bytes)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def build_vector_db(chunks):
    embeddings = model.encode(chunks)
    dim = embeddings.shape[1]
    idx = faiss.IndexFlatL2(dim)
    idx.add(np.array(embeddings))
    return idx, chunks

@app.post("/load_pdf/")
def load_pdf():
    global index, chunk_list
    with open('../data/data.pdf', "rb") as f:
        text = read_pdf(f)
    chunk_list = chunk_text(text)
    index, chunk_list = build_vector_db(chunk_list)
    return {"message": "Base vectorielle créée", "chunks": len(chunk_list)}

def search(query, top_k=5):
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), top_k)
    keywords = set(query.lower().split())
    filtered_chunks = []
    for i in I[0]:
        chunk = chunk_list[i]
        if any(word in chunk.lower() for word in keywords):
            filtered_chunks.append(chunk)
    return filtered_chunks if filtered_chunks else [chunk_list[i] for i in I[0]]


# ===== SOLUTION 1 : Ollama avec Qwen 2.5:3b (GRATUIT et LOCAL - RECOMMANDÉ) =====
import requests as req

def generate_with_ollama(context, query):
    """
    Utilise Ollama en local avec Qwen 2.5:3b - 100% gratuit
    Installation: 
    1. curl -fsSL https://ollama.com/install.sh | sh
    2. ollama pull qwen2.5:3b
    3. ollama serve
    """
    prompt = f"""Tu es un assistant pédagogique spécialisé dans le génie logiciel.

Contexte extrait du PDF :
{context}

Question : {query}

Instructions : Réponds de manière claire, précise et pédagogique en te basant UNIQUEMENT sur le contexte fourni. Si l'information n'est pas dans le contexte, dis-le clairement."""
    
    try:
        response = req.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:3b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 400  # Limite de tokens générés
                }
            },
            timeout=120  # 2 minutes max
        )
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"❌ Erreur Ollama (code {response.status_code}). Vérifiez qu'Ollama est bien lancé avec 'ollama serve'."
    except req.exceptions.ConnectionError:
        return "❌ Impossible de se connecter à Ollama. Assurez-vous qu'Ollama est installé et lancé avec 'ollama serve'."
    except req.exceptions.Timeout:
        return "⏱️ La requête a pris trop de temps. Le modèle traite peut-être une requête complexe."
    except Exception as e:
        return f"❌ Erreur inattendue : {str(e)}"


# ===== SOLUTION 2 : Utiliser T5 correctement =====
from transformers import T5Tokenizer, T5ForConditionalGeneration

t5_tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
t5_model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

def generate_with_t5(context, query):
    # T5 nécessite un format spécifique
    prompt = f"answer question: {query} context: {context}"
    
    inputs = t5_tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = t5_model.generate(
        inputs.input_ids,
        max_new_tokens=200,
        temperature=0.7,
        do_sample=True,
        top_p=0.9
    )
    answer = t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer


# ===== SOLUTION 3 : Utiliser un modèle français local =====
from transformers import pipeline

# Modèle francophone plus performant
generator_fr = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",  # ou "Helsinki-NLP/opus-mt-fr-en" pour français
    device_map="auto"
)

def generate_with_french_model(context, query):
    prompt = f"Contexte: {context}\n\nQuestion: {query}\n\nRéponse:"
    
    result = generator_fr(
        prompt,
        max_length=300,
        min_length=50,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        num_return_sequences=1
    )
    return result[0]["generated_text"]


# ===== SOLUTION 4 : Réponse simple basée sur extraction =====
def generate_simple_extraction(context, query):
    """
    Si vous n'avez pas d'API et que les modèles locaux ne fonctionnent pas bien,
    cette approche simple peut suffire temporairement
    """
    # Trouve les phrases les plus pertinentes
    sentences = context.split('.')
    relevant_sentences = []
    
    query_words = set(query.lower().split())
    for sentence in sentences:
        sentence_words = set(sentence.lower().split())
        # Compte les mots en commun
        overlap = len(query_words & sentence_words)
        if overlap >= 2:  # Au moins 2 mots en commun
            relevant_sentences.append(sentence.strip())
    
    if relevant_sentences:
        answer = ". ".join(relevant_sentences[:3]) + "."
        return f"D'après le document : {answer}"
    else:
        return "Je n'ai pas trouvé d'information pertinente dans le contexte fourni."


@app.post("/ask/")
async def ask(request: QueryRequest):
    relevant_chunks = search(request.query)
    context = "\n".join(relevant_chunks)
    
    # SOLUTION RECOMMANDÉE : Ollama (gratuit et local)
    answer = generate_with_ollama(context, request.query)
    
    return {"answer": answer}