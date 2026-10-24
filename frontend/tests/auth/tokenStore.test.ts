import { afterEach, describe, expect, it, vi } from "vitest";
import { logout, readSession, saveSession } from "../../src/auth/tokenStore";

const accountId = "acct-1";
const token = "secret-token-value";

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe("tokenStore", () => {
  it("stores the account id and token under the approved keys", () => {
    saveSession(accountId, token);

    expect(localStorage.getItem("todo.accountId")).toBe(accountId);
    expect(localStorage.getItem("todo.token")).toBe(token);
    expect(readSession()).toEqual({ accountId, token });
  });

  it("removes both keys on logout and does not call the network", () => {
    saveSession(accountId, token);
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);

    logout();

    expect(localStorage.getItem("todo.accountId")).toBeNull();
    expect(localStorage.getItem("todo.token")).toBeNull();
    expect(readSession()).toBeNull();
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("does not put the token in console output or thrown errors", () => {
    const log = vi.spyOn(console, "log").mockImplementation(() => undefined);
    const info = vi.spyOn(console, "info").mockImplementation(() => undefined);
    const warn = vi.spyOn(console, "warn").mockImplementation(() => undefined);
    const error = vi.spyOn(console, "error").mockImplementation(() => undefined);
    const storage = {
      getItem: vi.fn(() => token),
      setItem: vi.fn(() => {
        throw new Error(`disk full ${token}`);
      }),
      removeItem: vi.fn(),
    };
    vi.stubGlobal("localStorage", storage);

    expect(() => saveSession(accountId, token)).toThrow();
    try {
      saveSession(accountId, token);
    } catch (caught) {
      expect(String(caught)).not.toContain(token);
    }

    logout();

    const output = [log, info, warn, error]
      .flatMap((spy) => spy.mock.calls.flat())
      .join(" ");
    expect(output).not.toContain(token);
  });
});
