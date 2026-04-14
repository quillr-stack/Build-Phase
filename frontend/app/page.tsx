import React from 'react';
import RunLauncher from '../components/simulation/RunLauncher';
import { Panel, MetricCard, BracketLabel } from '../components/ui/SattvaComponents';
import Link from 'next/link';

export default function Dashboard() {
  return (
    <main className="min-h-screen p-8 max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <header className="flex justify-between items-end border-b-[0.5px] border-sattva-navy-mid pb-4">
        <div>
          <h1 className="text-4xl tracking-tighter">SATTVA</h1>
          <p className="mono-label text-sattva-muted">Behavioral Intelligence Engine // India</p>
        </div>
        <nav className="flex gap-6">
          <Link href="/" className="mono-label hover:text-sattva-navy-light underline decoration-sattva-amber underline-offset-4">DASHBOARD</Link>
          <Link href="/personas" className="mono-label hover:text-sattva-navy-light">PERSONAS</Link>
          <Link href="/analytics" className="mono-label hover:text-sattva-navy-light">SYSTEM ANALYTICS</Link>
        </nav>
      </header>

      <div className="grid grid-cols-12 gap-8">
        {/* Left Column - System Status */}
        <div className="col-span-4 space-y-8">
          <Panel title="System Status">
            <div className="space-y-4">
              <MetricCard label="Global Accuracy" value="71.2%" subValue="+6.4%" color="green" />
              <div className="grid grid-cols-2 gap-4 pt-2">
                <div>
                  <BracketLabel className="text-[10px]">Validated Runs</BracketLabel>
                  <div className="font-mono text-xl">23</div>
                </div>
                <div>
                  <BracketLabel className="text-[10px]">Active Agents</BracketLabel>
                  <div className="font-mono text-xl">10K</div>
                </div>
              </div>
            </div>
          </Panel>

          <Panel title="Intelligence Feed">
             <div className="space-y-3">
               {[
                 { time: '14:20', msg: 'Fintech Simulation #821 Complete' },
                 { time: '14:15', msg: 'New Validation Data: FMCG North' },
                 { time: '13:50', msg: 'Persona traits updated: T2_M_UP' }
               ].map((item, i) => (
                 <div key={i} className="flex gap-3 text-[10px] font-mono border-b border-sattva-grid border-opacity-30 pb-2">
                   <span className="text-sattva-muted">{item.time}</span>
                   <span className="uppercase">{item.msg}</span>
                 </div>
               ))}
             </div>
          </Panel>
        </div>

        {/* Right Column - Run Launcher */}
        <div className="col-span-8">
          <RunLauncher />
        </div>
      </div>

      {/* Footer / Context */}
      <footer className="pt-8 flex justify-between items-center opacity-50">
        <BracketLabel className="text-[10px]">SATTVA V0.1.0-ALPHA</BracketLabel>
        <BracketLabel className="text-[10px]">ENCRYPTED TERMINAL ACCESS ONLY</BracketLabel>
      </footer>
    </main>
  );
}
