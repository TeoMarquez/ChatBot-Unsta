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

# Inicialización FastAPI

app = FastAPI(title="Chatbot UNSTA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego limitar al dominio de React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de modelo y datos
MODEL = SentenceTransformer("all-MiniLM-L6-v2")
executor = ThreadPoolExecutor(max_workers=2)

def load_json(filename):
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, "faq_data", filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

faq_data = load_json("data.json")
intent_data = load_json("intents.json")
extras_data = load_json("extras.json")  # complementos humanos opcionales

# Embeddings precalculados de intents
    # Guardar embeddings en disco para acelerar reinicios
EMBEDDINGS_FILE = "intent_embeddings.pt"
if os.path.exists(EMBEDDINGS_FILE):
    intent_embeddings = torch.load(EMBEDDINGS_FILE)
else:
    intent_embeddings = {
        intent: MODEL.encode(samples, convert_to_tensor=True)
        for intent, samples in intent_data.items()
    }
    torch.save(intent_embeddings, EMBEDDINGS_FILE)

# Funciones de matching
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

# Función de detección de saludos y despedidas

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


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    query = data.get("query", "").strip()

    if not query:
        return {
            "greeting_text": None,
            "response_text": "Por favor, escribe una pregunta.",
            "farewell_text": None
        }

    greeting_text, farewell_text = extract_greetings_and_farewells(query)

    # Buscar intent principal
    intent, score = await find_best_intent(query)

    # --- INTENTS SOCIALES ---
    social_intents = ["agradecimiento", "despedida", "saludo"]

    # Si la confianza es baja y no es social, pedimos reformulación
    if score < 0.55 and intent not in social_intents:
        return {
            "greeting_text": greeting_text,
            "response_text": "No entendí la pregunta, ¿podés reformularla?",
            "farewell_text": farewell_text,
            "confidence": score
        }

    # Si es un intent social: respuesta simple y directa
    if intent in social_intents:
        respuesta = random.choice(extras_data.get(intent + "s", ["¡Claro!"]))
        return {
            "greeting_text": greeting_text,
            "response_text": respuesta,
            "farewell_text": farewell_text,
            "confidence": score,
            "intent": intent
        }

    # INTENTS ACADÉMICOS 
    response_entry = faq_data.get(intent, {})
    response_text = response_entry.get("long") or response_entry.get("short") or "No hay información disponible."

    # Concatenar entrada y salida solo en intents académicos
    entrada = random.choice(extras_data.get("entradas", [""]))
    salida = random.choice(extras_data.get("salidas", [""]))
    response_text = f"{entrada} {response_text} {salida}".strip()

    return {
        "greeting_text": greeting_text,
        "response_text": response_text,
        "farewell_text": farewell_text,
        "confidence": score,
        "intent": intent
    }
