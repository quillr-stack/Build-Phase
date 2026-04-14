import React from 'react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const BracketLabel = ({ children, className, uppercase = true }: { children: React.ReactNode, className?: string, uppercase?: boolean }) => (
  <span className={cn(
    "mono-label bracket-label text-sattva-navy-mid font-mono",
    uppercase && "uppercase",
    className
  )}>
    {children}
  </span>
);

export const Panel = ({
  children,
  title,
  className,
  titleClassName
}: {
  children: React.ReactNode,
  title?: string,
  className?: string,
  titleClassName?: string
}) => (
  <div className={cn(
    "panel-crosshair border-[0.5px] border-sattva-navy-mid bg-sattva-cream p-4 relative",
    className
  )}>
    <div className="crosshair-bottom-left" />
    <div className="crosshair-bottom-right" />

    {title && (
      <div className={cn("mb-4 flex items-center", titleClassName)}>
        <BracketLabel>{title}</BracketLabel>
      </div>
    )}

    {children}
  </div>
);

export const MetricCard = ({
  label,
  value,
  subValue,
  color = 'navy'
}: {
  label: string,
  value: string | number,
  subValue?: string,
  color?: 'navy' | 'green' | 'amber'
}) => {
  const colorMap = {
    navy: 'text-sattva-navy',
    green: 'text-sattva-green',
    amber: 'text-sattva-amber',
  };

  return (
    <div className="flex flex-col border-l-[0.5px] border-sattva-navy-mid pl-3 py-1">
      <span className="mono-label text-sattva-muted uppercase mb-1">{label}</span>
      <div className="flex items-baseline gap-2">
        <span className={cn("text-2xl font-mono font-bold", colorMap[color])}>{value}</span>
        {subValue && <span className="mono-label text-sattva-muted">{subValue}</span>}
      </div>
    </div>
  );
};

export const StatusBadge = ({ status }: { status: string }) => {
  const statusStyles: Record<string, string> = {
    pending: 'text-sattva-amber border-sattva-amber',
    running: 'text-sattva-navy-light border-sattva-navy-light animate-pulse',
    processing: 'text-sattva-navy-light border-sattva-navy-light animate-pulse',
    complete: 'text-sattva-green border-sattva-green',
    failed: 'text-red-600 border-red-600',
  };

  return (
    <span className={cn(
      "mono-label px-2 py-0.5 border-[0.5px] uppercase",
      statusStyles[status.toLowerCase()] || 'text-sattva-muted border-sattva-muted'
    )}>
      {status}
    </span>
  );
};
