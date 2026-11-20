import { useState } from "react";
import { Mutation, type Task } from "./work";
type Sub = {
  id: number;
  title: string;
  assignee: number | null;
  person: string;
  due: string | null;
  done: boolean;
};
type Comment = {
  id: number;
  body: string;
  author: string;
  mine: boolean;
  edited: boolean;
  date: string;
};
export type DiscussionData = {
  people: { id: number; name: string }[];
  subtasks: Sub[];
  comments: Comment[];
};

function SubFields({ task, sub }: { task: Task; sub?: Sub }) {
  return (
    <>
      <label>
        Subtask title <input name="title" required defaultValue={sub?.title} />
      </label>
      <label>
        Subtask assignee{" "}
        <select name="assignee" defaultValue={sub?.assignee ?? ""}>
          <option value="">Unassigned</option>
          {task.people.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
      </label>
      <label>
        Subtask due date{" "}
        <input type="date" name="due" defaultValue={sub?.due ?? ""} />
      </label>
      <label>
        Subtask status{" "}
        <select name="done" defaultValue={sub?.done ? "true" : "false"}>
          <option value="false">Open</option>
          <option value="true">Completed</option>
        </select>
      </label>
    </>
  );
}
export function Discussion({
  task,
  refresh,
}: {
  task: Task;
  refresh: () => void;
}) {
  const [add, setAdd] = useState(false);
  const [rev, setRev] = useState(0);
  const full = task.access === "full";
  return (
    <>
      <section>
        <h2>Subtasks</h2>
        {full && <button onClick={() => setAdd(!add)}>Add subtask</button>}
        {add && (
          <Mutation
            name="subtask-add"
            target={task.id}
            label="Create subtask"
            onSuccess={() => {
              setAdd(false);
              refresh();
            }}
          >
            <SubFields task={task} />
          </Mutation>
        )}
        <ul>
          {task.subtasks.map((s) => (
            <li key={s.id}>
              <span>{s.title}</span> · {s.done ? "Completed" : "Open"}{" "}
              {s.person} {s.due}
              {full && (
                <details>
                  <summary>Edit subtask</summary>
                  <Mutation
                    name="subtask-edit"
                    target={s.id}
                    label="Save subtask"
                    onSuccess={refresh}
                  >
                    <SubFields task={task} sub={s} />
                  </Mutation>
                  <Mutation
                    name="subtask-delete"
                    target={s.id}
                    label="Delete subtask"
                    onSuccess={refresh}
                  />
                </details>
              )}
            </li>
          ))}
        </ul>
      </section>
      <section>
        <h2>Comments</h2>
        {task.comments.map((c) => (
          <article key={c.id}>
            <strong>{c.author}</strong> <time>{c.date}</time>{" "}
            {c.edited && "(edited)"}
            <p>{c.body}</p>
            {c.mine && (
              <details>
                <summary>Edit comment</summary>
                <Mutation
                  name="comment-edit"
                  target={c.id}
                  label="Save comment"
                  onSuccess={refresh}
                >
                  <label>
                    Comment text{" "}
                    <textarea name="comment" defaultValue={c.body} required />
                  </label>
                </Mutation>
                <Mutation
                  name="comment-delete"
                  target={c.id}
                  label="Delete comment"
                  onSuccess={refresh}
                />
              </details>
            )}
          </article>
        ))}
        <Mutation
          key={rev}
          name="comment-add"
          target={task.id}
          label="Post comment"
          onSuccess={() => {
            setRev(rev + 1);
            refresh();
          }}
        >
          <label>
            New comment <textarea name="comment" required maxLength={4000} />
          </label>
        </Mutation>
      </section>
    </>
  );
}
