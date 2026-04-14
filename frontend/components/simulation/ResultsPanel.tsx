"use client";

import React from 'react';
import { Panel, MetricCard, BracketLabel } from '../ui/SattvaComponents';

export default function ResultsPanel({ data }: { data: any }) {
  if (!data) return null;

  const { most_likely, best_case, worst_case, key_driver, metrics, summary } = data;

  return (
    <div className="space-y-6">
      <Panel title="Executive Summary">
        <p className="text-lg font-display font-medium text-sattva-navy-mid leading-relaxed">
          {summary}
        </p>
      </Panel>

      <div className="grid grid-cols-3 gap-6">
        <Panel title="Best Case">
          <MetricCard
            label="Adoption Prob"
            value={`${(best_case.probability * 100).toFixed(1)}%`}
            color="green"
          />
          <div className="mt-4 space-y-1">
            <BracketLabel className="text-[10px]">Sentiment</BracketLabel>
            <div className="uppercase font-mono text-sm text-sattva-green">{best_case.sentiment}</div>
          </div>
        </Panel>

        <Panel title="Most Likely">
          <MetricCard
            label="Adoption Prob"
            value={`${(most_likely.probability * 100).toFixed(1)}%`}
            color="navy"
          />
          <div className="mt-4 space-y-1">
            <BracketLabel className="text-[10px]">Sentiment</BracketLabel>
            <div className="uppercase font-mono text-sm text-sattva-navy">{most_likely.sentiment}</div>
          </div>
        </Panel>

        <Panel title="Worst Case">
          <MetricCard
            label="Adoption Prob"
            value={`${(worst_case.probability * 100).toFixed(1)}%`}
            color="amber"
          />
          <div className="mt-4 space-y-1">
            <BracketLabel className="text-[10px]">Sentiment</BracketLabel>
            <div className="uppercase font-mono text-sm text-sattva-amber">{worst_case.sentiment}</div>
          </div>
        </Panel>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <Panel title="Key Intelligence Metrics">
          <div className="grid grid-cols-2 gap-y-6 gap-x-4">
            <MetricCard label="Trust Gap" value={metrics?.trust_gap_score?.toFixed(1) || '0.0'} subValue="/10" />
            <MetricCard label="Price Sensitivity" value={metrics?.price_sensitivity_index?.toFixed(1) || '0.0'} subValue="/10" />
            <MetricCard label="Viral Potential" value={metrics?.viral_potential?.toFixed(1) || '0.0'} subValue="/10" />
            <MetricCard label="Digital Readiness" value={metrics?.digital_readiness_score?.toFixed(1) || '0.0'} subValue="/10" />
          </div>
        </Panel>

        <Panel title="Critical Barriers">
          <div className="space-y-3">
            <div className="p-3 bg-sattva-navy text-sattva-white flex justify-between items-center">
              <span className="mono-label">Primary Constraint</span>
              <span className="font-mono text-sm uppercase">{key_driver}</span>
            </div>
            <div className="space-y-2">
              <BracketLabel className="text-[10px]">Other Identified Barriers</BracketLabel>
              {most_likely.barriers?.map((barrier: string, i: number) => (
                <div key={i} className="font-mono text-xs border-b border-sattva-grid border-opacity-30 pb-1 uppercase">
                  {i + 1}. {barrier}
                </div>
              ))}
            </div>
          </div>
        </Panel>
      </div>
    </div>
  );
}
