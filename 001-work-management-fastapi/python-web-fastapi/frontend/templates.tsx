import { useState } from "react";
import { Mutation, type Project } from "./work";

type Sub = {
  title: string;
  assignee: number | string | null;
  offset: number | string | null;
};
export type Template = {
  id: number;
  name: string;
  title: string;
  description: string | null;
  assignee: number | null;
  offset: number | null;
  repeat: string;
  approval: boolean;
  choices: Record<string, number>;
  subtasks: Sub[];
};
function TemplateForm({
  project,
  template,
  saved,
}: {
  project: Project;
  template?: Template;
  saved: () => void;
}) {
  const [subs, setSubs] = useState<Sub[]>(template?.subtasks ?? []);
  const [choices, setChoices] = useState<Record<string, number | string>>(
    template?.choices ?? {},
  );
  const people = project.members.map((m) => (
    <option key={m.id} value={m.id}>
      {m.name}
    </option>
  ));
  const patch = (i: number, values: Partial<Sub>) =>
    setSubs(subs.map((s, j) => (j === i ? { ...s, ...values } : s)));
  return (
    <Mutation
      name={template ? "template-update" : "template-create"}
      target={template?.id ?? project.id}
      label="Save template"
      values={{
        choices: JSON.stringify(choices),
        subtasks: JSON.stringify(subs),
      }}
      onSuccess={saved}
    >
      <label>
        Template name{" "}
        <input name="name" required defaultValue={template?.name} />
      </label>
      <label>
        Task title{" "}
        <input name="title" required defaultValue={template?.title} />
      </label>
      <label>
        Initial description{" "}
        <textarea
          name="description"
          defaultValue={template?.description ?? ""}
        />
      </label>
      <label>
        Assignee{" "}
        <select name="assignee" defaultValue={template?.assignee ?? ""}>
          <option value="">Unassigned</option>
          {people}
        </select>
      </label>
      <label>
        Days until due{" "}
        <input
          type="number"
          min="0"
          name="offset"
          defaultValue={template?.offset ?? ""}
        />
      </label>
      <label>
        Repeat{" "}
        <select name="repeat" defaultValue={template?.repeat ?? "none"}>
          {["none", "daily", "weekly", "monthly"].map((x) => (
            <option key={x}>{x}</option>
          ))}
        </select>
      </label>
      <label>
        Task type{" "}
        <select
          name="approval"
          defaultValue={String(template?.approval ?? false)}
        >
          <option value="false">Task</option>
          <option value="true">Approval</option>
        </select>
      </label>
      {project.fields.map((f) => (
        <label key={f.id}>
          {f.name}{" "}
          <select
            value={choices[f.id] ?? ""}
            onChange={(e) => setChoices({ ...choices, [f.id]: e.target.value })}
          >
            <option value="">No value</option>
            {f.options.map((o) => (
              <option key={o.id} value={o.id}>
                {o.name}
              </option>
            ))}
          </select>
        </label>
      ))}
      {subs.map((s, i) => (
        <fieldset key={i}>
          <legend>Subtask {i + 1}</legend>
          <label>
            Subtask title{" "}
            <input
              required
              value={s.title}
              onChange={(e) => patch(i, { title: e.target.value })}
            />
          </label>
          <label>
            Subtask assignee{" "}
            <select
              value={s.assignee ?? ""}
              onChange={(e) => patch(i, { assignee: e.target.value })}
            >
              <option value="">Unassigned</option>
              {people}
            </select>
          </label>
          <label>
            Subtask due offset{" "}
            <input
              type="number"
              min="0"
              value={s.offset ?? ""}
              onChange={(e) => patch(i, { offset: e.target.value })}
            />
          </label>
          <button
            type="button"
            onClick={() => setSubs(subs.filter((_, j) => i !== j))}
          >
            Remove subtask
          </button>
        </fieldset>
      ))}
      <button
        type="button"
        onClick={() =>
          setSubs([...subs, { title: "", assignee: null, offset: null }])
        }
      >
        Add template subtask
      </button>
    </Mutation>
  );
}
function TemplateContents({
  project,
  template,
}: {
  project: Project;
  template: Template;
}) {
  const person = (id: number | string | null) =>
    project.members.find((m) => String(m.id) === String(id))?.name;
  return (
    <details>
      <summary>Template details</summary>
      <dl>
        <dt>Task title</dt>
        <dd>{template.title}</dd>
        {template.description && (
          <>
            <dt>Description</dt>
            <dd>{template.description}</dd>
          </>
        )}
        {template.assignee && (
          <>
            <dt>Assignee</dt>
            <dd>{person(template.assignee)}</dd>
          </>
        )}
        {template.offset !== null && (
          <>
            <dt>Days until due</dt>
            <dd>{template.offset}</dd>
          </>
        )}
        <dt>Task type</dt>
        <dd>{template.approval ? "Approval" : "Task"}</dd>
        {template.repeat !== "none" && (
          <>
            <dt>Repeat</dt>
            <dd>{template.repeat}</dd>
          </>
        )}
        {project.fields.map((f) => {
          const option = f.options.find((o) => o.id === template.choices[f.id]);
          return (
            option && (
              <div key={f.id}>
                <dt>{f.name}</dt>
                <dd>{option.name}</dd>
              </div>
            )
          );
        })}
      </dl>
      {template.subtasks.length > 0 && (
        <>
          <h3>Subtasks</h3>
          <ul>
            {template.subtasks.map((sub, i) => (
              <li key={i}>
                {sub.title}
                {sub.assignee && <> · {person(sub.assignee)}</>}
                {sub.offset != null && <> · Due in {sub.offset} days</>}
              </li>
            ))}
          </ul>
        </>
      )}
    </details>
  );
}

export function Templates({
  project,
  refresh,
}: {
  project: Project;
  refresh: () => void;
}) {
  const [open, setOpen] = useState(false);
  const [editor, setEditor] = useState<number | null>(null);
  return (
    <section>
      <button aria-expanded={open} onClick={() => setOpen(!open)}>
        Task templates
      </button>
      {open && (
        <>
          <h2>Task templates</h2>
          {project.access === "full" && (
            <button onClick={() => setEditor(editor === 0 ? null : 0)}>
              {editor === 0 ? "Cancel" : "New task template"}
            </button>
          )}
          {editor === 0 && (
            <TemplateForm
              project={project}
              saved={() => {
                setEditor(null);
                refresh();
              }}
            />
          )}
          <ul>
            {project.templates.map((t) => (
              <li key={t.id}>
                <span>{t.name}</span>
                <TemplateContents project={project} template={t} />
                {project.access === "full" && (
                  <>
                    <Mutation
                      name="template-use"
                      target={t.id}
                      label="Use template"
                    />
                    <button onClick={() => setEditor(t.id)}>
                      Edit template
                    </button>
                    {editor === t.id && (
                      <TemplateForm
                        project={project}
                        template={t}
                        saved={() => {
                          setEditor(null);
                          refresh();
                        }}
                      />
                    )}
                    <Mutation
                      name="template-delete"
                      target={t.id}
                      label="Delete template"
                      onSuccess={refresh}
                    />
                  </>
                )}
              </li>
            ))}
          </ul>
        </>
      )}
    </section>
  );
}
