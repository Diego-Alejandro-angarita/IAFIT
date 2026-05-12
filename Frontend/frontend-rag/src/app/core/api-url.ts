const API_PORT = '8001';
const API_HOST = '107.20.54.80';

export function getApiBaseUrl(): string {
  return `http://${API_HOST}:${API_PORT}/api`;
}

export function apiUrl(path: string): string {
  const cleanPath = path.replace(/^\/+/, '');
  return `${getApiBaseUrl()}/${cleanPath}`;
}
