# Chatbot UNSTA

Chatbot UNSTA es una API de chatbot desarrollada con FastAPI y Sentence Transformers, diseñada para responder preguntas académicas de la Universidad del Norte Santo Tomás de Aquino (UNSTA) y manejar interacciones sociales (saludos, despedidas, agradecimientos, etc.).

## El chatbot combina:

- Embeddings de texto para detección de intención (sentence-transformers/all-MiniLM-L6-v2).
- Respuestas académicas basadas en FAQs.
- Historial de keywords por usuario para mejorar contexto.

## Características

- Respuestas a preguntas académicas sobre carreras, materias, campus, etc.
- Respuestas a saludos, despedidas y preguntas sociales.
- Soporte de embeddings precomputados para rendimiento.
- Compatible con requests asincrónicos.
- Middleware CORS 

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/TeoMarquez/chatbot-unsta.
cd chatbot-unsta/backend
```

Crear entorno virtual e instalar dependencias:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS
```

```bash
pip install -r requirements.txt
```

## Asegurarse de que los archivos JSON estén en backend/faq_data/:

- data.json
- intents.json
- extras.json

## Inicializar embeddings (se generan automáticamente al correr la app por primera vez):

```bash
python -m uvicorn app:app --reload
```

## Uso

Enviar POST requests al endpoint /chat con JSON:

```bash
{
  "query": "¿Qué materias tiene bioingeniería?",
  "user_id": "usuario123"
}
```

Ejemplo con curl:

```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d "{\"query\": \"hola\"}"
```

Respuesta de ejemplo:

```bash
{
  "greeting_text": "¡Hola! ¿Cómo estás?",
  "response_text": "¡Hola! Bienvenido al Chatbot UNSTA.",
  "farewell_text": null,
  "confidence": 0.75,
  "intent": "saludo"
}
```

## Estructura del proyecto
chatbot-unsta/
├─ backend/
│  ├─ app.py                  # Código principal de FastAPI
│  ├─ faq_data/
│  │  ├─ data.json            
│  │  ├─ intents.json         
│  │  ├─ extras.json           
│ 
├─ frontend/               
│  │  public/
│  │  ├─ index.html
│  │  src/
│  │  ├─ assets/
│  │  ├─ components/
│  │  ├─ hooks/
│  │  ├─ views/
│  │  app.tsx
│  │  index.js

## Notas importantes
La primera ejecución generará los embeddings lo que puede tardar algunos segundos.

El chatbot maneja saludos y despedidas, pero su texto se prioriza solo si hay coincidencia exacta en extras.json.

Se recomienda probar con distintas queries para validar el ranking de intents.
