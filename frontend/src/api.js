export async function postChat(message, history, conversationId) {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history, conversation_id: conversationId }),
  });
  if (!res.ok) {
    throw new Error(`Chat request failed: ${res.status}`);
  }
  return res.json();
}

export async function getStatsSummary() {
  const res = await fetch("/api/stats/summary");
  if (!res.ok) {
    throw new Error(`Stats request failed: ${res.status}`);
  }
  return res.json();
}
