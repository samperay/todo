import { act, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { App } from "../../src/App";

const LOADING = "Loading todos.";
const EMPTY_ACCOUNT = "This account has no todos.";
const LIST_FAILED = "The list could not be loaded.";

interface RecordedCall {
  url: string;
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

function todo(fields: {
  id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: "low" | "medium" | "high";
  created_at: string;
  updated_at: string;
}) {
  return fields;
}

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe("todo list", () => {
  it("shows returned order and every field, including markup as text", async () => {
    const calls = installFetch();
    const alert = vi.fn();
    vi.stubGlobal("alert", alert);
    localStorage.setItem("todo.accountId", "acct-a");
    localStorage.setItem("todo.token", "token-a");
    const { container } = render(<App />);

    await waitFor(() => {
      expect(screen.getByText(LOADING)).toBeInTheDocument();
    });
    expect(screen.queryByText(EMPTY_ACCOUNT)).not.toBeInTheDocument();

    const older = todo({
      id: "todo-older",
      title: "<script>alert(1)</script>",
      description: "From the shop",
      completed: false,
      priority: "low",
      created_at: "2020-01-01T00:00:00Z",
      updated_at: "2020-01-02T00:00:00Z",
    });
    const newer = todo({
      id: "todo-newer",
      title: "Newer title",
      description: null,
      completed: true,
      priority: "high",
      created_at: "2024-05-01T00:00:00Z",
      updated_at: "2024-05-02T00:00:00Z",
    });

    await act(async () => {
      calls[0]?.resolve(jsonResponse(200, [older, newer]));
    });

    expect(screen.queryByText(LOADING)).not.toBeInTheDocument();
    expect(screen.queryByText(EMPTY_ACCOUNT)).not.toBeInTheDocument();
    const items = screen.getAllByRole("listitem");
    expect(items).toHaveLength(2);
    expect(items[0]).toHaveTextContent("<script>alert(1)</script>");
    expect(items[0]).toHaveTextContent("From the shop");
    expect(items[0]).toHaveTextContent("Not completed");
    expect(items[0]).toHaveTextContent("low");
    expect(items[0]).toHaveTextContent("todo-older");
    expect(items[0]).toHaveTextContent("2020-01-01T00:00:00Z");
    expect(items[0]).toHaveTextContent("2020-01-02T00:00:00Z");
    expect(items[1]).toHaveTextContent("Newer title");
    expect(items[1]).not.toHaveTextContent("From the shop");
    expect(items[1]).toHaveTextContent("Completed");
    expect(items[1]).not.toHaveTextContent("Not completed");
    expect(items[1]).toHaveTextContent("high");
    expect(items[1]).toHaveTextContent("todo-newer");
    expect(items[1]).toHaveTextContent("2024-05-01T00:00:00Z");
    expect(items[1]).toHaveTextContent("2024-05-02T00:00:00Z");
    expect(items[0]?.compareDocumentPosition(items[1]!) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(container.querySelector("script")).toBeNull();
    expect(container.innerHTML).not.toContain("<script>");
    expect(alert).not.toHaveBeenCalled();
  });

  it("shows the empty account only after a successful empty list", async () => {
    const calls = installFetch();
    localStorage.setItem("todo.accountId", "acct-a");
    localStorage.setItem("todo.token", "token-a");
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(LOADING)).toBeInTheDocument();
    });
    expect(screen.queryByText(EMPTY_ACCOUNT)).not.toBeInTheDocument();

    await act(async () => {
      calls[0]?.resolve(jsonResponse(200, []));
    });

    expect(screen.getByText(EMPTY_ACCOUNT)).toBeInTheDocument();
    expect(screen.queryByText(LOADING)).not.toBeInTheDocument();
    expect(screen.queryByText(LIST_FAILED)).not.toBeInTheDocument();
    expect(screen.queryByRole("listitem")).not.toBeInTheDocument();
  });

  it("shows a failure instead of an empty account when the first list fails", async () => {
    const calls = installFetch();
    localStorage.setItem("todo.accountId", "acct-a");
    localStorage.setItem("todo.token", "token-a");
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(LOADING)).toBeInTheDocument();
    });

    await act(async () => {
      calls[0]?.resolve(jsonResponse(500, { detail: "database unavailable" }));
    });

    expect(screen.getByText(LIST_FAILED)).toBeInTheDocument();
    expect(screen.queryByText(EMPTY_ACCOUNT)).not.toBeInTheDocument();
    expect(screen.queryByText(LOADING)).not.toBeInTheDocument();
    expect(screen.queryByText("database unavailable")).not.toBeInTheDocument();
    expect(screen.queryByRole("listitem")).not.toBeInTheDocument();
  });

  it("replaces the visible rows when the account changes and ignores the old response", async () => {
    const user = userEvent.setup();
    const calls = installFetch();
    localStorage.setItem("todo.accountId", "acct-a");
    localStorage.setItem("todo.token", "token-a");
    render(<App />);

    await waitFor(() => {
      expect(calls).toHaveLength(1);
    });
    await act(async () => {
      calls[0]?.resolve(
        jsonResponse(200, [
          todo({
            id: "todo-a",
            title: "Alpha",
            description: null,
            completed: false,
            priority: "medium",
            created_at: "2024-01-01T00:00:00Z",
            updated_at: "2024-01-01T00:00:00Z",
          }),
        ]),
      );
    });
    expect(screen.getByText("Alpha")).toBeInTheDocument();

    await user.type(screen.getByLabelText("Saved token"), "token-b");
    await user.click(screen.getByRole("button", { name: "Use saved token" }));

    expect(screen.queryByText("Alpha")).not.toBeInTheDocument();
    expect(screen.queryByText(EMPTY_ACCOUNT)).not.toBeInTheDocument();
    expect(screen.getByText(LOADING)).toBeInTheDocument();

    await waitFor(() => {
      expect(calls).toHaveLength(2);
    });
    await act(async () => {
      calls[1]?.resolve(
        jsonResponse(200, [
          todo({
            id: "todo-b",
            title: "Beta",
            description: "Second account",
            completed: false,
            priority: "low",
            created_at: "2024-02-01T00:00:00Z",
            updated_at: "2024-02-01T00:00:00Z",
          }),
        ]),
      );
    });
    expect(screen.getByText("Beta")).toBeInTheDocument();
    expect(screen.queryByText("Alpha")).not.toBeInTheDocument();
  });
});
