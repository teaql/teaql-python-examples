import { useState } from "react";
import { Mutation, type Task } from "./work";
type Place = { id: number; name: string; access: string };
export type Homes = {
  projects: Place[];
  candidates: Place[];
  selected: number | null;
};
export function Placements({
  task,
  refresh,
}: {
  task: Task;
  refresh: () => void;
}) {
  const [adding, setAdding] = useState(false);
  return (
    <section>
      <h2>Projects</h2>
      <ul>
        {task.projects.map((p) => (
          <li key={p.id}>
            <a href={"/crud/work_project/" + p.id}>{p.name}</a>
            {p.access === "full" && (
              <Mutation
                name="project-unlink"
                target={task.id}
                values={{ project: p.id }}
                label={"Remove from " + p.name}
              />
            )}
          </li>
        ))}
      </ul>
      {task.candidates.length > 0 && (
        <button onClick={() => setAdding(!adding)}>
          {adding ? "Cancel" : "Add to another project"}
        </button>
      )}
      {adding && (
        <Mutation
          name="project-link"
          target={task.id}
          label="Add to project"
          onSuccess={() => {
            setAdding(false);
            refresh();
          }}
        >
          <label>
            Project{" "}
            <select name="project">
              {task.candidates.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name}
                </option>
              ))}
            </select>
          </label>
        </Mutation>
      )}
    </section>
  );
}
