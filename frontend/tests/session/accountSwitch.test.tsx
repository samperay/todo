import { act, renderHook, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { useTodoSession } from "../../src/session/useTodoSession";

interface RecordedCall {
  url: string;
  method: string;
  authorization: string | null;
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

function ids(todos: { id: string }[]): string {
  return todos.map((item) => item.id).join(",");
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("account switch", () => {
  it("keeps only the new account when the previous list resolves late", async () => {
    const calls = installFetch();
    localStorage.setItem("todo.accountId", "acct-a");
    localStorage.setItem("todo.token", "token-a");
    const { result } = renderHook(() => useTodoSession());

    await waitFor(() => {
      expect(calls).toHaveLength(1);
    });
    const listA = calls[0];
    expect(listA?.authorization).toBe("Bearer token-a");

    act(() => {
      void result.current.pasteToken("token-b");
    });
    await waitFor(() => {
      expect(calls).toHaveLength(2);
    });
    const listB = calls[1];
    expect(listB?.authorization).toBe("Bearer token-b");
    expect(ids(result.current.todos)).toBe("");
    expect(result.current.accountId).toBeNull();

    listB?.resolve(jsonResponse(200, [todo("todo-b")]));
    await waitFor(() => {
      expect(ids(result.current.todos)).toBe("todo-b");
    });

    await act(async () => {
      listA?.resolve(jsonResponse(200, [todo("todo-a")]));
    });
    expect(ids(result.current.todos)).toBe("todo-b");
  });

  it("leaves stored todos empty when a list resolves after logout", async () => {
    const calls = installFetch();
    localStorage.setItem("todo.accountId", "acct-a");
    localStorage.setItem("todo.token", "token-a");
    const { result } = renderHook(() => useTodoSession());

    await waitFor(() => {
      expect(calls).toHaveLength(1);
    });
    const listA = calls[0];

    act(() => {
      result.current.logout();
    });
    expect(ids(result.current.todos)).toBe("");
    expect(localStorage.getItem("todo.accountId")).toBeNull();
    expect(localStorage.getItem("todo.token")).toBeNull();

    await act(async () => {
      listA?.resolve(jsonResponse(200, [todo("todo-a")]));
    });
    expect(ids(result.current.todos)).toBe("");
  });
});
