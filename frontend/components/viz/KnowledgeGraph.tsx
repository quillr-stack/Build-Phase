"use client";

import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export default function KnowledgeGraph() {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    const width = 400;
    const height = 300;

    const svg = d3.select(svgRef.current)
      .attr('viewBox', [0, 0, width, height]);

    svg.selectAll('*').remove();

    // Mock data
    const nodes = [
      { id: 'Agent', group: 1 },
      { id: 'Trust', group: 2 },
      { id: 'Price', group: 2 },
      { id: 'WhatsApp', group: 3 },
      { id: 'UPI', group: 2 }
    ];

    const links = [
      { source: 'Agent', target: 'Trust' },
      { source: 'Agent', target: 'Price' },
      { source: 'Agent', target: 'WhatsApp' },
      { source: 'Agent', target: 'UPI' }
    ];

    const simulation = d3.forceSimulation(nodes as any)
      .force('link', d3.forceLink(links).id((d: any) => d.id))
      .force('charge', d3.forceManyBody().strength(-100))
      .force('center', d3.forceCenter(width / 2, height / 2));

    const link = svg.append('g')
      .attr('stroke', '#C8BFB0')
      .attr('stroke-opacity', 0.6)
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke-width', 0.5);

    const node = svg.append('g')
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', 5)
      .attr('fill', (d: any) => d.group === 1 ? '#0D2240' : '#4A7AB5');

    const labels = svg.append('g')
      .selectAll('text')
      .data(nodes)
      .join('text')
      .text((d: any) => d.id)
      .attr('font-family', 'JetBrains Mono')
      .attr('font-size', '8px')
      .attr('dx', 8)
      .attr('dy', 3);

    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node
        .attr('cx', (d: any) => d.x)
        .attr('cy', (d: any) => d.y);

      labels
        .attr('x', (d: any) => d.x)
        .attr('y', (d: any) => d.y);
    });

  }, []);

  return (
    <div className="w-full h-full min-h-[300px]">
      <svg ref={svgRef} className="w-full h-full" />
    </div>
  );
}
