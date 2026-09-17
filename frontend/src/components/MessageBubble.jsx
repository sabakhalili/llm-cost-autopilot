import RoutingStrip from "./RoutingStrip.jsx";

export default function MessageBubble({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`message-row ${isUser ? "from-user" : "from-assistant"}`}>
      <div className="message-bubble">{message.content}</div>
      {!isUser && message.routing && <RoutingStrip routing={message.routing} />}
    </div>
  );
}
