const API_BASE = import.meta.env.VITE_API_URL;

export async function fetchRooms() {
  const response = await fetch(`${API_BASE}/api/images`);

  if (!response.ok) {
    throw new Error('Failed to load hospital rooms');
  }

  return response.json();
}

export async function analyzeRoom(roomId) {
  const response = await fetch(
    `${API_BASE}/api/rooms/${encodeURIComponent(roomId)}/analyze`,
    { method: 'POST' }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Room analysis failed');
  }

  return data;
}