import { useCallback, useEffect, useRef, useState } from "react";
import { listTodos } from "../api/todos";
import type { Todo } from "../api/types";
import { createAccount } from "../api/users";
import { logout as clearStoredSession, readSession, saveSession } from "../auth/tokenStore";

export type ListStatus = "idle" | "loading" | "ready" | "error";
export type TodoFilter = "all" | "pending" | "completed";

const UNAUTHENTICATED = "You must be identified.";

function initialSession(): { accountId: string | null; token: string | null } {
  const stored = readSession();
  if (!stored?.token) {
    return { accountId: null, token: null };
  }
  return { accountId: stored.accountId || null, token: stored.token };
}

export function useTodoSession() {
  const initial = useState(initialSession)[0];
  const generationRef = useRef(0);
  const controllersRef = useRef<AbortController[]>([]);
  const creatingRef = useRef(false);
  const accountIdRef = useRef<string | null>(initial.accountId);
  const tokenRef = useRef<string | null>(initial.token);
  const [sessionGeneration, setSessionGeneration] = useState(0);
  const [todos, setTodos] = useState<Todo[]>([]);
  const [filter] = useState<TodoFilter>("all");
  const [listStatus, setListStatus] = useState<ListStatus>("idle");
  const [accountId, setAccountId] = useState<string | null>(initial.accountId);
  const [token, setToken] = useState<string | null>(initial.token);
  const [revealToken, setRevealToken] = useState(false);
  const [creating, setCreating] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);

  const isCurrent = useCallback((generation: number): boolean => {
    return generation === generationRef.current;
  }, []);

  const remember = useCallback((nextAccountId: string | null, nextToken: string | null): void => {
    accountIdRef.current = nextAccountId;
    tokenRef.current = nextToken;
    setAccountId(nextAccountId);
    setToken(nextToken);
  }, []);

  const abortInFlight = useCallback((): void => {
    for (const controller of controllersRef.current) {
      controller.abort();
    }
    controllersRef.current = [];
  }, []);

  const bumpGeneration = useCallback((): number => {
    abortInFlight();
    generationRef.current += 1;
    setSessionGeneration(generationRef.current);
    setTodos([]);
    setNotice(null);
    return generationRef.current;
  }, [abortInFlight]);

  const trackRequest = useCallback((): AbortController => {
    const controller = new AbortController();
    controllersRef.current.push(controller);
    return controller;
  }, []);

  const loadTodos = useCallback(
    async (activeToken: string, generation: number): Promise<void> => {
      const controller = trackRequest();
      setListStatus("loading");
      const result = await listTodos(activeToken, generation, isCurrent, controller.signal);
      if (result.discarded || controller.signal.aborted || !isCurrent(generation)) {
        return;
      }
      if (result.status === 401) {
        bumpGeneration();
        setNotice(UNAUTHENTICATED);
        setListStatus("error");
        return;
      }
      if (result.status === 200 && result.todos) {
        if (!isCurrent(generation)) {
          return;
        }
        setTodos(result.todos);
        setListStatus("ready");
        return;
      }
      setListStatus("error");
    },
    [bumpGeneration, isCurrent, trackRequest],
  );

  useEffect(() => {
    if (!initial.token) {
      return;
    }
    void loadTodos(initial.token, generationRef.current);
    return () => {
      abortInFlight();
    };
  }, [initial.token, loadTodos, abortInFlight]);

  async function createNewAccount(): Promise<void> {
    if (creatingRef.current) {
      return;
    }
    creatingRef.current = true;
    setCreating(true);
    const generation = generationRef.current;
    const controller = trackRequest();
    try {
      const result = await createAccount(generation, isCurrent, controller.signal);
      if (result.discarded || !isCurrent(generation) || !result.user) {
        return;
      }
      const nextGeneration = bumpGeneration();
      saveSession(result.user.id, result.user.token);
      remember(result.user.id, result.user.token);
      setRevealToken(true);
      await loadTodos(result.user.token, nextGeneration);
    } finally {
      creatingRef.current = false;
      setCreating(false);
    }
  }

  function logout(): void {
    bumpGeneration();
    clearStoredSession();
    remember(null, null);
    setRevealToken(false);
    setListStatus("idle");
  }

  async function pasteToken(value: string): Promise<void> {
    const nextToken = value.trim();
    if (!nextToken) {
      return;
    }
    const nextAccountId = tokenRef.current === nextToken ? accountIdRef.current : null;
    const nextGeneration = bumpGeneration();
    saveSession(nextAccountId ?? "", nextToken);
    remember(nextAccountId, nextToken);
    setRevealToken(false);
    await loadTodos(nextToken, nextGeneration);
  }

  return {
    sessionGeneration,
    todos,
    filter,
    listStatus,
    accountId,
    token,
    revealToken,
    creating,
    notice,
    createAccount: createNewAccount,
    logout,
    pasteToken,
  };
}
