import { useEffect, useState } from "react";
import { Mutation } from "./work";

export type Notice = {
  id: number;
  task: string;
  read: boolean;
  actor: string;
  label: string;
  old: string | null;
  new: string | null;
  at: string;
};
export function InboxLink() {
  const [unread, setUnread] = useState<number | null>(null);
  useEffect(() => {
    let active = true;
    async function count() {
      try {
        const r = await fetch("/api/inbox", { cache: "no-store" });
        if (r.ok) {
          const v = await r.json();
          if (active) setUnread(v.unread);
        }
      } catch {}
    }
    void count();
    const timer = setInterval(() => {
      if (!document.hidden) void count();
    }, 7000);
    return () => {
      active = false;
      clearInterval(timer);
    };
  }, []);
  return <a href="/inbox">Inbox{unread ? " (" + unread + ")" : ""}</a>;
}
export function Inbox({
  items,
  unread,
  refresh,
}: {
  items: Notice[];
  unread: number;
  refresh: () => void;
}) {
  return (
    <>
      <a href="/">Your records</a>
      <h1>Inbox</h1>
      <p>{unread} unread</p>
      <ol>
        {items.map((n) => (
          <li key={n.id}>
            <Mutation
              name="notice-read"
              target={n.id}
              label={n.task}
              values={{ state: true, open: true }}
            />
            <p>
              {n.actor} · {n.label}
              {n.old && " · " + n.old}
              {n.new && " → " + n.new} · <time>{n.at}</time>
            </p>
            <Mutation
              name="notice-read"
              target={n.id}
              label={n.read ? "Mark unread" : "Mark read"}
              values={{ state: !n.read }}
              onSuccess={refresh}
            />
          </li>
        ))}
      </ol>
    </>
  );
}
