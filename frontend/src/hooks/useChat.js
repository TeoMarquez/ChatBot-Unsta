import { useState } from "react";

const API_URL = process.env.REACT_APP_API_URL;

export default function useChat() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "¡Hola! Soy tu asistente UNSTA 🤖 estoy aquí para resolver tus dudas" },
  ]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (userText) => {
    if (!userText.trim()) return;

    const newUserMsg = { sender: "user", text: userText };
    setMessages((prev) => [...prev, newUserMsg]);
    setLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userText }),
      });

      const data = await res.json();
      const combined =
        `${data.greeting_text ?? ""} ${data.response_text ?? ""} ${data.farewell_text ?? ""}`.trim();

      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: combined || "No tengo respuesta 😅" },
      ]);
    } catch (error) {
      console.error("Error en el fetch:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Hubo un error al conectar con el servidor 😔" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return { messages, sendMessage, loading };
}
