'use client';

import { FormEvent, useMemo, useState } from 'react';
import { useChat } from '@ai-sdk/react';
import { TextStreamChatTransport, UIMessage } from 'ai';

function getMessageText(message: UIMessage) {
  return message.parts
    .filter((p) => p.type === 'text')
    .map((p) => p.text)
    .join(' ');
}

export default function HomePage() {
  const [candidateName, setCandidateName] = useState('Candidato');
  const [conversationId] = useState(() => crypto.randomUUID());
  const [input, setInput] = useState('');

  const { messages, status, sendMessage } = useChat({
    transport: new TextStreamChatTransport({
      api: '/api/chat',
      body: { conversationId, candidateName },
    }),
  });

  const disabled = useMemo(() => status === 'submitted' || status === 'streaming', [status]);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const text = input.trim();
    if (!text) return;
    setInput('');
    await sendMessage({ text });
  };

  return (
    <main className="container">
      <h1>Agentic UI · Screening Product Designer</h1>
      <p className="small">UI con AI SDK que conversa y orquesta la entrevista contra FastAPI.</p>

      <div className="row">
        <input value={candidateName} onChange={(e) => setCandidateName(e.target.value)} placeholder="Nombre del candidato" />
        <button onClick={() => sendMessage({ text: 'Hola, quiero iniciar la entrevista.' })} disabled={disabled}>
          Iniciar entrevista
        </button>
      </div>

      <div className="chat">
        {messages.map((m) => (
          <div key={m.id} className={`msg ${m.role}`}>
            <strong>{m.role === 'user' ? 'Candidato' : 'Entrevistador'}:</strong>
            <span>{getMessageText(m)}</span>
          </div>
        ))}
      </div>

      <form onSubmit={onSubmit} className="row">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          rows={3}
          style={{ flex: 1 }}
          placeholder="Escribe una respuesta de experiencia profesional..."
        />
        <button type="submit" disabled={disabled}>Enviar</button>
      </form>
    </main>
  );
}
