"use client";

import React, { useEffect, useState } from 'react';
import { Panel, MetricCard, BracketLabel } from '../../components/ui/SattvaComponents';
import { fetchPersonas } from '../../lib/api';
import Link from 'next/link';

export default function PersonasPage() {
  const [personas, setPersonas] = useState<any[]>([]);

  useEffect(() => {
    fetchPersonas().then(setPersonas);
  }, []);

  return (
    <main className="min-h-screen p-8 max-w-7xl mx-auto space-y-8">
      <header className="flex justify-between items-end border-b-[0.5px] border-sattva-navy-mid pb-4">
        <div>
          <h1 className="text-4xl tracking-tighter">PERSONA EXPLORER</h1>
          <p className="mono-label text-sattva-muted">Indian Behavioral Archetypes (Seed Data)</p>
        </div>
        <Link href="/" className="mono-label hover:text-sattva-navy-light underline decoration-sattva-amber underline-offset-4">DASHBOARD</Link>
      </header>

      <div className="grid grid-cols-2 gap-8">
        {personas.map((persona, i) => (
          <Panel key={i} title={persona.persona_id}>
             <div className="grid grid-cols-3 gap-4">
                <div className="col-span-1 space-y-4">
                   <div className="space-y-1">
                      <BracketLabel className="text-[10px]">Segment</BracketLabel>
                      <div className="uppercase font-mono text-sm">{persona.segment}</div>
                   </div>
                   <div className="space-y-1">
                      <BracketLabel className="text-[10px]">Platform</BracketLabel>
                      <div className="uppercase font-mono text-sm">{persona.traits.platform_preference}</div>
                   </div>
                   <div className="space-y-1">
                      <BracketLabel className="text-[10px]">Data Sources</BracketLabel>
                      <div className="flex flex-wrap gap-1">
                        {persona.data_sources?.map((s: string) => (
                          <span key={s} className="bg-sattva-navy-mid text-sattva-white text-[8px] px-1 font-mono uppercase">{s}</span>
                        ))}
                      </div>
                   </div>
                </div>

                <div className="col-span-2 grid grid-cols-2 gap-4">
                   <MetricCard label="Trust" value={persona.traits.trust_level.toFixed(2)} />
                   <MetricCard label="Price Sens" value={persona.traits.price_sensitivity.toFixed(2)} />
                   <MetricCard label="Digital Lit" value={persona.traits.digital_literacy.toFixed(2)} />
                   <MetricCard label="Social Infl" value={persona.traits.social_influence.toFixed(2)} />
                </div>
             </div>
          </Panel>
        ))}
      </div>
    </main>
  );
}
