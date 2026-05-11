const API_PORT = '8001';

export function getApiBaseUrl(): string {
  if (typeof window === 'undefined') {
    return `http://127.0.0.1:${API_PORT}/api`;
  }

  const { hostname, protocol } = window.location;
  const apiHost =
    hostname === 'localhost' || hostname === '127.0.0.1'
      ? '127.0.0.1'
      : hostname;

  return `${protocol}//${apiHost}:${API_PORT}/api`;
}

export function apiUrl(path: string): string {
  const cleanPath = path.replace(/^\/+/, '');
  return `${getApiBaseUrl()}/${cleanPath}`;
}
