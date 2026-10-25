import { request } from "./client";
import type { Priority, Todo } from "./types";

export interface ListTodosResult {
  discarded: boolean;
  status: number;
  todos: Todo[] | null;
}

function isPriority(value: unknown): value is Priority {
  return value === "low" || value === "medium" || value === "high";
}

function isTodo(value: unknown): value is Todo {
  if (!value || typeof value !== "object") {
    return false;
  }
  const record = value as Record<string, unknown>;
  return (
    typeof record.id === "string" &&
    typeof record.title === "string" &&
    (record.description === null || typeof record.description === "string") &&
    typeof record.completed === "boolean" &&
    isPriority(record.priority) &&
    typeof record.created_at === "string" &&
    typeof record.updated_at === "string"
  );
}

export async function listTodos(
  token: string,
  sessionGeneration: number,
  isCurrent: (generation: number) => boolean,
  signal?: AbortSignal,
): Promise<ListTodosResult> {
  const result = await request<unknown>({
    path: "/todos",
    method: "GET",
    token,
    sessionGeneration,
    isCurrent,
    signal,
  });
  if (result.discarded) {
    return { discarded: true, status: result.status, todos: null };
  }
  if (result.status === 200 && Array.isArray(result.body) && result.body.every(isTodo)) {
    return { discarded: false, status: result.status, todos: result.body };
  }
  return { discarded: false, status: result.status, todos: null };
}
