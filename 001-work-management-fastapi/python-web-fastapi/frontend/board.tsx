import { useState } from "react";
import { change, Mutation, type Project } from "./work";

export type Card = {
  id: number;
  decision: string | null;
  href: string;
  title: string;
  done: boolean;
  assignee: string | null;
  due: string | null;
  values?: string[];
};
export type Section = { id: number; name: string; tasks: Card[] };

export function Board({
  project,
  refresh,
  create,
}: {
  project: Project;
  refresh: () => void;
  create: string | null;
}) {
  const [board, setBoard] = useState(false);
  const [error, setError] = useState("");
  const [add, setAdd] = useState(false);
  const [edit, setEdit] = useState<number | null>(null);
  const writable = project.access === "full";
  async function move(tid: number, sid: number, index: number) {
    try {
      await change(
        "task-move",
        tid,
        { section: sid, position: index },
        crypto.randomUUID(),
      );
      refresh();
    } catch (e) {
      setError((e as Error).message);
    }
  }
  return (
    <section>
      <div className="board-tools">
        <nav aria-label="Project view">
          <button aria-pressed={!board} onClick={() => setBoard(false)}>
            List
          </button>
          <button aria-pressed={board} onClick={() => setBoard(true)}>
            Board
          </button>
        </nav>
        {create && (
          <a className="create-task" href={create}>
            Create Task
          </a>
        )}
        {writable && <button onClick={() => setAdd(!add)}>Add section</button>}
      </div>
      {add && (
        <Mutation
          name="section-add"
          target={project.id}
          label="Create section"
          onSuccess={() => {
            setAdd(false);
            refresh();
          }}
        >
          <label>
            Section name <input required maxLength={200} name="name" />
          </label>
        </Mutation>
      )}
      {error && <p role="alert">{error}</p>}
      <div className={board ? "board-grid" : "project-list"}>
        {project.sections.map((s, si) => (
          <section
            className={board ? "board-col" : "list-section"}
            key={s.id}
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => {
              e.preventDefault();
              const tid = Number(e.dataTransfer.getData("text/plain"));
              if (tid && writable) void move(tid, s.id, s.tasks.length);
            }}
          >
            <h3>{s.name}</h3>
            {writable && (
              <button
                onClick={() => setEdit(edit === s.id ? null : s.id)}
                aria-label={"Manage " + s.name}
              >
                Section settings
              </button>
            )}
            {edit === s.id && (
              <>
                <Mutation
                  name="section-edit"
                  target={s.id}
                  label="Save section"
                  onSuccess={() => {
                    setEdit(null);
                    refresh();
                  }}
                >
                  <label>
                    Section name{" "}
                    <input name="name" defaultValue={s.name} required />
                  </label>
                  <label>
                    Section position{" "}
                    <select name="position" defaultValue={si}>
                      {project.sections.map((o, i) => (
                        <option key={o.id} value={i}>
                          {i + 1}
                        </option>
                      ))}
                    </select>
                  </label>
                </Mutation>
                <Mutation
                  name="section-delete"
                  target={s.id}
                  label="Delete section"
                  onSuccess={() => {
                    setEdit(null);
                    refresh();
                  }}
                />
              </>
            )}
            <div className="board-cards" data-dropzone>
              {s.tasks.map((t, ti) => (
                <article
                  key={t.id}
                  draggable={writable}
                  onDragStart={(e) =>
                    e.dataTransfer.setData("text/plain", String(t.id))
                  }
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    const tid = Number(e.dataTransfer.getData("text/plain"));
                    if (tid && writable) void move(tid, s.id, ti);
                  }}
                >
                  <a href={t.href}>{t.title}</a>
                  <div className="card-metadata">
                    <span>{t.decision || (t.done ? "Completed" : "Open")}</span>
                    {t.assignee && (
                      <span aria-label={"Assigned to " + t.assignee}>
                        {t.assignee}
                      </span>
                    )}
                    {t.due && (
                      <time dateTime={t.due} aria-label={"Due " + t.due}>
                        {t.due}
                      </time>
                    )}
                    {t.values?.map((v) => (
                      <span key={v}>{v}</span>
                    ))}
                  </div>
                  {writable && (
                    <details>
                      <summary>Move task</summary>
                      <Mutation
                        name="task-move"
                        target={t.id}
                        label="Move task"
                        onSuccess={refresh}
                      >
                        <label>
                          Section{" "}
                          <select name="section" defaultValue={s.id}>
                            {project.sections.map((o) => (
                              <option key={o.id} value={o.id}>
                                {o.name}
                              </option>
                            ))}
                          </select>
                        </label>
                        <label>
                          Position{" "}
                          <input
                            name="position"
                            defaultValue={ti}
                            type="number"
                            min="0"
                          />
                        </label>
                      </Mutation>
                    </details>
                  )}
                </article>
              ))}
            </div>
          </section>
        ))}
      </div>
    </section>
  );
}
