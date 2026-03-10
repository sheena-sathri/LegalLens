import React, { useState, useEffect } from 'react';
import { Settings, Server, Bell, Key, Users, CheckCircle2, XCircle, RefreshCw } from 'lucide-react';
import { healthCheck } from '../services/api';

const configSections = [
  {
    title: 'General',
    icon: Settings,
    description: 'Application preferences, default language, timezone, and display settings.',
  },
  {
    title: 'Notifications',
    icon: Bell,
    description: 'Configure email, Slack, and in-app notification preferences for matter updates and deadlines.',
  },
  {
    title: 'API Keys',
    icon: Key,
    description: 'Manage API keys for LLM providers, integrations, and external services.',
  },
  {
    title: 'Team Management',
    icon: Users,
    description: 'Add or remove team members, assign roles, and manage permissions across your organization.',
  },
];

export default function SettingsPage() {
  const [health, setHealth] = useState(null);
  const [healthLoading, setHealthLoading] = useState(true);
  const [healthError, setHealthError] = useState(null);

  const fetchHealth = () => {
    setHealthLoading(true);
    setHealthError(null);
    healthCheck()
      .then((data) => {
        setHealth(data);
        setHealthLoading(false);
      })
      .catch(() => {
        setHealthError('Unable to reach API');
        setHealthLoading(false);
      });
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="text-sm text-gray-500 mt-1">System configuration and preferences</p>
      </div>

      <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-indigo-50 flex items-center justify-center">
              <Server className="w-5 h-5 text-indigo-600" />
            </div>
            <h2 className="text-lg font-semibold text-gray-900">System Info</h2>
          </div>
          <button
            onClick={fetchHealth}
            className="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-indigo-600 transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${healthLoading ? 'animate-spin' : ''}`} /> Refresh
          </button>
        </div>
        {healthLoading ? (
          <div className="text-sm text-gray-500">Checking API status...</div>
        ) : healthError ? (
          <div className="flex items-center gap-2 text-sm">
            <XCircle className="w-5 h-5 text-rose-500" />
            <span className="text-rose-600 font-medium">{healthError}</span>
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-xs text-gray-500 mb-1">API Status</p>
              <div className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                <span className="text-sm font-medium text-gray-900">
                  {health?.status || 'Healthy'}
                </span>
              </div>
            </div>
            <div>
              <p className="text-xs text-gray-500 mb-1">Version</p>
              <p className="text-sm font-medium text-gray-900">{health?.version || '1.0.0'}</p>
            </div>
            <div>
              <p className="text-xs text-gray-500 mb-1">Environment</p>
              <p className="text-sm font-medium text-gray-900">{health?.environment || 'Production'}</p>
            </div>
            <div>
              <p className="text-xs text-gray-500 mb-1">Uptime</p>
              <p className="text-sm font-medium text-gray-900">{health?.uptime || 'N/A'}</p>
            </div>
          </div>
        )}
      </div>

      <div className="space-y-4">
        {configSections.map((section) => (
          <div key={section.title} className="bg-white border border-gray-200 rounded-lg shadow-sm p-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-gray-50 flex items-center justify-center">
                <section.icon className="w-5 h-5 text-gray-600" />
              </div>
              <div>
                <h3 className="text-base font-semibold text-gray-900">{section.title}</h3>
                <p className="text-sm text-gray-500">{section.description}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
