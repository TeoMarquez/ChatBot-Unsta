import React from "react";
import ChatRoom from "./views/ChatRoom";
import patternBg from './assets/pattern-background.jpg';

function App() {
  return (
    <div
      className="app"
      style={{
        backgroundImage: `linear-gradient(rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.6)), url(${patternBg})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "repeat",
        width: "100%",
        height: "98vh",
        overflow: "hidden",
      }}
    >
      <ChatRoom />
    </div>
  );
}

export default App;
