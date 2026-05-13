const LOCAL_API_PORT = '8001';
const REMOTE_API_PORT = '8001';
const REMOTE_API_HOST = '107.20.54.80';

function isLocalFrontend(): boolean {
  if (typeof globalThis.location === 'undefined') {
    return false;
  }

  return ['localhost', '127.0.0.1'].includes(globalThis.location.hostname);
}

export function getApiBaseUrl(): string {
  if (isLocalFrontend()) {
    return `http://localhost:${LOCAL_API_PORT}/api`;
  }

  return `http://${REMOTE_API_HOST}:${REMOTE_API_PORT}/api`;
}

export function apiUrl(path: string): string {
  const cleanPath = path.replace(/^\/+/, '');
  return `${getApiBaseUrl()}/${cleanPath}`;
}
