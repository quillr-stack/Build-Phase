"use client";

import React, { useEffect, useState } from 'react';
import { BracketLabel } from '../../../components/ui/SattvaComponents';
import ResultsPanel from '../../../components/simulation/ResultsPanel';
import { getRun } from '../../../lib/api';
import Link from 'next/link';

export default function ResultsPage({ params }: { params: { id: string } }) {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    getRun(params.id).then(res => {
      if (res.output) {
        setData(res.output);
      }
    });
  }, [params.id]);

  return (
    <main className="min-h-screen p-8 max-w-7xl mx-auto space-y-8">
      <header className="flex justify-between items-end border-b-[0.5px] border-sattva-navy-mid pb-4">
        <div>
          <h1 className="text-4xl tracking-tighter">INTELLIGENCE REPORT</h1>
          <p className="mono-label text-sattva-muted">Simulation ID: {params.id}</p>
        </div>
        <Link href="/" className="bg-sattva-navy text-sattva-white px-6 py-2 font-display font-bold text-sm tracking-wider hover:bg-sattva-navy-mid transition-colors">
          [ NEW SIMULATION ]
        </Link>
      </header>

      {data ? (
        <ResultsPanel data={data} />
      ) : (
        <div className="flex justify-center items-center h-64 font-mono text-sattva-muted">
          [ LOADING REPORT ARTIFACTS... ]
        </div>
      )}
    </main>
  );
}
