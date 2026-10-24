import { apiBasePath } from "../config";

const REQUEST_TIMEOUT_MS = 10_000;

export interface RequestArgs {
  path: string;
  method: string;
  token?: string;
  body?: unknown;
  sessionGeneration: number;
  isCurrent: (generation: number) => boolean;
  signal?: AbortSignal;
}

export interface RequestResult<T> {
  status: number;
  body: T | null;
  discarded: boolean;
}

function combineSignals(signals: AbortSignal[]): AbortSignal {
  const controller = new AbortController();
  const abort = () => {
    if (!controller.signal.aborted) {
      controller.abort();
    }
  };
  for (const signal of signals) {
    if (signal.aborted) {
      abort();
      break;
    }
    signal.addEventListener("abort", abort, { once: true });
  }
  return controller.signal;
}

export async function request<T>(args: RequestArgs): Promise<RequestResult<T>> {
  const path = args.path.startsWith("/") ? args.path : `/${args.path}`;
  if (path.includes("?") || path.includes("#")) {
    throw new Error("The request path must not include a query or fragment.");
  }

  const headers = new Headers();
  if (args.body !== undefined) {
    headers.set("Content-Type", "application/json");
  }
  if (args.token) {
    headers.set("Authorization", `Bearer ${args.token}`);
  }

  const timeout = new AbortController();
  const timer = setTimeout(() => timeout.abort(), REQUEST_TIMEOUT_MS);
  const signal = combineSignals(args.signal ? [timeout.signal, args.signal] : [timeout.signal]);

  try {
    const response = await fetch(`${apiBasePath}${path}`, {
      method: args.method,
      headers,
      body: args.body === undefined ? undefined : JSON.stringify(args.body),
      signal,
    });

    if (!args.isCurrent(args.sessionGeneration) || args.signal?.aborted) {
      return { status: response.status, body: null, discarded: true };
    }

    if (response.status === 204) {
      return { status: response.status, body: null, discarded: false };
    }

    const text = await response.text();
    if (!args.isCurrent(args.sessionGeneration) || args.signal?.aborted) {
      return { status: response.status, body: null, discarded: true };
    }

    const body = text ? (JSON.parse(text) as T) : null;
    return { status: response.status, body, discarded: false };
  } catch {
    if (!args.isCurrent(args.sessionGeneration) || args.signal?.aborted) {
      return { status: 0, body: null, discarded: true };
    }
    return { status: 0, body: null, discarded: false };
  } finally {
    clearTimeout(timer);
  }
}
