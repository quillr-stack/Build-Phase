"use client";

import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export default function BehaviorChart({ data }: { data: any }) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || !data) return;

    const width = 500;
    const height = 200;
    const margin = { top: 20, right: 30, bottom: 40, left: 40 };

    const svg = d3.select(svgRef.current)
      .attr('viewBox', [0, 0, width, height]);

    svg.selectAll('*').remove();

    // Mock data based on scenarios
    const chartData = [
      { name: 'Pessimistic', value: data.worst_case?.probability || 0 },
      { name: 'Realistic', value: data.most_likely?.probability || 0 },
      { name: 'Optimistic', value: data.best_case?.probability || 0 }
    ];

    const x = d3.scaleBand()
      .domain(chartData.map(d => d.name))
      .range([margin.left, width - margin.right])
      .padding(0.3);

    const y = d3.scaleLinear()
      .domain([0, 1])
      .range([height - margin.bottom, margin.top]);

    svg.append('g')
      .attr('transform', `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x))
      .selectAll('text')
      .attr('font-family', 'JetBrains Mono')
      .attr('font-size', '10px');

    svg.append('g')
      .attr('transform', `translate(${margin.left},0)`)
      .call(d3.axisLeft(y).ticks(5, "%"))
      .selectAll('text')
      .attr('font-family', 'JetBrains Mono')
      .attr('font-size', '10px');

    svg.selectAll('.bar')
      .data(chartData)
      .join('rect')
      .attr('class', 'bar')
      .attr('x', d => x(d.name)!)
      .attr('y', d => y(d.value))
      .attr('width', x.bandwidth())
      .attr('height', d => y(0) - y(d.value))
      .attr('fill', d => {
        if (d.name === 'Optimistic') return '#2D7A4F';
        if (d.name === 'Pessimistic') return '#C8961A';
        return '#1B3A6B';
      });

  }, [data]);

  return (
    <div className="w-full h-full min-h-[200px]">
      <svg ref={svgRef} className="w-full h-full" />
    </div>
  );
}
