# Feature Specification: Basic Todo Management

**Feature Branch**: `001-todo-management`

**Created**: 2026-10-02

**Status**: Draft

**Input**: User description: "Implement basic Todo management. A user must be able to create a todo, retrieve a todo by ID, list todos, update a todo, delete a todo, and mark a todo as completed. A todo contains id, title, description, completed, created_at, and updated_at. Title is required. Description is optional. New todos are incomplete by default. Deleting a todo permanently removes it. Do not decide implementation details yet. Focus on functional requirements and expected behaviour."

## Clarifications

### Session 2026-10-02

- Q: Who can see and change the todos? → A: Each person has their own todos. They must be identified, and they only see and change their own.
- Q: Can a person mark their own completed todo as incomplete again? → A: Yes, as its own action. The id, title, description, and created time stay the same. The updated time changes.
- Q: If the same person changes one todo twice at the same time, which change is kept? → A: The later change wins. The earlier change is replaced. The person is not warned.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create a todo (Priority: P1)

An identified person adds a todo by supplying a title and, when they have more detail, a description. The new todo starts incomplete, belongs only to that person, receives a unique identifier, and records when it was created and last changed.

**Why this priority**: Nothing else in this feature has value until a todo can be added.

**Independent Test**: As an identified person, create a todo with a title and confirm it is stored as incomplete with an identifier and timestamps. Repeat without a description, then attempt creation without a title and confirm nothing is stored. Confirm a second person cannot see the first person's todo.

**Acceptance Scenarios**:

1. **Given** the user is adding a todo, **When** they provide a title and a description, **Then** a new todo is stored with that title and description, completed set to incomplete, a unique id, and created_at and updated_at set to the time of creation.
2. **Given** the user is adding a todo, **When** they provide a title and omit the description, **Then** the todo is stored as incomplete with no description.
3. **Given** the user is adding a todo, **When** they omit the title or provide only whitespace, **Then** no todo is stored and the user is told that a title is required.
4. **Given** the user is adding a todo, **When** the title is longer than 200 characters or the description is longer than 2,000 characters, **Then** no todo is stored and the user is told which limit was exceeded.
5. **Given** the person is not identified, **When** they try to create a todo, **Then** nothing is stored and they are told they must be identified.
6. **Given** person A created a todo, **When** person B lists or retrieves todos, **Then** person B does not see person A's todo.

---

### User Story 2 - List todos (Priority: P1)

An identified person views every todo they own, including completed ones.

**Why this priority**: Creating a todo only helps if that person can see it afterward. Listing is independently useful as soon as any of their todos exist, including an empty personal collection.

**Independent Test**: With a known set of todos owned by one person, list them and confirm each of that person's todos appears once. Confirm another person's todos are absent. With none of their own stored, confirm the result is an empty collection.

**Acceptance Scenarios**:

1. **Given** an identified person owns one or more todos, **When** they list todos, **Then** every todo they own is returned once with id, title, description, completed, created_at, and updated_at, and no one else's todos are included.
2. **Given** an identified person owns no todos, **When** they list todos, **Then** the result is an empty collection even if other people have todos.
3. **Given** an identified person's todos were created at different times, **When** they list todos, **Then** their todos are ordered newest first by created_at.
4. **Given** the person is not identified, **When** they list todos, **Then** nothing is returned and they are told they must be identified.

---

### User Story 3 - Mark a todo as completed (Priority: P1)

A person marks an existing todo complete. The todo stays in the collection and shows as completed wherever it is viewed.

**Why this priority**: Recording that work is done is the outcome a todo list exists to support, and it can be demonstrated with a single created todo.

**Independent Test**: Create an incomplete todo, mark it completed, then retrieve it and list todos. Both views show it completed, with the same title, description, and created_at.

**Acceptance Scenarios**:

1. **Given** an incomplete todo exists, **When** the user marks it completed, **Then** completed becomes true, title, description, id, and created_at stay the same, and updated_at becomes the time of completion.
2. **Given** a todo is already completed, **When** the user marks it completed again, **Then** it stays completed and no field changes.
3. **Given** no todo the person owns has the requested id, including when that id belongs to someone else, **When** the user marks it completed, **Then** the user is told the todo does not exist and nothing is stored.
4. **Given** the person is not identified, **When** they mark a todo completed, **Then** nothing changes and they are told they must be identified.

---

### User Story 4 - Retrieve a todo by ID (Priority: P2)

A person opens one todo using its identifier and sees its current details.

**Why this priority**: Direct lookup confirms a single item. Create, list, and complete already deliver a usable list without it.

**Independent Test**: Create a todo, retrieve it by the returned id, and confirm the same fields. Request an id that was never issued and confirm the user is told it does not exist.

**Acceptance Scenarios**:

1. **Given** a todo exists, **When** the user retrieves it by its id, **Then** they receive that todo’s id, title, description, completed, created_at, and updated_at.
2. **Given** no todo the person owns has the requested id, including when that id belongs to someone else, **When** the user retrieves it, **Then** they are told the todo does not exist, and no todo is created or changed.
3. **Given** the person is not identified, **When** they retrieve a todo, **Then** nothing is returned and they are told they must be identified.

---

### User Story 5 - Update a todo (Priority: P2)

A person changes the title, the description, or both on an existing todo. This action does not change whether the todo is completed.

**Why this priority**: Wording often needs correction after creation, but the collection is already usable with the original text.

**Independent Test**: Create a todo, change its title and description, then retrieve it. The text matches the change, completed and created_at are unchanged, and updated_at is the time of the update.

**Acceptance Scenarios**:

1. **Given** a todo exists, **When** the user updates its title and description, **Then** those fields change, completed and created_at stay the same, and updated_at becomes the time of the update.
2. **Given** a todo exists, **When** the user updates only the title, **Then** the description is unchanged.
3. **Given** a todo exists, **When** the user updates only the description, including clearing it, **Then** the title is unchanged and the description becomes the supplied value, or no description when cleared.
4. **Given** a todo exists, **When** the user sets the title to empty or whitespace, **Then** the todo is unchanged and the user is told that a title is required.
5. **Given** a todo exists, **When** the user sets a title longer than 200 characters or a description longer than 2,000 characters, **Then** the todo is unchanged and the user is told which limit was exceeded.
6. **Given** no todo the person owns has the requested id, including when that id belongs to someone else, **When** the user updates it, **Then** they are told the todo does not exist and nothing is stored.
7. **Given** the person is not identified, **When** they update a todo, **Then** nothing changes and they are told they must be identified.
8. **Given** two overlapping changes to the same todo, **When** the later change sets the title to "Buy milk" and the description to "2 liters" after an earlier change had set the title to "Buy oat milk", **Then** the stored todo has title "Buy milk" and description "2 liters", the earlier title is not kept, and the person is not warned.

---

### User Story 6 - Delete a todo (Priority: P3)

A person permanently removes a todo. It cannot be retrieved or listed afterward.

**Why this priority**: Cleanup matters, but create, list, complete, retrieve, and update already cover day-to-day use.

**Independent Test**: Create a todo, delete it, then retrieve it and list todos. It is absent from both. Other todos remain. Deleting the same id again reports that it does not exist.

**Acceptance Scenarios**:

1. **Given** a todo exists, **When** the user deletes it, **Then** it is permanently removed and does not appear in a later retrieve or list.
2. **Given** a todo was already deleted or never existed, **When** the user deletes that id, **Then** they are told the todo does not exist.
3. **Given** several todos exist, **When** the user deletes one of their own, **Then** their remaining todos and every other person's todos are unchanged.
4. **Given** the requested id belongs to someone else, **When** the user deletes it, **Then** they are told the todo does not exist and the owner's todo remains.
5. **Given** the person is not identified, **When** they delete a todo, **Then** nothing changes and they are told they must be identified.

---

### User Story 7 - Mark a todo incomplete (Priority: P2)

An identified person marks their own completed todo incomplete again, without changing its id, title, description, or created time.

**Why this priority**: Completing a todo is already useful on its own. This action only corrects a completion. It does not replace delete.

**Independent Test**: Create a todo, mark it completed, then mark it incomplete. Retrieve and list show it incomplete, with the same id, title, description, and created_at, and a later updated_at. Marking an already incomplete todo incomplete again changes nothing.

**Acceptance Scenarios**:

1. **Given** an identified person owns a completed todo, **When** they mark it incomplete, **Then** completed becomes false, id, title, description, and created_at stay the same, updated_at becomes the time of the change, and later retrieve and list show it as incomplete.
2. **Given** the person owns an incomplete todo, **When** they mark it incomplete again, **Then** no field changes.
3. **Given** the id is unknown or belongs to someone else, **When** the person marks it incomplete, **Then** they are told the todo does not exist, nothing changes, and the response does not reveal that another person owns that id.
4. **Given** the person is not identified, **When** they mark a todo incomplete, **Then** nothing changes and they are told they must be identified.

---

### Edge Cases

- A title that is missing, only whitespace, or longer than 200 characters is rejected on create and on update, and stored todos stay as they were.
- A description longer than 2,000 characters is rejected on create and on update, and stored todos stay as they were.
- A description may be omitted on create, left unchanged on a title-only update, or cleared on update. All three mean the todo has no description.
- Two todos may share the same title. The id is the only identity.
- The user cannot choose or change the id. The system assigns it at creation and keeps it until the todo is deleted.
- A person who is not identified cannot create, list, retrieve, update, complete, mark incomplete, or delete. Nothing is stored or changed.
- Retrieve, update, complete, mark incomplete, and delete of an unknown id, or of an id owned by someone else, report that the todo does not exist and do not create a replacement or reveal that another person owns that id.
- Listing never includes another person's todos. Two people may use the same title on their own todos.
- Marking a completed todo completed again does not change updated_at or any other field.
- Completing a todo does not remove it from the list.
- Marking a completed todo incomplete is a separate action from update and from mark completed. It does not change id, title, description, or created_at.
- Marking an already incomplete todo incomplete again does not change updated_at or any other field.
- Marking a todo incomplete does not remove it from the list.
- Deleting a todo is permanent. The same id is not reused, and the item cannot be restored.
- created_at does not change after creation. updated_at changes only when title, description, or completed actually changes, and it is never earlier than created_at.
- On creation, created_at and updated_at are the same moment.
- If two changes to the same todo overlap, only fields the later request supplies change. For a field both requests set, the later successfully processed request wins. A field the later request omits keeps the value from the previous successful update. The person is not warned. A later change does not recreate a todo that was already deleted.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST let an identified person create a todo with a title and an optional description, and that todo MUST belong only to the person who created it.
- **FR-002**: The system MUST reject creation when the title is missing or contains only whitespace, and MUST NOT store a todo in that case.
- **FR-003**: The system MUST store every new todo as incomplete.
- **FR-004**: The system MUST assign each new todo a unique id that the user does not choose and cannot change.
- **FR-005**: The system MUST set created_at and updated_at to the creation time when a todo is created.
- **FR-006**: The system MUST let an identified person list every todo they own, including completed ones, and MUST exclude every todo owned by someone else.
- **FR-007**: The system MUST return an empty collection when an identified person lists todos and they own none, even if other people have todos.
- **FR-008**: The system MUST order a todo list newest first by created_at.
- **FR-009**: The system MUST let a user retrieve one todo by its id.
- **FR-010**: The system MUST tell the person the todo does not exist when they retrieve, update, complete, mark incomplete, or delete an id they do not own, including an id that does not exist and an id owned by someone else, and MUST NOT create a todo or reveal that another person owns that id.
- **FR-011**: The system MUST let a user change the title, the description, or both of an existing todo without changing its completed state or its id.
- **FR-012**: The system MUST modify only fields the request explicitly supplies. Omitted fields MUST retain their stored values. A title-only update MUST leave the description unchanged, and a description-only update MUST leave the title unchanged.
- **FR-013**: The system MUST reject an update that would leave the title missing or whitespace-only, and MUST leave the todo unchanged.
- **FR-014**: The system MUST let a user clear a description so the todo has no description.
- **FR-015**: The system MUST let a user mark an existing incomplete todo as completed.
- **FR-016**: The system MUST keep a completed todo in the collection and show it as completed on later retrieve and list.
- **FR-017**: The system MUST leave a todo unchanged when the user marks an already completed todo as completed again.
- **FR-018**: The system MUST let an identified person mark their own completed todo incomplete. The id, title, description, and created_at MUST stay the same, completed MUST become false, updated_at MUST become the time of that change, and later retrieve and list MUST show it as incomplete.
- **FR-019**: The system MUST let a user permanently delete a todo by id so that later retrieve and list no longer include it.
- **FR-020**: The system MUST leave every todo other than the deleted one unchanged.
- **FR-021**: The system MUST NOT reuse the id of a deleted todo for a later todo.
- **FR-022**: Every create, retrieve, list item, update result, completion result, and mark-incomplete result MUST include id, title, description, completed, created_at, and updated_at.
- **FR-023**: The system MUST keep created_at unchanged after creation, and MUST set updated_at to the time of a change only when title, description, or completed actually changes.
- **FR-024**: The system MUST keep stored todos available after the user leaves and returns, until each todo is deleted.
- **FR-025**: The system MUST accept duplicate titles. Identity is the id, not the title.
- **FR-026**: The system MUST reject a title longer than 200 characters on create and on update, leave stored todos unchanged, and tell the user the title limit was exceeded.
- **FR-027**: The system MUST reject a description longer than 2,000 characters on create and on update, leave stored todos unchanged, and tell the user the description limit was exceeded.
- **FR-028**: The system MUST require an identified person for create, list, retrieve, update, complete, mark incomplete, and delete. When the person is not identified, the system MUST reject the action and MUST NOT store or change a todo.
- **FR-029**: Each todo MUST belong to exactly one person, the person who created it, and that ownership MUST NOT change.
- **FR-030**: The system MUST keep one person's todos unchanged when another person creates, updates, completes, marks incomplete, or deletes their own todos.
- **FR-031**: The system MUST leave a todo unchanged when the owner marks an already incomplete todo incomplete again.
- **FR-032**: When overlapping writes set the same field, the later successfully processed request MUST win for that field. Fields omitted by the later request MUST retain the value produced by previous successful updates. The system MUST NOT warn the person. A later change MUST NOT recreate a todo that has already been deleted.

### Key Entities *(include if feature involves data)*

- **Person**: The domain entity for an identified user of the collection. The HTTP resource name for this entity is `users`. The same person sees the same todos when they return. This feature has no roles beyond that identity. How the person proves who they are is left for planning.
- **Todo**: A single piece of work owned by exactly one Person. It has a stable id, a required title, an optional description, a completed flag that starts false, created_at for when it was added, and updated_at for the last time its title, description, or completed flag changed. Ownership is not one of the fields returned with the todo. Todos owned by different people are not visible to each other.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can add a todo using only a title and then see that todo in the list, in a single pass, without any other required fields.
- **SC-002**: For every todo created during a check, retrieve-by-id returns the same title, description, and completed state that were stored, in 100% of cases.
- **SC-003**: 100% of create and update attempts with a missing title, a whitespace-only title, a title over 200 characters, or a description over 2,000 characters are rejected, and the stored collection is unchanged by those attempts.
- **SC-004**: After a user marks a todo completed, both retrieve and list show that todo as completed, and the todo is still present.
- **SC-005**: After a user deletes a todo, it is absent from retrieve and list, a second delete of that same id reports that it does not exist, and every other todo is unchanged.
- **SC-006**: A list of 100 todos owned by one person returns all 100 of that person's todos, each once, ordered newest first by created_at, and includes none owned by anyone else.
- **SC-007**: An identified person who knows the field names can create, list, retrieve, update, complete, mark incomplete, and delete their own todo on the first attempt without additional guidance.
- **SC-009**: After a person marks their own completed todo incomplete, retrieve and list show it incomplete with the same id, title, description, and created_at, in 100% of cases. Marking an already incomplete todo incomplete again leaves every field unchanged.
- **SC-010**: When two overlapping changes set the same field, the later successfully processed request wins that field in 100% of cases. A field the later request omits keeps the value from the previous successful update. The person receives no conflict warning.
- **SC-008**: In a check with two identified people, neither person's list nor retrieve shows the other's todos, in 100% of cases. An action against the other person's id reports that the todo does not exist, and the owner's todo is unchanged.

## Assumptions

- Each todo belongs only to the identified person who created it. People do not share todos, and there is no role that can see or change another person's todos.
- The same person is recognized when they return, so their todos remain available to them until deleted. How they prove their identity is left for planning.
- A person who is not identified is rejected on every action in this feature. Nothing is stored or changed.
- A title must contain at least one non-whitespace character and must be at most 200 characters.
- A description, when present, must be at most 2,000 characters. Omitting it, sending it empty, or clearing it all mean the todo has no description.
- Update changes title and description only. The completed flag changes only when the owner marks the todo completed or marks it incomplete.
- List returns that person's full collection, including completed todos. Search, filters (including hide-completed), pagination, sorting choices, due dates, priority, tags, subtasks, and bulk actions are out of scope.
- Unknown ids are reported as not found. Delete is not treated as success when the todo is already gone.
- Overlapping changes apply only to fields the later request supplies. That later successful request wins on those fields. Omitted fields keep the stored value. The person is not warned. A change never brings back a deleted todo.
- Timestamps are recorded in a form the user can read and compare. Exact display formatting is left for planning.
- How the user invokes each action (screen, request, or command) is left for planning. This specification defines the behavior of each action, not the interface technology.
