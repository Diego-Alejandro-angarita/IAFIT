const REMOTE_API_PORT = '8001';
const REMOTE_API_HOST = '100.31.58.141';
const API_BASE_URL = `http://${REMOTE_API_HOST}:${REMOTE_API_PORT}/api`;

export function getApiBaseUrl(): string {
  return API_BASE_URL;
}

export function apiUrl(path: string): string {
  const cleanPath = path.replace(/^\/+/, '');
  return `${getApiBaseUrl()}/${cleanPath}`;
}
