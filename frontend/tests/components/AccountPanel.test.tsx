import { act, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { App } from "../../src/App";

interface RecordedCall {
  url: string;
  method: string;
  authorization: string | null;
  body: string | null;
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
          body: init?.body === undefined || init.body === null ? null : String(init.body),
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
  vi.restoreAllMocks();
});

describe("account lifecycle", () => {
  it("creates, restores, logs out, and pastes a token", async () => {
    const user = userEvent.setup();
    const calls = installFetch();
    const token = "one-time-token";
    const first = render(<App />);

    expect(screen.getByText("The service cannot replace a lost token.")).toBeInTheDocument();
    expect(screen.queryByLabelText(/name/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/email/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/password/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/no todos/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/empty account/i)).not.toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "Create account" }));
    await user.click(screen.getByRole("button", { name: "Create account" }));

    const creates = calls.filter((call) => call.method === "POST" && call.url === "/api/v1/users");
    expect(creates).toHaveLength(1);
    expect(creates[0]?.authorization).toBeNull();
    expect(creates[0]?.body).toBeNull();
    expect(creates[0]?.url).not.toContain(token);

    creates[0]?.resolve(jsonResponse(201, { id: "acct-1", token }));

    expect(await screen.findByTestId("token-reveal")).toHaveTextContent(token);
    expect(screen.getByTestId("token-reveal")).toHaveTextContent("acct-1");
    expect(localStorage.getItem("todo.accountId")).toBe("acct-1");
    expect(localStorage.getItem("todo.token")).toBe(token);

    await waitFor(() => {
      expect(calls.filter((call) => call.url === "/api/v1/todos")).toHaveLength(1);
    });
    const firstList = calls.find((call) => call.url === "/api/v1/todos");
    expect(firstList?.method).toBe("GET");
    expect(firstList?.authorization).toBe(`Bearer ${token}`);
    expect(firstList?.url).not.toContain("?");
    await act(async () => {
      firstList?.resolve(jsonResponse(200, [todo("todo-a")]));
    });
    expect(screen.getByText("Title todo-a")).toBeInTheDocument();

    first.unmount();
    const restoredView = render(<App />);
    expect(screen.getByText("Account acct-1")).toBeInTheDocument();
    expect(screen.queryByTestId("token-reveal")).not.toBeInTheDocument();
    expect(screen.queryByText(token)).not.toBeInTheDocument();
    await waitFor(() => {
      expect(calls.filter((call) => call.url === "/api/v1/todos")).toHaveLength(2);
    });
    const restored = calls.filter((call) => call.url === "/api/v1/todos")[1];
    expect(restored?.authorization).toBe(`Bearer ${token}`);
    await act(async () => {
      restored?.resolve(jsonResponse(200, [todo("todo-a")]));
    });
    expect(screen.getByText("Title todo-a")).toBeInTheDocument();

    const callsBeforeLogout = calls.length;
    await user.click(screen.getByRole("button", { name: "Log out" }));
    expect(screen.queryByText("Title todo-a")).not.toBeInTheDocument();
    expect(localStorage.getItem("todo.accountId")).toBeNull();
    expect(localStorage.getItem("todo.token")).toBeNull();
    expect(calls).toHaveLength(callsBeforeLogout);
    expect(calls.some((call) => /revoke|logout/i.test(call.url))).toBe(false);
    expect(window.location.href).not.toContain(token);
    expect(screen.getByText("The service cannot replace a lost token.")).toBeInTheDocument();

    await user.type(screen.getByLabelText("Saved token"), token);
    await user.click(screen.getByRole("button", { name: "Use saved token" }));
    await waitFor(() => {
      expect(calls.filter((call) => call.url === "/api/v1/todos")).toHaveLength(3);
    });
    const pasted = calls.filter((call) => call.url === "/api/v1/todos")[2];
    expect(pasted?.authorization).toBe(`Bearer ${token}`);
    expect(screen.queryByTestId("token-reveal")).not.toBeInTheDocument();
    expect(screen.queryByText("Account acct-1")).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Log out" })).toBeInTheDocument();
    await act(async () => {
      pasted?.resolve(jsonResponse(200, [todo("todo-a")]));
    });
    expect(screen.getByText("Title todo-a")).toBeInTheDocument();
    restoredView.unmount();
  });

  it("drops the previous account id when a different token is pasted", async () => {
    const user = userEvent.setup();
    const calls = installFetch();
    localStorage.setItem("todo.accountId", "acct-a");
    localStorage.setItem("todo.token", "token-a");
    render(<App />);

    expect(screen.getByText("Account acct-a")).toBeInTheDocument();
    await waitFor(() => {
      expect(calls.filter((call) => call.url === "/api/v1/todos")).toHaveLength(1);
    });

    await user.type(screen.getByLabelText("Saved token"), "token-b");
    await user.click(screen.getByRole("button", { name: "Use saved token" }));
    expect(screen.queryByText("Account acct-a")).not.toBeInTheDocument();
    expect(screen.queryByTestId("token-reveal")).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Log out" })).toBeInTheDocument();
    const replacement = calls.filter((call) => call.url === "/api/v1/todos").at(-1);
    expect(replacement?.authorization).toBe("Bearer token-b");
    expect(replacement?.url).toBe("/api/v1/todos");
    expect(replacement?.url).not.toContain("token-a");
    expect(replacement?.url).not.toContain("token-b");
    await act(async () => {
      replacement?.resolve(jsonResponse(200, [todo("todo-b")]));
    });
    expect(screen.queryByText("Title todo-a")).not.toBeInTheDocument();
    expect(screen.getByText("Title todo-b")).toBeInTheDocument();
  });

  it("clears stored todos when the service rejects the token", async () => {
    const calls = installFetch();
    localStorage.setItem("todo.accountId", "acct-1");
    localStorage.setItem("todo.token", "token-bad");
    render(<App />);

    await waitFor(() => {
      expect(calls.filter((call) => call.url === "/api/v1/todos")).toHaveLength(1);
    });
    calls[0]?.resolve(
      jsonResponse(401, {
        error: { code: "unauthenticated", message: "You must be identified." },
      }),
    );

    expect(await screen.findByText("You must be identified.")).toBeInTheDocument();
    expect(screen.queryByText("Title todo-a")).not.toBeInTheDocument();
    expect(window.location.href).not.toContain("token-bad");
  });
});
