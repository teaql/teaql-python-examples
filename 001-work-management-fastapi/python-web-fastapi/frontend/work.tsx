import type { Template } from "./templates";
import type { Event } from "./history";
import type { Homes } from "./placements";
import type { DependencyData } from "./dependencies";
import type { DiscussionData } from "./discussion";
import type { Dropdown } from "./fields";
import type { Section } from "./board";
import { useState } from "react";

export type Person = { id: number; name: string; email: string };
export type Project = {
  id: number;
  access: string;
  sections: Section[];
  fields: Dropdown[];
  templates: Template[];
  shiftDates: boolean;
  members: (Person & { role: string; owner: boolean; me: boolean })[];
  candidates: Person[];
};
export type Task = Homes &
  DependencyData &
  DiscussionData & {
    occurrences: { label: string; href: string; due: string | null }[];
    history: Event[];
    decision: string | null;
    canDecide: boolean;
    id: number;
    access: string;
  };
type Values = Record<string, string | number | boolean | null>;

export async function change(
  name: string,
  target: number,
  values: Values,
  key: string,
) {
  const response = await fetch("/api/change/" + name + "/" + target, {
    method: "POST",
    headers: { "Content-Type": "application/json", "Idempotency-Key": key },
    body: JSON.stringify(values),
    cache: "no-store",
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.detail || "Unable to save");
  return result as { location: string };
}

export function Mutation({
  name,
  target,
  values = {},
  label,
  children,
  onSuccess,
}: {
  name: string;
  target: number;
  values?: Values;
  label: string;
  children?: React.ReactNode;
  onSuccess?: () => void;
}) {
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [key, setKey] = useState(() => crypto.randomUUID());
  return (
    <form
      onSubmit={async (event) => {
        event.preventDefault();
        if (busy) return;
        const data = Object.fromEntries(
          new FormData(event.currentTarget),
        ) as Record<string, string>;
        setBusy(true);
        setError("");
        try {
          const res = await change(name, target, { ...values, ...data }, key);
          setKey(crypto.randomUUID());
          if (onSuccess) onSuccess();
          else location.assign(res.location);
        } catch (e) {
          setError((e as Error).message);
        } finally {
          setBusy(false);
        }
      }}
    >
      {children}
      <button disabled={busy}>{label}</button>
      {error && <p role="alert">{error}</p>}
    </form>
  );
}

export function Members({
  project,
  refresh,
}: {
  project: Project;
  refresh: () => void;
}) {
  const [open, setOpen] = useState(false);
  return (
    <section>
      <button onClick={() => setOpen(!open)} aria-expanded={open}>
        Members
      </button>
      {open && (
        <>
          <h2>Project members</h2>
          <ul>
            {project.members.map((p) => (
              <li key={p.id}>
                {p.name} ({p.email})
                <span>
                  {" "}
                  ·{" "}
                  {p.owner
                    ? "Owner"
                    : p.role === "comment"
                      ? "Comment-only"
                      : "Full access"}
                </span>
                {project.access === "full" && !p.owner && !p.me && (
                  <Mutation
                    name="member-role"
                    target={project.id}
                    values={{
                      account: p.id,
                      role: p.role === "full" ? "comment" : "full",
                    }}
                    label={
                      p.role === "full"
                        ? "Make comment-only"
                        : "Give full access"
                    }
                    onSuccess={refresh}
                  />
                )}
                {project.access === "full" && !p.owner && (
                  <Mutation
                    name="member-remove"
                    target={project.id}
                    values={{ account: p.id }}
                    label={"Remove " + p.name}
                    onSuccess={refresh}
                  />
                )}
              </li>
            ))}
          </ul>
          {project.access === "full" && project.candidates.length > 0 && (
            <Mutation
              name="member-add"
              target={project.id}
              label="Add member"
              onSuccess={refresh}
            >
              <label>
                Workspace member{" "}
                <select name="account">
                  {project.candidates.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.name} ({p.email})
                    </option>
                  ))}
                </select>
              </label>
            </Mutation>
          )}
        </>
      )}
    </section>
  );
}
