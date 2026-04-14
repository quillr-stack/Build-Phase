"use client";

import React, { useEffect, useState, useRef } from 'react';
import { Panel, StatusBadge } from '../ui/SattvaComponents';

interface LogEntry {
  timestamp: string;
  layer: string;
  event: string;
  data: any;
}

export default function LiveFeed({ runId }: { runId: string }) {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // In a real implementation, this would be an SSE connection
    // For Phase 3 demo, we might poll or simulate
    const fetchLogs = async () => {
      // Mocking some live feed behavior
      const mockEvents = [
        { timestamp: new Date().toISOString(), layer: 'input_layer', event: 'VALIDATING PARAMS', data: {} },
        { timestamp: new Date().toISOString(), layer: 'persona_engine', event: 'LOADING 1000 AGENTS', data: { count: 1000 } },
        { timestamp: new Date().toISOString(), layer: 'scenario_engine', event: 'GENERATING SCENARIOS', data: { count: 3 } },
      ];
      setLogs(prev => [...prev, ...mockEvents].slice(-50));
    };

    const interval = setInterval(fetchLogs, 3000);
    return () => clearInterval(interval);
  }, [runId]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <Panel title="Live Intelligence Feed" className="h-full flex flex-col">
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto space-y-2 font-mono text-[10px] pr-2 custom-scrollbar"
      >
        {logs.map((log, i) => (
          <div key={i} className="flex gap-3 border-b border-sattva-grid border-opacity-30 pb-1">
            <span className="text-sattva-muted shrink-0">
              {new Date(log.timestamp).toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}
            </span>
            <span className="text-sattva-navy-light shrink-0 uppercase w-24">
              [{log.layer}]
            </span>
            <span className="text-sattva-navy uppercase">
              {log.event}
            </span>
          </div>
        ))}
      </div>
    </Panel>
  );
}
