import { AccountPanel } from "./components/AccountPanel";
import { TodoList } from "./components/TodoList";
import { useTodoSession } from "./session/useTodoSession";

export function App() {
  const session = useTodoSession();

  return (
    <main data-testid="app-shell">
      <AccountPanel
        accountId={session.accountId}
        token={session.token}
        revealToken={session.revealToken}
        notice={session.notice}
        onCreate={() => {
          void session.createAccount();
        }}
        onLogout={session.logout}
        onPaste={(value) => {
          void session.pasteToken(value);
        }}
      />
      <TodoList todos={session.todos} listStatus={session.listStatus} notice={session.notice} />
    </main>
  );
}
