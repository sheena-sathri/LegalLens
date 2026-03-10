import React, { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { LayoutGrid, List, Plus, Search, Filter, User, FileText, MessageSquare, AlertTriangle } from 'lucide-react';
import { PriorityDot, PriorityBadge, StatusBadge } from '../components/Badge';
import { matters } from '../data/mockData';

const statusColumns = [
  { key: 'New', label: 'New', color: 'bg-indigo-500' },
  { key: 'In Review', label: 'In Review', color: 'bg-blue-500' },
  { key: 'Pending Approval', label: 'Pending Approval', color: 'bg-amber-500' },
  { key: 'Approved', label: 'Approved', color: 'bg-emerald-500' },
  { key: 'Closed', label: 'Closed', color: 'bg-gray-400' },
];

function MatterCard({ matter }) {
  const totalRisks = matter.riskFlags.high + matter.riskFlags.medium + matter.riskFlags.low;
  return (
    <Link to={`/matters/${matter.id}`} className="block">
      <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow cursor-pointer">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs text-gray-500 font-mono">{matter.id}</span>
          <PriorityDot priority={matter.priority} />
        </div>
        <h4 className="text-sm font-semibold text-gray-900 mb-2 line-clamp-2">{matter.title}</h4>
        <div className="text-xs text-gray-500 mb-3">
          {matter.type} · {matter.assignee.team}
        </div>
        <div className="flex items-center text-xs text-gray-500 mb-3">
          <User className="w-3.5 h-3.5 mr-1" />
          <span>{matter.assignee.name}</span>
        </div>
        <div className="flex items-center justify-between text-xs text-gray-400">
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1">
              <FileText className="w-3.5 h-3.5" />
              {matter.documents}
            </span>
            <span className="flex items-center gap-1">
              <MessageSquare className="w-3.5 h-3.5" />
              {matter.comments}
            </span>
          </div>
          <span>{matter.dueDate}</span>
        </div>
        {totalRisks > 0 && (
          <div className="flex items-center gap-1 mt-2 text-xs">
            <AlertTriangle className="w-3.5 h-3.5 text-orange-500" />
            {matter.riskFlags.high > 0 && <span className="text-rose-600 font-medium">{matter.riskFlags.high}H</span>}
            {matter.riskFlags.medium > 0 && <span className="text-amber-600 font-medium">{matter.riskFlags.medium}M</span>}
            {matter.riskFlags.low > 0 && <span className="text-emerald-600 font-medium">{matter.riskFlags.low}L</span>}
          </div>
        )}
      </div>
    </Link>
  );
}

export default function MattersPage() {
  const [view, setView] = useState('kanban');
  const [search, setSearch] = useState('');
  const [filterStatus, setFilterStatus] = useState('All');

  const filtered = useMemo(() => {
    return matters.filter((m) => {
      const matchSearch =
        !search ||
        m.title.toLowerCase().includes(search.toLowerCase()) ||
        m.id.toLowerCase().includes(search.toLowerCase()) ||
        m.type.toLowerCase().includes(search.toLowerCase());
      const matchStatus = filterStatus === 'All' || m.status === filterStatus;
      return matchSearch && matchStatus;
    });
  }, [search, filterStatus]);

  const grouped = useMemo(() => {
    const map = {};
    statusColumns.forEach((col) => (map[col.key] = []));
    filtered.forEach((m) => {
      if (map[m.status]) map[m.status].push(m);
    });
    return map;
  }, [filtered]);

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Matters</h1>
          <p className="text-sm text-gray-500 mt-1">{matters.length} total matters</p>
        </div>
        <button className="inline-flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors">
          <Plus className="w-4 h-4" />
          New Matter
        </button>
      </div>

      <div className="flex items-center gap-3 mb-6">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search matters..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
        </div>
        <div className="relative">
          <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="pl-10 pr-8 py-2 border border-gray-200 rounded-lg text-sm appearance-none bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="All">All Statuses</option>
            {statusColumns.map((col) => (
              <option key={col.key} value={col.key}>{col.label}</option>
            ))}
          </select>
        </div>
        <div className="flex items-center border border-gray-200 rounded-lg overflow-hidden ml-auto">
          <button
            onClick={() => setView('kanban')}
            className={`p-2 ${view === 'kanban' ? 'bg-indigo-50 text-indigo-600' : 'text-gray-400 hover:text-gray-600'}`}
          >
            <LayoutGrid className="w-4 h-4" />
          </button>
          <button
            onClick={() => setView('list')}
            className={`p-2 ${view === 'list' ? 'bg-indigo-50 text-indigo-600' : 'text-gray-400 hover:text-gray-600'}`}
          >
            <List className="w-4 h-4" />
          </button>
        </div>
      </div>

      {view === 'kanban' ? (
        <div className="flex gap-4 overflow-x-auto pb-4">
          {statusColumns.map((col) => (
            <div key={col.key} className="flex-shrink-0 w-72">
              <div className="flex items-center gap-2 mb-3">
                <span className={`w-2.5 h-2.5 rounded-full ${col.color}`} />
                <h3 className="text-sm font-semibold text-gray-700">{col.label}</h3>
                <span className="text-xs text-gray-400 bg-gray-100 px-1.5 py-0.5 rounded-full">
                  {grouped[col.key].length}
                </span>
              </div>
              <div className="space-y-3">
                {grouped[col.key].map((matter) => (
                  <MatterCard key={matter.id} matter={matter} />
                ))}
                {grouped[col.key].length === 0 && (
                  <div className="text-center py-8 text-xs text-gray-400 border border-dashed border-gray-200 rounded-lg">
                    No matters
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-200">
                <th className="text-left px-4 py-3 font-medium text-gray-500">ID</th>
                <th className="text-left px-4 py-3 font-medium text-gray-500">Title</th>
                <th className="text-left px-4 py-3 font-medium text-gray-500">Type</th>
                <th className="text-left px-4 py-3 font-medium text-gray-500">Priority</th>
                <th className="text-left px-4 py-3 font-medium text-gray-500">Assignee</th>
                <th className="text-left px-4 py-3 font-medium text-gray-500">Status</th>
                <th className="text-left px-4 py-3 font-medium text-gray-500">Due Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filtered.map((matter) => (
                <tr key={matter.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-4 py-3">
                    <Link to={`/matters/${matter.id}`} className="text-indigo-600 hover:text-indigo-800 font-mono text-xs">
                      {matter.id}
                    </Link>
                  </td>
                  <td className="px-4 py-3">
                    <Link to={`/matters/${matter.id}`} className="text-gray-900 hover:text-indigo-600 font-medium">
                      {matter.title}
                    </Link>
                  </td>
                  <td className="px-4 py-3 text-gray-500">{matter.type}</td>
                  <td className="px-4 py-3"><PriorityBadge priority={matter.priority} /></td>
                  <td className="px-4 py-3 text-gray-500">{matter.assignee.name}</td>
                  <td className="px-4 py-3"><StatusBadge status={matter.status} /></td>
                  <td className="px-4 py-3 text-gray-500">{matter.dueDate}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
