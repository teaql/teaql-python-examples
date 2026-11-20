import { useState } from "react";
import { Mutation, type Project } from "./work";
export type Dropdown = {
  id: number;
  name: string;
  options: { id: number; name: string }[];
};
export function Fields({
  project,
  refresh,
}: {
  project: Project;
  refresh: () => void;
}) {
  const [open, setOpen] = useState(false);
  return (
    <section>
      <button aria-expanded={open} onClick={() => setOpen(!open)}>
        Custom fields
      </button>
      {open && (
        <>
          <h2>Custom fields</h2>
          {project.access === "full" && (
            <Mutation
              name="field-add"
              target={project.id}
              label="Create field"
              onSuccess={refresh}
            >
              <label>
                Field name <input required name="name" maxLength={200} />
              </label>
              <label>
                Option names (comma separated) <input name="options" />
              </label>
            </Mutation>
          )}
          {project.fields.map((f) => (
            <section key={f.id}>
              <h3>{f.name}</h3>
              {f.options.map((o, i) => (
                <details key={o.id}>
                  <summary>{o.name}</summary>
                  {project.access === "full" && (
                    <>
                      <Mutation
                        name="option-edit"
                        target={o.id}
                        label="Save option"
                        onSuccess={refresh}
                      >
                        <label>
                          Option name{" "}
                          <input defaultValue={o.name} name="name" required />
                        </label>
                        <label>
                          Option position{" "}
                          <input
                            name="position"
                            type="number"
                            min="0"
                            defaultValue={i}
                          />
                        </label>
                      </Mutation>
                      <Mutation
                        name="option-delete"
                        target={o.id}
                        label="Delete option"
                        onSuccess={refresh}
                      />
                    </>
                  )}
                </details>
              ))}
              {project.access === "full" && (
                <Mutation
                  name="option-add"
                  target={f.id}
                  label="Add option"
                  onSuccess={refresh}
                >
                  <label>
                    New option name <input required name="name" />
                  </label>
                </Mutation>
              )}
            </section>
          ))}
        </>
      )}
    </section>
  );
}
