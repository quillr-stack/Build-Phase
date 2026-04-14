"use client";

import React, { useEffect, useState } from 'react';
import { Panel, StatusBadge, BracketLabel } from '../../../components/ui/SattvaComponents';
import LiveFeed from '../../../components/simulation/LiveFeed';
import { getRun } from '../../../lib/api';
import { useRouter } from 'next/navigation';
import dynamic from 'next/dynamic';

// Dynamically import Three.js viz to avoid SSR issues
const AgentGraph3D = dynamic(() => import('../../../components/viz/AgentGraph3D'), { ssr: false });

export default function RunPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [run, setRun] = useState<any>(null);

  useEffect(() => {
    const poll = async () => {
      try {
        const data = await getRun(params.id);
        setRun(data);
        if (data.status === 'complete') {
          router.push(`/results/${params.id}`);
        }
      } catch (err) {
        console.error(err);
      }
    };

    poll();
    const interval = setInterval(poll, 5000);
    return () => clearInterval(interval);
  }, [params.id, router]);

  return (
    <main className="h-screen flex flex-col p-6 space-y-6">
      <header className="flex justify-between items-center shrink-0">
        <div>
          <BracketLabel className="text-xs">Simulation Run</BracketLabel>
          <h2 className="text-2xl font-mono truncate max-w-md">{params.id}</h2>
        </div>
        <div className="flex items-center gap-4">
          <StatusBadge status={run?.status || 'pending'} />
          <button
            onClick={() => router.push('/')}
            className="text-xs font-mono border-[0.5px] border-sattva-navy-mid px-3 py-1 hover:bg-sattva-navy hover:text-sattva-white transition-colors"
          >
            [ ABORT ]
          </button>
        </div>
      </header>

      <div className="flex-1 grid grid-cols-12 gap-6 min-h-0">
        <div className="col-span-8 flex flex-col space-y-6">
          <Panel title="Agent Propagation Network" className="flex-1 bg-sattva-navy relative overflow-hidden p-0">
            <div className="absolute inset-0 z-0">
              <AgentGraph3D />
            </div>
            <div className="absolute top-4 left-4 z-10 pointer-events-none">
              <div className="bg-sattva-navy bg-opacity-60 backdrop-blur-sm p-3 border-[0.5px] border-sattva-navy-light">
                 <BracketLabel className="text-[10px] text-sattva-white">Network Stats</BracketLabel>
                 <div className="text-sattva-white font-mono text-lg">1,000 Nodes</div>
                 <div className="text-sattva-navy-light font-mono text-xs uppercase">WhatsApp Graph Layer Active</div>
              </div>
            </div>
          </Panel>
        </div>

        <div className="col-span-4 flex flex-col min-h-0">
           <LiveFeed runId={params.id} />
        </div>
      </div>
    </main>
  );
}
