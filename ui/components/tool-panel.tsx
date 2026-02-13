'use client';

export function ToolPanel({ profile }: { profile: Record<string, unknown> | null }) {
  if (!profile) return null;

  return (
    <div className="tool-card">
      <strong>Extracción estructurada (Agentic UI)</strong>
      <pre style={{ whiteSpace: 'pre-wrap', margin: '.5rem 0 0' }}>{JSON.stringify(profile, null, 2)}</pre>
    </div>
  );
}
