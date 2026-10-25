# Contract: Screen Behavior

One page. No route table. Text from the person is rendered as React text, never as HTML.

## Regions

| Region | Behavior |
|--------|----------|
| Account | Create account with no name, email, or password. Show `id` and the token once after create. Paste a saved token. Logout removes local keys only. |
| Notice | One failure notice, or nothing. Not used for the empty list. |
| Create | Title, optional description, priority select of low, medium, high, or unset. |
| Filter | All, pending, completed. Initial value is all. Changing it does not fetch. |
| List | Loading, empty account, empty filter, error, or rows in service order. |
| Row | Title, description when present, completed, priority, created time, updated time. Complete, reopen, edit, delete. |
| Editor | Title, description, priority. Save sends only changes. Cancel sends nothing. |
| Delete | Asks for confirmation. Cancel leaves the row. |

## Loading and double submit

A loading indicator is visible while account creation, list, create, edit save, complete, reopen, or delete is in flight.

The same submit does not fire again until that request finishes. A second edit of the same todo does not open while its editor is open or its save is in flight. An edit of a different todo may open.

## Filter

| Filter | Rows |
|--------|------|
| all | The full array |
| pending | `completed` is false |
| completed | `completed` is true |

Order inside the filter is the relative order from `GET /api/v1/todos`. No `completed` query parameter is sent.

## Account visibility

These actions leave zero todos from the previous credential on screen:

- Logout
- Successful create-account
- Paste of a token
- Any `401`

Each of those actions increments the session generation and aborts requests from the previous generation. The following list request then fills the screen for the new credential, or shows the empty state, or shows the unauthenticated notice.

A response that belongs to an older generation does not change the stored list, the editor, or the notice. That remains true when the older response arrives after the current generation's request has completed. The account-session test asserts the stored records and the requests. It does not require row markup. The list test then asserts the rendered titles: the previous account's titles stay absent. Switching accounts must not expose stale account data in stored state or on screen.

## Text

A title or description that contains markup or script text is visible as characters. It does not run. The token is not shown except on the one-time reveal and in the paste field.

## Out of this screen

No single-todo page, search, paging, due dates, tags, bulk edit, or server-side filter.
