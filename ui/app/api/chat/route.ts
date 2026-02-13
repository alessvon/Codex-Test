import { createTextStreamResponse, simulateReadableStream } from 'ai';

type ChatBody = {
  messages: Array<{ role: string; content: string }>;
  conversationId?: string;
  candidateName?: string;
};

const sessionByConversation = new Map<string, string>();

const baseUrl = process.env.FASTAPI_URL ?? 'http://127.0.0.1:8000';

export async function POST(req: Request) {
  const body = (await req.json()) as ChatBody;
  const conversationId = body.conversationId ?? crypto.randomUUID();
  const lastUserMessage = [...(body.messages ?? [])].reverse().find((m) => m.role === 'user')?.content ?? '';

  let sessionId = sessionByConversation.get(conversationId);

  if (!sessionId) {
    const createRes = await fetch(`${baseUrl}/api/session`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        candidate_name: body.candidateName || 'Candidato',
        target_role: 'Product Designer',
        language: 'es',
      }),
    });

    if (!createRes.ok) {
      return new Response('No se pudo crear la sesión en FastAPI. Asegúrate de correr backend en puerto 8000.', { status: 500 });
    }

    const created = await createRes.json();
    const newSessionId = String(created.session_id || "");
    if (!newSessionId) {
      return new Response("FastAPI no devolvió session_id.", { status: 500 });
    }
    sessionId = newSessionId;
    sessionByConversation.set(conversationId, newSessionId);
  }

  const answerRes = await fetch(`${baseUrl}/api/session/${sessionId}/message`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ message: lastUserMessage || 'Continuemos con la entrevista.' }),
  });

  if (!answerRes.ok) {
    return new Response('No se pudo continuar la entrevista.', { status: 500 });
  }

  const assistant = await answerRes.json();

  const reportRes = await fetch(`${baseUrl}/api/session/${sessionId}/report`);
  const report = reportRes.ok ? await reportRes.json() : null;

  return createTextStreamResponse({
    headers: report ? { 'x-profile-json': encodeURIComponent(JSON.stringify(report)) } : undefined,
    textStream: simulateReadableStream({ chunks: [assistant.reply] }),
  });
}
