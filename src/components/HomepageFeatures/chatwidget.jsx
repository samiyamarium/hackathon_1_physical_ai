import React, { useState } from "react";

export default function ChatWidget() {
  const [messages, setMessages] = useState([]);
  const [msg, setMsg] = useState("");

  async function sendMessage() {
    const res = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: msg,
        selected_text: window.getSelection().toString()
      }),
    });

    const data = await res.json();
    setMessages([...messages, { q: msg, a: data.answer }]);
    setMsg("");
  }

  return (
    <div style={{position:"fixed", bottom:20, right:20, background:"white", padding:20, width:300, borderRadius:10}}>
      <h4>📘 Book Assistant</h4>
      <div style={{maxHeight:200, overflowY:"scroll"}}>
        {messages.map((m, i) => (
          <div key={i}>
            <b>You:</b> {m.q}<br/>
            <b>Bot:</b> {m.a}<hr/>
          </div>
        ))}
      </div>
      <input value={msg} onChange={e => setMsg(e.target.value)} style={{width:"100%"}} />
      <button onClick={sendMessage} style={{marginTop:10, width:"100%"}}>Ask</button>
    </div>
  );
}
