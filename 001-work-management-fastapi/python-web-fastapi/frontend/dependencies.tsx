import { useState } from "react";
import { Mutation, type Task, type Project } from "./work";
export type LinkTask = { id: number; title: string; edge?: number };
export type DependencyData = {
  blockers: LinkTask[];
  blocking: LinkTask[];
  dependencyCandidates: LinkTask[];
};
export function Dependencies({
  task,
  refresh,
}: {
  task: Task;
  refresh: () => void;
}) {
  const [open, setOpen] = useState(false);
  return (
    <section>
      <h2>Dependencies</h2>
      {task.blockers.length > 0 && (
        <>
          <h3>Blocked by</h3>
          <ul>
            {task.blockers.map((b) => (
              <li key={b.id}>
                <a href={"/crud/work_task/" + b.id}>{b.title}</a>
                {task.access === "full" && (
                  <Mutation
                    name="dependency-remove"
                    target={b.edge!}
                    label="Remove dependency"
                    onSuccess={refresh}
                  />
                )}
              </li>
            ))}
          </ul>
        </>
      )}
      {task.blocking.length > 0 && (
        <>
          <h3>Blocking</h3>
          <ul>
            {task.blocking.map((b) => (
              <li key={b.id}>
                <a href={"/crud/work_task/" + b.id}>{b.title}</a>
              </li>
            ))}
          </ul>
        </>
      )}
      {task.access === "full" && (
        <button onClick={() => setOpen(!open)}>
          {open ? "Cancel" : "Add dependency"}
        </button>
      )}
      {open && task.dependencyCandidates.length > 0 && (
        <Mutation
          name="dependency-add"
          target={task.id}
          label="Add blocker"
          onSuccess={() => {
            setOpen(false);
            refresh();
          }}
        >
          <label>
            Blocking task{" "}
            <select name="blocker">
              {task.dependencyCandidates.map((b) => (
                <option value={b.id} key={b.id}>
                  {b.title}
                </option>
              ))}
            </select>
          </label>
        </Mutation>
      )}
    </section>
  );
}
export function ShiftDates({
  project,
  refresh,
}: {
  project: Project;
  refresh: () => void;
}) {
  return (
    <details>
      <summary>Project settings</summary>
      {project.access !== "full" && (
        <p>Shift dependent dates · {project.shiftDates ? "On" : "Off"}</p>
      )}
      {project.access === "full" && (
        <Mutation
          name="shift-setting"
          target={project.id}
          label="Save date settings"
          onSuccess={refresh}
        >
          <label>
            Shift dependent dates{" "}
            <select name="enabled" defaultValue={String(project.shiftDates)}>
              <option value="false">Off</option>
              <option value="true">On</option>
            </select>
          </label>
        </Mutation>
      )}
    </details>
  );
}
