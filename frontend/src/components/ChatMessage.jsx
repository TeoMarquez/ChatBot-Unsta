import { Box, Avatar, Paper, Typography } from "@mui/material";

import icon from '../assets/icon-genericPFP.png';

const ChatMessage = ({ sender, text }) => {
  const isUser = sender === "user";

  const avatarContent = isUser ? (
    <Avatar
      src={icon}
      alt="User"
      sx={{ width: 40, height: 40 }}
    />
  ) : (
    <Avatar sx={{ width: 40, height: 40, bgcolor: "#1976d2" }}>
      🤖
    </Avatar>
  );

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        gap: 1,
      }}
    >
      {!isUser && avatarContent}

      <Paper
        elevation={1}
        sx={{
          px: 2,
          py: 1,
          maxWidth: "75%",
          bgcolor: isUser ? "#1976d2" : "#e0e0e0",
          color: isUser ? "white" : "black",
          borderTopLeftRadius: 16,
          borderTopRightRadius: 16,
          borderBottomLeftRadius: isUser ? 16 : 0,
          borderBottomRightRadius: isUser ? 0 : 16,
        }}
      >
        <Typography variant="body1">{text}</Typography>
      </Paper>

      {isUser && avatarContent}
    </Box>
  );
};

export default ChatMessage;
