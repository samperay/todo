import type { Todo } from "../api/types";

export function TodoItem({ todo }: { todo: Todo }) {
  return (
    <article className="todo-item">
      <h2>{todo.title}</h2>
      {todo.description !== null ? <p>{todo.description}</p> : null}
      <p>{todo.completed ? "Completed" : "Not completed"}</p>
      <p>{todo.priority}</p>
      <p>{todo.created_at}</p>
      <p>{todo.updated_at}</p>
      <p>{todo.id}</p>
    </article>
  );
}
