const API_BASE = import.meta.env.VITE_API_URL || '';

async function handleResponse(res: Response) {
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || 'API Error');
  }
  return res.json();
}

const api = {
  get: (path: string) => fetch(`${API_BASE}${path}`, { credentials: 'include' }).then(handleResponse),
  post: (path: string, body?: unknown) => fetch(`${API_BASE}${path}`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body ?? {}),
  }).then(handleResponse),
  put: (path: string, body?: unknown) => fetch(`${API_BASE}${path}`, {
    method: 'PUT',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body ?? {}),
  }).then(handleResponse),
  delete: (path: string) => fetch(`${API_BASE}${path}`, {
    method: 'DELETE',
    credentials: 'include',
  }).then(handleResponse),
};

export default api;
