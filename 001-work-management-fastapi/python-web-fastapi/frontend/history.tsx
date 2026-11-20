import type { Task } from "./work";
export type Event = {
  id: number;
  actor: string;
  label: string;
  old: string | null;
  new: string | null;
  at: string;
};
export function History({ task }: { task: Task }) {
  return (
    <section aria-label="Activity history" className="history">
      <h2>Activity history</h2>
      <ol>
        {task.history.map((e) => (
          <li key={e.id}>
            <time>{e.at}</time> · {e.actor} · {e.label}
            {e.old != null && <> · {e.old}</>}
            {e.new != null && <> → {e.new}</>}
          </li>
        ))}
      </ol>
    </section>
  );
}
