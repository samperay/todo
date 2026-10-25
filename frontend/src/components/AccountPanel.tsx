import { useState } from "react";

interface AccountPanelProps {
  accountId: string | null;
  token: string | null;
  revealToken: boolean;
  notice: string | null;
  onCreate: () => void;
  onLogout: () => void;
  onPaste: (token: string) => void;
}

export function AccountPanel({
  accountId,
  token,
  revealToken,
  notice,
  onCreate,
  onLogout,
  onPaste,
}: AccountPanelProps) {
  const [draft, setDraft] = useState("");

  return (
    <section>
      <h1>Todo</h1>
      {token === null ? <p>The service cannot replace a lost token.</p> : null}
      {notice ? <p role="status">{notice}</p> : null}
      {revealToken && token ? (
        <div data-testid="token-reveal">
          <p>{accountId}</p>
          <p>{token}</p>
        </div>
      ) : null}
      {accountId && !revealToken ? <p>Account {accountId}</p> : null}
      {token ? (
        <button type="button" onClick={onLogout}>
          Log out
        </button>
      ) : (
        <button type="button" onClick={onCreate}>
          Create account
        </button>
      )}
      <form
        onSubmit={(event) => {
          event.preventDefault();
          onPaste(draft);
          setDraft("");
        }}
      >
        <label>
          Saved token
          <input
            value={draft}
            onChange={(event) => {
              setDraft(event.target.value);
            }}
          />
        </label>
        <button type="submit">Use saved token</button>
      </form>
    </section>
  );
}
