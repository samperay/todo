import type { ListStatus } from "../session/useTodoSession";
import type { Todo } from "../api/types";
import { TodoItem } from "./TodoItem";

export const LOADING_TODOS = "Loading todos.";
export const EMPTY_ACCOUNT = "This account has no todos.";
export const LIST_FAILED = "The list could not be loaded.";

export function TodoList({
  todos,
  listStatus,
  notice,
}: {
  todos: Todo[];
  listStatus: ListStatus;
  notice: string | null;
}) {
  if (listStatus === "loading") {
    return <p role="status">{LOADING_TODOS}</p>;
  }
  if (listStatus === "error") {
    if (notice) {
      return null;
    }
    return <p role="alert">{LIST_FAILED}</p>;
  }
  if (listStatus !== "ready") {
    return null;
  }
  if (todos.length === 0) {
    return <p>{EMPTY_ACCOUNT}</p>;
  }
  return (
    <ol className="todo-list">
      {todos.map((todo) => (
        <li key={todo.id}>
          <TodoItem todo={todo} />
        </li>
      ))}
    </ol>
  );
}
