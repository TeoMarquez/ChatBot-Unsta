import { Box, Paper, Typography, Divider } from "@mui/material";
import ChatMessage from "../components/ChatMessage";
import MessageInput from "../components/MessageInput";
import useChat from "../hooks/useChat";

import patternBg from '../assets/pattern-background.jpg';

const ChatRoom = () => {
  const { messages, sendMessage, loading } = useChat();

  return (
    <Paper
      elevation={3}
      sx={{
        width: "100%",
        height: "95vh",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden", // evita scroll global
        borderRadius: 0,
        bgcolor: "#f5f5f5",

        backgroundImage: `
          linear-gradient(rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.6)),
          url(${patternBg})
        `,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "repeat",
      }}
    >
      {/* Contenedor de mensajes scrollable */}
      <Box
        sx={{
          flex: 1, // ocupa todo el espacio restante
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: 1,
          p: 2,
        }}
      >
        {messages.length === 0 && (
          <Typography
            variant="body2"
            color="text.secondary"
            align="center"
            sx={{ mt: 2 }}
          >
            ¡Bienvenido al chat! Escribe algo para comenzar.
          </Typography>
        )}

        {messages.map((msg, idx) => (
          <ChatMessage key={idx} sender={msg.sender} text={msg.text} />
        ))}
      </Box>

      <Divider />

      {/* Input siempre al final */}
      <Box
        sx={{
          flexShrink: 0,
          width: "97%", // ocupa todo el ancho
          display: "flex",
          p: 1,
        }}
      >
        {/* Envolver el input en un Box con flex para full width */}
        <Box sx={{ flex: 1 }}>
          <MessageInput onSend={sendMessage} loading={loading} />
        </Box>
      </Box>
    </Paper>
  );
};

export default ChatRoom;
