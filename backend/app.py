from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import random
import torch
from sentence_transformers import SentenceTransformer, util
import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import re
import unicodedata

app = FastAPI(title="Chatbot UNSTA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = SentenceTransformer("all-MiniLM-L6-v2")
executor = ThreadPoolExecutor(max_workers=2)

def load_json(filename):
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, "faq_data", filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

faq_data = load_json("data.json")
intent_data = load_json("intents.json")
extras_data = load_json("extras.json")

EMBEDDINGS_FILE = "intent_embeddings.pt"
if os.path.exists(EMBEDDINGS_FILE):
    intent_embeddings = torch.load(EMBEDDINGS_FILE)
else:
    intent_embeddings = {
        intent: MODEL.encode(samples, convert_to_tensor=True)
        for intent, samples in intent_data.items()
    }
    torch.save(intent_embeddings, EMBEDDINGS_FILE)

user_keywords_history = {}

async def encode_async(text):
    loop = asyncio.get_event_loop()
    func = partial(MODEL.encode, text, convert_to_tensor=True)
    return await loop.run_in_executor(executor, func)

async def find_best_intent(user_input: str):
    user_emb = await encode_async(user_input)
    best_intent = None
    best_score = 0.0

    for intent, emb_tensor in intent_embeddings.items():
        score = util.cos_sim(user_emb, emb_tensor).max().item()
        if score > best_score:
            best_score = score
            best_intent = intent

    return best_intent, best_score

def normalize_text(text: str) -> str:
    text = text.lower()
    text = ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_greetings_and_farewells(text):
    text_lower = text.lower()
    saludo = None
    despedida = None

    posibles_saludos = [s for s in extras_data.get("saludos", []) if s.lower().replace("¡", "").replace("!", "").strip() in text_lower]
    if posibles_saludos:
        saludo = random.choice(posibles_saludos)

    posibles_despedidas = [d for d in extras_data.get("despedidas", []) if d.lower().replace("¡", "").replace("!", "").strip() in text_lower]
    if posibles_despedidas:
        despedida = random.choice(posibles_despedidas)

    return saludo, despedida

def extract_keywords(text: str, max_words=5):
    # Extrae palabras clave simples (las primeras n no stopwords
    words = [w for w in text.split() if w not in ["el","la","los","las","de","del","y","en","su","sus","un","una"]]
    return words[:max_words]

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    query = data.get("query", "").strip()
    user_id = data.get("user_id", "anon")
    query_normalized = normalize_text(query)

    if not query:
        return {
            "greeting_text": None,
            "response_text": "Por favor, escribe una pregunta.",
            "farewell_text": None
        }

    greeting_text, farewell_text = extract_greetings_and_farewells(query_normalized)

    social_intents = ["agradecimiento", "despedida", "saludo"]
    social_info_intents = [
        "social_info_creacion",
        "social_info_funcionamiento",
        "social_habilidades"
    ]

    intent_detected, score = await find_best_intent(query_normalized)

    if intent_detected in social_intents and score > 0.7:
        respuesta = random.choice(extras_data.get(intent_detected + "s", ["¡Claro!"]))
        # Limpiar contexto (no académico)
        user_keywords_history[user_id] = []
        return {
            "greeting_text": greeting_text,
            "response_text": respuesta,
            "farewell_text": farewell_text,
            "confidence": score,
            "intent": intent_detected
        }

    # Caso 2: info sobre el bot (creación, funcionamiento, habilidades)
    if intent_detected in social_info_intents and score > 0.6:
        posibles_respuestas = faq_data.get(intent_detected, [])
        respuesta = random.choice(posibles_respuestas) if posibles_respuestas else (
            "Soy un asistente virtual diseñado para ayudarte con información sobre carreras e ingeniería."
        )
        # Limpiar contexto (no académico)
        user_keywords_history[user_id] = []
        return {
            "greeting_text": greeting_text,
            "response_text": respuesta,
            "farewell_text": farewell_text,
            "confidence": score,
            "intent": intent_detected
        }

    # Caso 3: académico (usa contexto)
    prev_keywords = user_keywords_history.get(user_id, [])
    context_query = " ".join(prev_keywords + [query_normalized])
    intent_acad, score_acad = await find_best_intent(context_query)

    if score_acad < 0.55:
        # No se entendió, pero no contaminar contexto
        return {
            "greeting_text": greeting_text,
            "response_text": "No entendí la pregunta, ¿podés reformularla?",
            "farewell_text": farewell_text,
            "confidence": score_acad
        }

    response_entry = faq_data.get(intent_acad, {})

    if isinstance(response_entry, list):
        response_text = random.choice(response_entry)
    elif isinstance(response_entry, dict):
        response_text = (
            response_entry.get("long")
            or response_entry.get("short")
            or "No hay información disponible."
        )
    else:
        response_text = str(response_entry)

    entrada = random.choice(extras_data.get("entradas", [""]))
    salida = random.choice(extras_data.get("salidas", [""]))
    respuesta = f"{entrada} {response_text} {salida}".strip()

    user_keywords_history[user_id] = extract_keywords(response_text)

    return {
        "greeting_text": greeting_text,
        "response_text": respuesta,
        "farewell_text": farewell_text,
        "confidence": score_acad,
        "intent": intent_acad
    }

