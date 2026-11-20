import { Fragment, useEffect, useRef, useState, type FormEvent } from "react";
import { Inbox, InboxLink, type Notice } from "./inbox";
import { Templates } from "./templates";
import { History } from "./history";
import { Placements } from "./placements";
import { Dependencies, ShiftDates } from "./dependencies";
import { Discussion } from "./discussion";
import { Fields } from "./fields";
import { Board } from "./board";
import { Members, Mutation, type Project, type Task } from "./work";
import { createRoot } from "react-dom/client";
import { flushSync } from "react-dom";

type Field = {
  name: string;
  label: string;
  kind: "text" | "multiline" | "date" | "boolean" | "number" | "reference";
  value: string | number | boolean | null;
  required: boolean;
  readonly?: boolean;
  options: { id: string; label: string }[];
};
type RecordForm = {
  label: string;
  fields: Field[];
  action: string | null;
  submit: string;
  delete: string | null;
  commandKey: string | null;
};
type Collection = {
  label: string;
  create: string | null;
  links?: { href: string; label: string }[];
  columns?: string[];
  groups?: { label: string; rows: { href: string; cells: string[] }[] }[];
};
type View =
  | { kind: "login"; signup: boolean }
  | { kind: "signup" }
  | { kind: "saved" }
  | { kind: "inbox"; title: string; items: Notice[]; unread: number }
  | {
      kind: "deleted";
      title: string;
      items: { id: number; title: string; canRestore: boolean }[];
    }
  | {
      kind: "tasks";
      title: string;
      items: {
        href: string;
        label: string;
        project: string;
        due: string | null;
      }[];
    }
  | { kind: "home"; trace?: string; collections: Collection[] }
  | {
      kind: "record";
      title: string;
      form: RecordForm;
      collections: Collection[];
      project?: Project;
      task?: Task;
    };

class HttpFailure extends Error {
  constructor(
    readonly status: number,
    message: string,
  ) {
    super(message);
  }
}

async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch("/api" + path, { cache: "no-store", ...init });
  const data = await response.json();
  if (!response.ok) {
    const detail =
      typeof data.detail === "string"
        ? data.detail
        : "Request failed (" + response.status + ")";
    throw new HttpFailure(response.status, detail);
  }
  return data;
}

type Values = Record<string, string | boolean>;
function ActionForm({
  path,
  commandKey,
  children,
  submit,
  initial,
}: {
  path: string;
  commandKey?: string | null;
  children?: React.ReactNode;
  submit: string;
  initial?: Field[];
}) {
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const pending = useRef(false);
  const retry = useRef<{ payload: string; key: string } | null>(null);
  async function send(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (pending.current) return;
    pending.current = true;
    setBusy(true);
    setError("");
    const form = event.currentTarget;
    const values: Values = {};
    for (const [name, value] of new FormData(form))
      values[name] = String(value);
    for (const box of form.querySelectorAll<HTMLInputElement>(
      'input[type="checkbox"]',
    ))
      values[box.name] = box.checked;
    if (initial) {
      for (const f of initial) {
        const before = f.kind === "boolean" ? !!f.value : String(f.value ?? "");
        if (f.readonly || values[f.name] === before) delete values[f.name];
      }
    }
    const choices: Values = {};
    for (const key of Object.keys(values))
      if (key.startsWith("choice_")) {
        choices[key.slice(7)] = values[key];
        delete values[key];
      }
    if (Object.keys(choices).length)
      values.custom_fields = JSON.stringify(choices);
    const project = new URLSearchParams(location.search).get("project");
    if (initial && project) values.context_project = project;
    try {
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
      };
      const payload = JSON.stringify(values);
      if (!retry.current || retry.current.payload !== payload)
        retry.current = { payload, key: commandKey || crypto.randomUUID() };
      headers["Idempotency-Key"] = retry.current.key;
      const result = await api<{ location: string }>(path, {
        method: "POST",
        headers,
        body: payload,
      });
      window.location.assign(result.location);
    } catch (cause) {
      setError(
        cause instanceof Error ? cause.message : "Could not save the change.",
      );
      pending.current = false;
      setBusy(false);
    }
  }
  return (
    <form
      method="post"
      action={"/api" + path}
      onSubmit={send}
      className="teaql-fields"
    >
      {children}
      {error && <p role="alert">{error}</p>}
      <button disabled={busy}>{submit}</button>
    </form>
  );
}

function Auth({ view }: { view: Extract<View, { kind: "signup" | "login" }> }) {
  const signup = view.kind === "signup";
  const title = signup ? "Sign up" : "Sign in";
  return (
    <>
      <h1>{title}</h1>
      <ActionForm path={signup ? "/signup" : "/login"} submit={title}>
        {signup && (
          <label>
            Name{" "}
            <input name="name" autoComplete="name" maxLength={120} required />
          </label>
        )}
        <label>
          Email{" "}
          <input
            name="email"
            type="email"
            autoComplete="email"
            maxLength={254}
            required
          />
        </label>
        <label>
          Password{" "}
          <input
            name="password"
            type="password"
            autoComplete={signup ? "new-password" : "current-password"}
            maxLength={256}
            minLength={signup ? 6 : undefined}
            required
          />
        </label>
      </ActionForm>
      {signup ? (
        <p>
          <a href="/">Sign in</a>
        </p>
      ) : (
        view.signup && (
          <p>
            <a href="/signup">Sign up</a>
          </p>
        )
      )}
    </>
  );
}

function Control({
  field,
  value,
  onChange,
}: {
  field: Field;
  value: string | boolean;
  onChange: (value: string | boolean) => void;
}) {
  const { name, kind, required, readonly } = field;
  const labelledBy = "record-label-" + name;
  const props = {
    name,
    required,
    id: "record-field-" + name,
    "aria-labelledby": labelledBy,
    disabled: readonly,
    value: String(value),
  };
  if (kind === "reference")
    return (
      <select {...props} onChange={(e) => onChange(e.target.value)}>
        <option value="">Choose…</option>
        {field.options.map((option) => (
          <option key={option.id} value={option.id}>
            {option.label}
          </option>
        ))}
      </select>
    );
  if (kind === "boolean")
    return (
      <input
        name={name}
        id={"record-field-" + name}
        aria-labelledby={labelledBy}
        type="checkbox"
        disabled={readonly}
        checked={value === true}
        onChange={(e) => onChange(e.target.checked)}
      />
    );
  if (kind === "multiline")
    return (
      <textarea
        {...props}
        maxLength={4000}
        onChange={(e) => onChange(e.target.value)}
      />
    );
  return (
    <input
      {...props}
      type={kind}
      step={kind === "number" ? "any" : undefined}
      maxLength={4000}
      onChange={(e) => onChange(e.target.value)}
    />
  );
}

function RecordEditor({ form }: { form: RecordForm }) {
  const [drafts, setDrafts] = useState<Values>({});
  function text(field: Field) {
    return (
      field.options.find((o) => o.id === String(field.value))?.label ??
      (field.kind === "boolean"
        ? field.value
          ? "Yes"
          : "No"
        : String(field.value ?? ""))
    );
  }
  return (
    <>
      {form.action ? (
        <ActionForm
          path={form.action}
          commandKey={form.commandKey}
          submit={form.submit}
          initial={form.commandKey ? undefined : form.fields}
        >
          {form.fields.map((f) => {
            const saved =
              f.kind === "boolean" ? !!f.value : String(f.value ?? "");
            return (
              <label key={f.name} htmlFor={"record-field-" + f.name}>
                <span id={"record-label-" + f.name}>{f.label}</span>{" "}
                <Control
                  field={f}
                  value={f.readonly ? saved : (drafts[f.name] ?? saved)}
                  onChange={(v) =>
                    setDrafts((prev) => {
                      const next = { ...prev };
                      if (v === saved) delete next[f.name];
                      else next[f.name] = v;
                      return next;
                    })
                  }
                />
              </label>
            );
          })}
        </ActionForm>
      ) : (
        <dl>
          {form.fields.map((f) => (
            <Fragment key={f.name}>
              <dt>{f.label}</dt>
              <dd>{text(f)}</dd>
            </Fragment>
          ))}
        </dl>
      )}
      {form.delete && (
        <ActionForm path={form.delete} submit={"Delete " + form.label} />
      )}
    </>
  );
}

function Collections({ items }: { items: Collection[] }) {
  return (
    <>
      {items.map((item, index) => (
        <section key={index}>
          <h2>{item.label}</h2>
          {item.create && (
            <p>
              <a href={item.create}>Create {item.label}</a>
            </p>
          )}
          {item.links && (
            <ul>
              {item.links.map((link) => (
                <li key={link.href}>
                  <a href={link.href}>{link.label}</a>
                </li>
              ))}
            </ul>
          )}
          {item.groups?.map((group, index) => (
            <div key={index}>
              <h3>{group.label}</h3>
              <div className="teaql-table">
                <table>
                  <thead>
                    <tr>
                      {item.columns?.map((label, i) => (
                        <th key={i} scope="col">
                          {label}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {group.rows.map((row) => (
                      <tr key={row.href}>
                        {row.cells.map((cell, i) => (
                          <td key={i}>
                            {i === 0 ? <a href={row.href}>{cell}</a> : cell}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ))}
        </section>
      ))}
    </>
  );
}

function App({ view: initial }: { view: View }) {
  const [view, setView] = useState(initial);
  const [syncError, setSyncError] = useState("");
  const latestRequest = useRef(0);
  const refreshing = useRef(false);
  async function refresh() {
    const request = ++latestRequest.current;
    refreshing.current = true;
    try {
      const next = await api<View>(location.pathname + location.search);
      if (request !== latestRequest.current) return;
      setSyncError("");
      setView(next);
    } catch (error) {
      if (request !== latestRequest.current) return;
      if (error instanceof HttpFailure && error.status === 401)
        location.assign("/");
      else if (
        error instanceof HttpFailure &&
        [403, 404].includes(error.status)
      )
        location.assign("/my-tasks");
      else
        setSyncError(
          "Live updates paused. Your edits are still here. Retrying…",
        );
    } finally {
      if (request === latestRequest.current) refreshing.current = false;
    }
  }
  useEffect(() => {
    const live =
      initial.kind === "inbox" ||
      (initial.kind === "record" && !!(initial.project || initial.task));
    if (!live) return;
    const poll = () => {
      if (!document.hidden && !refreshing.current) void refresh();
    };
    const timer = window.setInterval(poll, 2500);
    document.addEventListener("visibilitychange", poll);
    return () => {
      window.clearInterval(timer);
      document.removeEventListener("visibilitychange", poll);
    };
  }, [initial]);
  switch (view.kind) {
    case "login":
    case "signup":
      return <Auth view={view} />;
    case "home":
      return (
        <>
          <h1>Your records</h1>
          <a href="/my-tasks">My Tasks</a> <a href="/deleted">Deleted tasks</a>{" "}
          <InboxLink />
          <span hidden data-teaql-home-trace={view.trace} />
          <Collections items={view.collections} />
          <ActionForm path="/logout" submit="Sign out" />
        </>
      );
    case "inbox":
      return (
        <>
          {syncError && <p role="status">{syncError}</p>}
          <Inbox items={view.items} unread={view.unread} refresh={refresh} />
        </>
      );
    case "deleted":
      return (
        <>
          <a href="/">Your records</a>
          <h1>Deleted tasks</h1>
          <ul>
            {view.items.map((i) => (
              <li key={i.id}>
                <span>{i.title}</span>
                {i.canRestore && (
                  <>
                    <Mutation
                      name="task-restore"
                      target={i.id}
                      label="Restore"
                      onSuccess={refresh}
                    />
                    <details>
                      <summary>Delete permanently</summary>
                      <Mutation
                        name="task-purge"
                        target={i.id}
                        label="Confirm permanent deletion"
                        onSuccess={refresh}
                      />
                    </details>
                  </>
                )}
              </li>
            ))}
          </ul>
        </>
      );
    case "tasks":
      return (
        <>
          <a href="/">Your records</a>
          <h1>{view.title}</h1>
          <ul>
            {view.items.map((i) => (
              <li key={i.href}>
                <a href={i.href}>{i.label}</a> {i.project} {i.due}
              </li>
            ))}
          </ul>
        </>
      );
    case "saved":
      return (
        <>
          <h1>Saved</h1>
          <p>Your change has been saved.</p>
          <a href="/">Your records</a>
        </>
      );
    case "record":
      return (
        <>
          <nav className="workspace-navigation" aria-label="Workspace">
            <a href="/">Your records</a>
            <a href="/my-tasks">My Tasks</a>
            <a href="/deleted">Deleted tasks</a>
            <InboxLink />
          </nav>
          <h1>{view.title}</h1>
          {syncError && <p role="status">{syncError}</p>}
          {view.project && (
            <div className="project-tools">
              <Members project={view.project} refresh={refresh} />
              <Fields project={view.project} refresh={refresh} />
              <ShiftDates project={view.project} refresh={refresh} />
              <Templates project={view.project} refresh={refresh} />
            </div>
          )}
          {(!view.project ||
            view.form.action ||
            view.form.delete ||
            view.form.fields.length !== 1 ||
            String(view.form.fields[0].value) !== view.title) && (
            <RecordEditor form={view.form} />
          )}
          {view.task && (
            <>
              {view.task.decision && (
                <section>
                  <h2>Approval</h2>
                  <p>{view.task.decision}</p>
                  {view.task.canDecide &&
                    [
                      ["approved", "Approve"],
                      ["rejected", "Reject"],
                      ["changes", "Request changes"],
                    ].map(([decision, label]) => (
                      <Mutation
                        key={decision}
                        name="approval-decision"
                        target={view.task!.id}
                        values={{ decision }}
                        label={label}
                        onSuccess={refresh}
                      />
                    ))}
                </section>
              )}
              {view.task.occurrences.map((o) => (
                <p key={o.href}>
                  <a href={o.href}>{o.label}</a>
                  {o.due && (
                    <>
                      {" "}
                      · <time>{o.due}</time>
                    </>
                  )}
                </p>
              ))}
              <Placements task={view.task} refresh={refresh} />
              <Dependencies task={view.task} refresh={refresh} />
              <Discussion task={view.task} refresh={refresh} />
              <History task={view.task} />
            </>
          )}
          {view.project ? (
            <Board
              project={view.project}
              refresh={refresh}
              create={view.collections.find((c) => c.create)?.create ?? null}
            />
          ) : (
            <Collections items={view.collections} />
          )}
        </>
      );
  }
}

export function mount(view: View) {
  const host = document.getElementById("root")!;
  document.title =
    view.kind === "record" ||
    view.kind === "tasks" ||
    view.kind === "deleted" ||
    view.kind === "inbox"
      ? view.title
      : {
          login: "Sign in",
          signup: "Sign up",
          home: "Your records",
          saved: "Saved",
        }[view.kind];
  const root = createRoot(host);
  flushSync(() => root.render(<App view={view} />));
  host.removeAttribute("aria-busy");
}
