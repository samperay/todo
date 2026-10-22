const ACCOUNT_ID_KEY = "todo.accountId";
const TOKEN_KEY = "todo.token";

export interface StoredSession {
  accountId: string;
  token: string;
}

export function readSession(): StoredSession | null {
  const token = localStorage.getItem(TOKEN_KEY);
  if (!token) {
    return null;
  }
  return {
    accountId: localStorage.getItem(ACCOUNT_ID_KEY) ?? "",
    token,
  };
}

export function saveSession(accountId: string, token: string): void {
  try {
    localStorage.setItem(ACCOUNT_ID_KEY, accountId);
    localStorage.setItem(TOKEN_KEY, token);
  } catch {
    throw new Error("Could not store the session.");
  }
}

export function logout(): void {
  localStorage.removeItem(ACCOUNT_ID_KEY);
  localStorage.removeItem(TOKEN_KEY);
}
