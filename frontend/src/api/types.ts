export const TITLE_MAX_LENGTH = 200;
export const DESCRIPTION_MAX_LENGTH = 2000;

export type Priority = "low" | "medium" | "high";

export interface UserCreated {
  id: string;
  token: string;
}

export interface Todo {
  id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: Priority;
  created_at: string;
  updated_at: string;
}

/** Title is required after trim and is at most 200 characters. */
export interface TodoCreate {
  title: string;
  description?: string | null;
  priority?: Priority;
}

/** Description, when present, is at most 2000 characters. */
export interface TodoUpdate {
  title?: string;
  description?: string | null;
  priority?: Priority;
}
