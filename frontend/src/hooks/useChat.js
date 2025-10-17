import { useState, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";

const API_URL = process.env.REACT_APP_API_URL;

export default function useChat() {
  const [userId, setUserId] = useState(() => {
    const existing = localStorage.getItem("chat_user_id");
    if (existing) return existing;
    const newId = uuidv4();
    localStorage.setItem("chat_user_id", newId);
    return newId;
  });

  const [messages, setMessages] = useState([
    { sender: "bot", text: "¡Hola! Soy tu asistente UNSTA 🤖 estoy aquí para resolver tus dudas" },
  ]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (userText) => {
    if (!userText.trim()) return;

    setMessages((prev) => [...prev, { sender: "user", text: userText }]);
    setLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userText, user_id: userId }),
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
