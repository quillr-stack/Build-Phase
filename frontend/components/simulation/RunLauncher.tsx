"use client";

import React, { useState, useEffect } from 'react';
import { Panel, BracketLabel } from '../ui/SattvaComponents';
import { simulate, fetchPersonas } from '../../lib/api';
import { useRouter } from 'next/navigation';

export default function RunLauncher() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    segment: 'tier2_urban',
    industry: 'fintech',
    objective: 'signup',
    product_description: '',
    agent_count: 100
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await simulate(formData);
      router.push(`/run/${res.run_id}`);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  return (
    <Panel title="Simulation Launcher">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1">
            <BracketLabel className="text-[10px]">Segment</BracketLabel>
            <select
              value={formData.segment}
              onChange={(e) => setFormData({...formData, segment: e.target.value})}
              className="w-full bg-sattva-white border-[0.5px] border-sattva-navy-mid p-2 font-mono text-sm focus:outline-none"
            >
              <option value="tier1_metro">TIER 1 METRO</option>
              <option value="tier2_urban">TIER 2 URBAN</option>
              <option value="tier3_rural">TIER 3 RURAL</option>
              <option value="mixed_india">MIXED INDIA</option>
            </select>
          </div>

          <div className="space-y-1">
            <BracketLabel className="text-[10px]">Industry</BracketLabel>
            <select
              value={formData.industry}
              onChange={(e) => setFormData({...formData, industry: e.target.value})}
              className="w-full bg-sattva-white border-[0.5px] border-sattva-navy-mid p-2 font-mono text-sm focus:outline-none"
            >
              <option value="fintech">FINTECH</option>
              <option value="fmcg">FMCG</option>
              <option value="edtech">EDTECH</option>
              <option value="ecommerce">ECOMMERCE</option>
              <option value="government">GOVERNMENT</option>
            </select>
          </div>
        </div>

        <div className="space-y-1">
          <BracketLabel className="text-[10px]">Objective</BracketLabel>
          <input
            type="text"
            value={formData.objective}
            onChange={(e) => setFormData({...formData, objective: e.target.value})}
            className="w-full bg-sattva-white border-[0.5px] border-sattva-navy-mid p-2 font-mono text-sm focus:outline-none"
            placeholder="e.g. increase signups"
          />
        </div>

        <div className="space-y-1">
          <BracketLabel className="text-[10px]">Product / Campaign Description</BracketLabel>
          <textarea
            rows={4}
            value={formData.product_description}
            onChange={(e) => setFormData({...formData, product_description: e.target.value})}
            className="w-full bg-sattva-white border-[0.5px] border-sattva-navy-mid p-2 font-mono text-sm focus:outline-none resize-none"
            placeholder="Describe the product or campaign strategy..."
          />
        </div>

        <div className="flex items-center justify-between pt-4">
           <div className="flex items-center gap-2">
             <BracketLabel className="text-[10px]">Agents</BracketLabel>
             <input
                type="number"
                value={formData.agent_count}
                onChange={(e) => setFormData({...formData, agent_count: parseInt(e.target.value)})}
                className="w-20 bg-sattva-white border-[0.5px] border-sattva-navy-mid p-1 font-mono text-sm focus:outline-none"
             />
           </div>

           <button
            type="submit"
            disabled={loading}
            className="bg-sattva-navy text-sattva-white px-6 py-2 font-display font-bold text-sm tracking-wider hover:bg-sattva-navy-mid transition-colors disabled:opacity-50"
           >
            {loading ? '[ INITIALIZING... ]' : '[ LAUNCH SIMULATION ]'}
           </button>
        </div>
      </form>
    </Panel>
  );
}
