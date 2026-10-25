import { request } from "./client";
import type { UserCreated } from "./types";

export interface CreateAccountResult {
  discarded: boolean;
  status: number;
  user: UserCreated | null;
}

function isUserCreated(value: unknown): value is UserCreated {
  if (!value || typeof value !== "object") {
    return false;
  }
  const record = value as Record<string, unknown>;
  return typeof record.id === "string" && typeof record.token === "string";
}

export async function createAccount(
  sessionGeneration: number,
  isCurrent: (generation: number) => boolean,
  signal?: AbortSignal,
): Promise<CreateAccountResult> {
  const result = await request<unknown>({
    path: "/users",
    method: "POST",
    sessionGeneration,
    isCurrent,
    signal,
  });
  if (result.discarded) {
    return { discarded: true, status: result.status, user: null };
  }
  if (result.status !== 201 || !isUserCreated(result.body)) {
    return { discarded: false, status: result.status, user: null };
  }
  return {
    discarded: false,
    status: result.status,
    user: { id: result.body.id, token: result.body.token },
  };
}
