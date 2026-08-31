"use client";

import { useEffect, useState } from "react";
import { auditApi, AuditEvent } from "../api/auditApi";

interface DecisionLogTableProps {
  bidderId: string;
}

export function DecisionLogTable({ bidderId }: DecisionLogTableProps) {
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchAuditLog() {
      try {
        const fetchedEvents = await auditApi.getBidderAuditTrail(bidderId);
        // Sort chronologically (oldest to newest for a log, or newest first? Let's do newest first)
        setEvents(fetchedEvents.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()));
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    }
    fetchAuditLog();
  }, [bidderId]);

  if (isLoading) return <div className="p-4 text-[var(--color-text-secondary)]">Loading audit log...</div>;
  if (error) return <div className="p-4 text-[var(--color-error)]">Error loading audit log: {error}</div>;

  return (
    <div className="bg-white border border-[var(--color-border)] rounded-md shadow-sm overflow-hidden mb-12 max-w-5xl mx-auto">
      <div className="bg-[var(--color-primary)] px-6 py-4">
        <h2 className="text-lg font-bold text-white">Chronological Decision Audit Log</h2>
      </div>
      
      {events.length === 0 ? (
        <div className="p-8 text-center text-[var(--color-text-secondary)] italic">
          No audit events recorded for this bidder.
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-[var(--color-surface)] border-b border-[var(--color-border)] text-xs uppercase tracking-wider text-[var(--color-text-secondary)] font-bold">
              <tr>
                <th className="px-4 py-3">Recorded At</th>
                <th className="px-4 py-3">Recorded By</th>
                <th className="px-4 py-3">Flag ID / Context</th>
                <th className="px-4 py-3">Previous State</th>
                <th className="px-4 py-3">New State</th>
                <th className="px-4 py-3 w-1/3">Notes</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--color-border)]">
              {events.map((event) => (
                <tr key={event.id} className="hover:bg-[var(--color-surface-hover)] transition-colors text-[var(--color-text-primary)]">
                  <td className="px-4 py-3 whitespace-nowrap">
                    {new Date(event.created_at).toLocaleString()}
                  </td>
                  <td className="px-4 py-3 font-mono text-xs">
                    {event.officer_user_id}
                  </td>
                  <td className="px-4 py-3 font-mono text-xs text-[var(--color-text-secondary)]">
                    {event.flag_id ? event.flag_id.slice(0, 8) : "N/A"}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    {event.previous_state ? (
                      <span className="inline-block px-2 py-1 rounded-sm border border-[var(--color-border)] bg-gray-50 text-gray-600 font-medium">
                        {event.previous_state}
                      </span>
                    ) : (
                      <span className="text-[var(--color-text-secondary)] italic">None</span>
                    )}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className="inline-block px-2 py-1 rounded-sm border border-[var(--color-border)] bg-white font-bold">
                      {event.new_state}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm leading-relaxed">
                    {event.notes || <span className="text-[var(--color-text-secondary)] italic">No notes provided</span>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
