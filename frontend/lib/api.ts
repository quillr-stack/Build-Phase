const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export async function fetchPersonas() {
  const res = await fetch(`${API_URL}/personas`);
  if (!res.ok) throw new Error('Failed to fetch personas');
  return res.json();
}

export async function simulate(data: any) {
  const res = await fetch(`${API_URL}/simulate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to start simulation');
  return res.json();
}

export async function getRun(id: string) {
  const res = await fetch(`${API_URL}/runs/${id}`);
  if (!res.ok) throw new Error('Failed to fetch run');
  return res.json();
}

export async function getSystemAccuracy() {
  const res = await fetch(`${API_URL}/system/accuracy`);
  if (!res.ok) throw new Error('Failed to fetch system accuracy');
  return res.json();
}
