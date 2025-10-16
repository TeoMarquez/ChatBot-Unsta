import React, { useState } from "react";
import { TextField, Button, Box } from "@mui/material";

const MessageInput = ({ onSend, loading }) => {
  const [input, setInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    onSend(input);
    setInput("");
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      display="flex"
      gap={1}
      borderRadius={2}
      bgcolor="rgba(255, 255, 255, 0.8)" // fondo blanco semi-transparente
      borderTop="1px solid rgba(0, 0, 0, 0.4)" // borde sutil
    >
      <TextField
        fullWidth
        value={input}
        disabled={loading}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Escribe tu mensaje..."
        variant="outlined"
        size="small"
        sx={{
          backgroundColor: "rgba(0, 0, 0, 0.4)",
          borderRadius: 1,
          "& .MuiInputBase-input": {
            color: "#000000ff",        // texto blanco
            fontWeight: 600,      // negrita ligera
          },
          "& .MuiOutlinedInput-notchedOutline": {
            borderColor: "rgba(255, 255, 255, 0.6)", // borde más visible sobre fondo oscuro
          },
          "&:hover .MuiOutlinedInput-notchedOutline": {
            borderColor: "#fff",
          },
          "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
            borderColor: "#fff",
          },
        }}
      />
      <Button
        type="submit"
        variant="contained"
        color="primary"
        disabled={loading}
      >
        {loading ? "..." : "Enviar"}
      </Button>
    </Box>
  );
};

export default MessageInput;
