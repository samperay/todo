import { act, renderHook, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { useTodoSession } from "../../src/session/useTodoSession";

interface RecordedCall {
  url: string;
  method: string;
  authorization: string | null;
  signal: AbortSignal | undefined;
  resolve: (response: Response) => void;
}

function installFetch() {
  const calls: RecordedCall[] = [];
  vi.stubGlobal(
    "fetch",
    vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const headers = new Headers(init?.headers);
      return new Promise<Response>((resolve) => {
        calls.push({
          url: String(input),
          method: (init?.method ?? "GET").toUpperCase(),
          authorization: headers.get("Authorization"),
          signal: init?.signal ?? undefined,
          resolve,
        });
      });
    }),
  );
  return calls;
}

function jsonResponse(status: number, body: unknown): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function todo(id: string) {
  return {
    id,
    title: `Title ${id}`,
    description: null,
    completed: false,
    priority: "medium",
    created_at: "2026-10-22T00:00:00Z",
    updated_at: "2026-10-22T00:00:00Z",
  };
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("useTodoSession", () => {
  it("stores the created account id and token and restores both without revealing the token", async () => {
    const calls = installFetch();
    const token = "created-token";
    const first = renderHook(() => useTodoSession());

    act(() => {
      void first.result.current.createAccount();
      void first.result.current.createAccount();
    });
    const creates = calls.filter((call) => call.method === "POST" && call.url === "/api/v1/users");
    expect(creates).toHaveLength(1);
    expect(creates[0]?.authorization).toBeNull();
    expect(creates[0]?.signal).toBeDefined();

    creates[0]?.resolve(jsonResponse(201, { id: "acct-1", token }));
    await waitFor(() => {
      expect(first.result.current.revealToken).toBe(true);
    });
    expect(first.result.current.accountId).toBe("acct-1");
    expect(first.result.current.token).toBe(token);
    expect(localStorage.getItem("todo.accountId")).toBe("acct-1");
    expect(localStorage.getItem("todo.token")).toBe(token);

    await waitFor(() => {
      expect(calls.filter((call) => call.url === "/api/v1/todos")).toHaveLength(1);
    });
    calls.find((call) => call.url === "/api/v1/todos")?.resolve(jsonResponse(200, [todo("todo-a")]));
    await waitFor(() => {
      expect(first.result.current.todos.map((item) => item.id)).toEqual(["todo-a"]);
    });

    first.unmount();
    const restored = renderHook(() => useTodoSession());
    expect(restored.result.current.accountId).toBe("acct-1");
    expect(restored.result.current.token).toBe(token);
    expect(restored.result.current.revealToken).toBe(false);
    await waitFor(() => {
      expect(calls.filter((call) => call.url === "/api/v1/todos")).toHaveLength(2);
    });
    expect(calls.filter((call) => call.url === "/api/v1/todos")[1]?.authorization).toBe(`Bearer ${token}`);
  });

  it("does not invent an account id for a pasted token", async () => {
    const calls = installFetch();
    localStorage.setItem("todo.accountId", "acct-a");
    localStorage.setItem("todo.token", "token-a");
    const { result } = renderHook(() => useTodoSession());

    await waitFor(() => {
      expect(calls).toHaveLength(1);
    });
    calls[0]?.resolve(jsonResponse(200, [todo("todo-a")]));
    await waitFor(() => {
      expect(result.current.todos.map((item) => item.id)).toEqual(["todo-a"]);
    });

    act(() => {
      void result.current.pasteToken("token-a");
    });
    expect(result.current.accountId).toBe("acct-a");
    expect(localStorage.getItem("todo.accountId")).toBe("acct-a");

    act(() => {
      void result.current.pasteToken("token-b");
    });
    expect(result.current.accountId).toBeNull();
    expect(result.current.token).toBe("token-b");
    expect(result.current.todos).toEqual([]);
    expect(localStorage.getItem("todo.accountId")).toBe("");
    expect(localStorage.getItem("todo.token")).toBe("token-b");
    await waitFor(() => {
      expect(calls.at(-1)?.authorization).toBe("Bearer token-b");
    });
  });

  it("clears stored todos when the service rejects the token", async () => {
    const calls = installFetch();
    localStorage.setItem("todo.accountId", "acct-1");
    localStorage.setItem("todo.token", "token-bad");
    const { result } = renderHook(() => useTodoSession());

    await waitFor(() => {
      expect(calls).toHaveLength(1);
    });
    calls[0]?.resolve(
      jsonResponse(401, {
        error: { code: "unauthenticated", message: "You must be identified." },
      }),
    );

    await waitFor(() => {
      expect(result.current.notice).toBe("You must be identified.");
    });
    expect(result.current.todos).toEqual([]);
  });

  it("discards the restore request cleaned up by StrictMode", async () => {
    const calls = installFetch();
    localStorage.setItem("todo.accountId", "acct-a");
    localStorage.setItem("todo.token", "token-a");
    const { result } = renderHook(() => useTodoSession(), { reactStrictMode: true });

    await waitFor(() => {
      const live = calls.filter((call) => call.url === "/api/v1/todos" && !call.signal?.aborted);
      expect(live).toHaveLength(1);
    });

    const lists = calls.filter((call) => call.url === "/api/v1/todos");
    const obsolete = lists.filter((call) => call.signal?.aborted);
    const live = lists.filter((call) => !call.signal?.aborted);
    expect(obsolete.length).toBeGreaterThan(0);
    expect(live).toHaveLength(1);

    await act(async () => {
      live[0]?.resolve(jsonResponse(200, [todo("todo-a")]));
    });
    await waitFor(() => {
      expect(result.current.todos.map((item) => item.id)).toEqual(["todo-a"]);
    });

    await act(async () => {
      for (const call of obsolete) {
        call.resolve(jsonResponse(200, [todo("stale")]));
      }
    });
    expect(result.current.todos.map((item) => item.id)).toEqual(["todo-a"]);
    expect(result.current.accountId).toBe("acct-a");
  });
});
