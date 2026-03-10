const colorMap = {
  indigo: 'bg-indigo-50 text-indigo-700 ring-indigo-600/10',
  emerald: 'bg-emerald-50 text-emerald-700 ring-emerald-600/10',
  amber: 'bg-amber-50 text-amber-700 ring-amber-600/10',
  rose: 'bg-rose-50 text-rose-700 ring-rose-600/10',
  orange: 'bg-orange-50 text-orange-700 ring-orange-600/10',
  blue: 'bg-blue-50 text-blue-700 ring-blue-600/10',
  gray: 'bg-gray-100 text-gray-600 ring-gray-500/10',
  purple: 'bg-purple-50 text-purple-700 ring-purple-600/10',
  violet: 'bg-violet-50 text-violet-700 ring-violet-600/10',
};

const priorityColor = {
  Low: 'emerald',
  Medium: 'amber',
  High: 'orange',
  Urgent: 'rose',
};

const statusColor = {
  New: 'indigo',
  'In Review': 'blue',
  'Pending Approval': 'amber',
  Approved: 'emerald',
  Closed: 'gray',
  Resolved: 'emerald',
  'In Progress': 'blue',
};

export function Badge({ children, color = 'gray', className = '' }) {
  const c = colorMap[color] || colorMap.gray;
  return (
    <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ring-1 ring-inset ${c} ${className}`}>
      {children}
    </span>
  );
}

export function PriorityBadge({ priority }) {
  return <Badge color={priorityColor[priority] || 'gray'}>{priority}</Badge>;
}

export function StatusBadge({ status }) {
  return <Badge color={statusColor[status] || 'gray'}>{status}</Badge>;
}

export function PriorityDot({ priority }) {
  const colors = { Low: 'bg-emerald-400', Medium: 'bg-amber-400', High: 'bg-orange-400', Urgent: 'bg-rose-500' };
  return <span className={`inline-block w-2.5 h-2.5 rounded-full ${colors[priority] || 'bg-gray-400'}`} />;
}
