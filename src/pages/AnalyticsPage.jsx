import React, { useState } from 'react';
import { TrendingUp, TrendingDown, BarChart3, AlertTriangle, ChevronDown } from 'lucide-react';
import {
  LineChart, PieChart, BarChart, ResponsiveContainer,
  Line, Bar, Pie, Cell, XAxis, YAxis, Tooltip, Legend, CartesianGrid
} from 'recharts';
import { monthlyData, mattersByType, workloadData, statusData, responseTimeData, riskDistribution } from '../data/mockData';

const metrics = [
  { label: 'Open Matters', value: '47', trend: '+12%', up: true, good: true },
  { label: 'Requests This Month', value: '128', trend: '+23%', up: true, good: true },
  { label: 'Avg Cycle Time', value: '3.2 days', trend: '-15%', up: false, good: true },
  { label: 'Resolution Rate', value: '94%', trend: '+5%', up: true, good: true },
];

function MetricCard({ label, value, trend, up, good }) {
  const isPositive = good;
  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6 flex-1">
      <p className="text-sm text-gray-500 mb-1">{label}</p>
      <p className="text-3xl font-bold text-gray-900">{value}</p>
      <div className={`flex items-center gap-1 mt-2 text-sm font-medium ${isPositive ? 'text-emerald-600' : 'text-rose-600'}`}>
        {up ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
        {trend}
      </div>
    </div>
  );
}

function ChartCard({ title, children }) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6 flex-1">
      <h3 className="text-sm font-semibold text-gray-900 mb-4">{title}</h3>
      {children}
    </div>
  );
}

export default function AnalyticsPage() {
  const [period, setPeriod] = useState('Last 30 days');

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Analytics & Reporting</h1>
          <p className="text-sm text-gray-500 mt-1">Executive dashboard overview</p>
        </div>
        <div className="relative">
          <select
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            className="appearance-none bg-white border border-gray-200 rounded-lg px-4 py-2 pr-10 text-sm font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option>Last 7 days</option>
            <option>Last 30 days</option>
            <option>Last 90 days</option>
            <option>Last 12 months</option>
          </select>
          <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
        </div>
      </div>

      <div className="flex gap-4 mb-6">
        {metrics.map((m) => (
          <MetricCard key={m.label} {...m} />
        ))}
      </div>

      <div className="flex gap-4 mb-6">
        <ChartCard title="Request Volume">
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="month" tick={{ fontSize: 12, fill: '#6b7280' }} />
              <YAxis tick={{ fontSize: 12, fill: '#6b7280' }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="requests" stroke="#6366F1" strokeWidth={2} dot={{ r: 4 }} name="Requests" />
              <Line type="monotone" dataKey="resolved" stroke="#10B981" strokeWidth={2} dot={{ r: 4 }} name="Resolved" />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Matters by Type">
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie
                data={mattersByType}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                dataKey="value"
                nameKey="name"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              >
                {mattersByType.map((entry, i) => (
                  <Cell key={i} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <div className="flex gap-4 mb-6">
        <ChartCard title="Workload by Assignee">
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={workloadData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis type="number" tick={{ fontSize: 12, fill: '#6b7280' }} />
              <YAxis dataKey="name" type="category" tick={{ fontSize: 12, fill: '#6b7280' }} width={100} />
              <Tooltip />
              <Bar dataKey="matters" fill="#6366F1" radius={[0, 4, 4, 0]} barSize={20} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Matters by Status">
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={statusData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="name" tick={{ fontSize: 12, fill: '#6b7280' }} />
              <YAxis tick={{ fontSize: 12, fill: '#6b7280' }} />
              <Tooltip />
              <Bar dataKey="count" radius={[4, 4, 0, 0]} barSize={36}>
                {statusData.map((entry, i) => (
                  <Cell key={i} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <div className="flex gap-4 mb-6">
        <ChartCard title="Avg Response Time by Type">
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={responseTimeData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="type" tick={{ fontSize: 12, fill: '#6b7280' }} />
              <YAxis tick={{ fontSize: 12, fill: '#6b7280' }} unit="h" />
              <Tooltip formatter={(value) => [`${value} hrs`, 'Avg Response Time']} />
              <Bar dataKey="hours" fill="#8B5CF6" radius={[4, 4, 0, 0]} barSize={36} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Risk Distribution">
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie
                data={riskDistribution}
                cx="50%"
                cy="50%"
                outerRadius={100}
                dataKey="value"
                nameKey="name"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              >
                {riskDistribution.map((entry, i) => (
                  <Cell key={i} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 flex items-start gap-3">
        <AlertTriangle className="w-5 h-5 text-amber-600 mt-0.5 flex-shrink-0" />
        <div>
          <p className="text-sm font-semibold text-amber-800">Bottleneck Detected</p>
          <p className="text-sm text-amber-700 mt-1">
            Compliance reviews are averaging 12.3 hours — 3x longer than other request types.
            Consider adding capacity to the Compliance team or implementing automated pre-screening.
          </p>
        </div>
      </div>
    </div>
  );
}
