import { useState } from "react";
import ChatThread from "./components/ChatThread.jsx";
import SavingsTicker from "./components/SavingsTicker.jsx";
import { postChat } from "./api.js";

const CONVERSATION_ID = crypto.randomUUID();

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [totalSaved, setTotalSaved] = useState(0);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null);

  async function sendMessage(text) {
    const trimmed = text.trim();
    if (!trimmed || sending) return;

    const userMessage = { id: crypto.randomUUID(), role: "user", content: trimmed };
    const history = messages.map((m) => ({ role: m.role, content: m.content }));

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setSending(true);
    setError(null);

    try {
      const data = await postChat(trimmed, history, CONVERSATION_ID);
      const assistantMessage = {
        id: data.id,
        role: "assistant",
        content: data.reply,
        routing: data.routing,
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setTotalSaved((prev) => prev + data.routing.cost_saved);
    } catch (err) {
      setError(err.message);
    } finally {
      setSending(false);
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    sendMessage(input);
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>LLM Cost Autopilot</h1>
        <SavingsTicker totalSaved={totalSaved} />
      </header>

      <ChatThread messages={messages} />

      {error && <p className="chat-error">{error}</p>}

      <form className="chat-input-row" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
          disabled={sending}
        />
        <button type="submit" disabled={sending || !input.trim()}>
          {sending ? "Routing..." : "Send"}
        </button>
      </form>
    </div>
  );
}
