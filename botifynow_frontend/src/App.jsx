import { useState } from "react";
import "./App.css";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [file, setFile] = useState(null);
  const [typing, setTyping] = useState(false);
  const [documentId, setDocumentId] = useState(null);

  const addMessage = (sender, text) => {
    setMessages((prev) => [...prev, { sender, text }]);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setTyping(true);

    try {
      const url = documentId ? "/api/rag-chat" : "/api/chat";
      const body = documentId
        ? { message: input, document_id: documentId }
        : { message: input };

      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Unknown error");

      addMessage("bot", data.response || "❌ No response from server.");
    } catch (err) {
      addMessage("bot", "❌ Error: Could not get response.");
    } finally {
      setTyping(false);
    }
  };

  const uploadFile = async () => {
    if (!file) return alert("Please select a PDF or TXT file.");
    setTyping(true);
    addMessage("bot", "📤 Uploading file...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Upload failed");

      setDocumentId(data.document_id);
      addMessage("bot", `✅ Document uploaded! ID: ${data.document_id}`);

      // Auto-summarize after upload
      setTyping(true);
      addMessage("bot", "🧠 Generating summary...");

      const summaryRes = await fetch("/api/rag-chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: "Summarize this document",
          document_id: data.document_id,
        }),
      });

      const summaryData = await summaryRes.json();
      if (!summaryRes.ok) throw new Error(summaryData.detail || "Summary failed");

      addMessage("bot", summaryData.response || "❌ Couldn't summarize the document.");
    } catch (err) {
      addMessage("bot", `❌ ${err.message}`);
    } finally {
      setTyping(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">🤖 BotifyNow</header>

      <div className="chat-container">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`chat-bubble ${msg.sender === "user" ? "user" : "bot"}`}
          >
            {msg.text}
          </div>
        ))}
        {typing && <div className="chat-bubble bot typing">…Bot is typing</div>}
      </div>

      <div className="input-section">
        <input
          type="text"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>

      <div className="upload-section">
        <input
          type="file"
          accept=".pdf, .txt"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button onClick={uploadFile}>Upload</button>
      </div>
    </div>
  );
}
