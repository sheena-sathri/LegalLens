import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Clock, Upload, FileText, User, Calendar, Building, AlertTriangle, CheckCircle2, Circle, Tag, Briefcase } from 'lucide-react';
import { StatusBadge, PriorityBadge, Badge } from '../components/Badge';
import { matters } from '../data/mockData';

const tabs = ['Overview', 'Documents', 'Activity', 'Tasks'];

const timelineIcons = {
  analysis: AlertTriangle,
  upload: Upload,
  assign: User,
  classify: Tag,
  create: Clock,
};

function DetailItem({ icon: Icon, label, value }) {
  return (
    <div className="flex items-start gap-3">
      <div className="w-8 h-8 bg-gray-50 rounded-lg flex items-center justify-center flex-shrink-0">
        <Icon className="w-4 h-4 text-gray-400" />
      </div>
      <div>
        <p className="text-xs text-gray-500">{label}</p>
        <p className="text-sm font-medium text-gray-900">{value}</p>
      </div>
    </div>
  );
}

export default function MatterDetailPage() {
  const { id } = useParams();
  const [activeTab, setActiveTab] = useState('Overview');

  const matter = matters.find((m) => m.id === id);

  if (!matter) {
    return (
      <div className="p-6">
        <Link to="/matters" className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700 mb-4">
          <ArrowLeft className="w-4 h-4" /> Back to Matters
        </Link>
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-12 text-center">
          <p className="text-gray-500">Matter not found.</p>
        </div>
      </div>
    );
  }

  const createdDate = new Date(matter.createdAt).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
  });

  const sampleDocuments = [
    { name: `${matter.type.toLowerCase().replace(/\s+/g, '_')}_draft.pdf`, size: '2.4 MB', uploaded: createdDate },
    ...(matter.documents > 1
      ? [{ name: 'redline_comparison.pdf', size: '1.8 MB', uploaded: createdDate }]
      : []),
    ...(matter.documents > 2
      ? [{ name: 'supporting_materials.pdf', size: '3.1 MB', uploaded: createdDate }]
      : []),
  ];

  return (
    <div className="p-6">
      <Link to="/matters" className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700 mb-4">
        <ArrowLeft className="w-4 h-4" /> Back to Matters
      </Link>

      <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6 mb-6">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <span className="text-xs text-gray-500 font-mono">{matter.id}</span>
              <StatusBadge status={matter.status} />
            </div>
            <h1 className="text-xl font-bold text-gray-900">{matter.title}</h1>
          </div>
          <PriorityBadge priority={matter.priority} />
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-5 pt-5 border-t border-gray-100">
          <div>
            <p className="text-xs text-gray-500">Requester</p>
            <p className="text-sm font-medium text-gray-900">{matter.requester.name}</p>
            <p className="text-xs text-gray-400">{matter.requester.department}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500">Assignee</p>
            <p className="text-sm font-medium text-gray-900">{matter.assignee.name}</p>
            <p className="text-xs text-gray-400">{matter.assignee.team}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500">Created</p>
            <p className="text-sm font-medium text-gray-900">{createdDate}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500">Due Date</p>
            <p className="text-sm font-medium text-gray-900">{matter.dueDate}</p>
          </div>
        </div>
      </div>

      <div className="border-b border-gray-200 mb-6">
        <nav className="flex gap-6">
          {tabs.map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`pb-3 text-sm font-medium border-b-2 transition-colors ${
                activeTab === tab
                  ? 'border-indigo-600 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              {tab}
            </button>
          ))}
        </nav>
      </div>

      {activeTab === 'Overview' && (
        <div className="space-y-6">
          <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-6 h-6 bg-indigo-100 rounded flex items-center justify-center">
                <Briefcase className="w-3.5 h-3.5 text-indigo-600" />
              </div>
              <h3 className="text-sm font-semibold text-gray-900">AI Summary</h3>
            </div>
            <p className="text-sm text-gray-600 leading-relaxed">{matter.summary}</p>
          </div>
          <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6">
            <h3 className="text-sm font-semibold text-gray-900 mb-4">Details</h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-5">
              <DetailItem icon={Tag} label="Type" value={matter.type} />
              <DetailItem icon={AlertTriangle} label="Priority" value={matter.priority} />
              <DetailItem icon={Calendar} label="Due Date" value={matter.dueDate} />
              <DetailItem icon={User} label="Requester" value={matter.requester.name} />
              <DetailItem icon={Building} label="Department" value={matter.requester.department} />
              <DetailItem icon={Briefcase} label="Entity" value={matter.entity} />
            </div>
          </div>
        </div>
      )}

      {activeTab === 'Documents' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-gray-900">{sampleDocuments.length} Documents</h3>
            <button className="inline-flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors">
              <Upload className="w-4 h-4" />
              Upload
            </button>
          </div>
          {sampleDocuments.map((doc, i) => (
            <div key={i} className="bg-white border border-gray-200 rounded-lg shadow-sm p-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-indigo-50 rounded-lg flex items-center justify-center">
                  <FileText className="w-5 h-5 text-indigo-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-900">{doc.name}</p>
                  <p className="text-xs text-gray-400">{doc.size} · Uploaded {doc.uploaded}</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <button className="px-3 py-1.5 text-xs font-medium text-indigo-600 bg-indigo-50 rounded-md hover:bg-indigo-100 transition-colors">
                  View Analysis
                </button>
                <button className="px-3 py-1.5 text-xs font-medium text-gray-600 bg-gray-50 rounded-md hover:bg-gray-100 transition-colors">
                  Extract Clauses
                </button>
                <button className="px-3 py-1.5 text-xs font-medium text-gray-600 bg-gray-50 rounded-md hover:bg-gray-100 transition-colors">
                  Compare
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'Activity' && (
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6">
          <h3 className="text-sm font-semibold text-gray-900 mb-4">Activity Timeline</h3>
          <div className="space-y-0">
            {matter.timeline.map((event, i) => {
              const IconComp = timelineIcons[event.icon] || Clock;
              return (
                <div key={i} className="flex gap-4 relative">
                  <div className="flex flex-col items-center">
                    <div className="w-8 h-8 bg-gray-50 border border-gray-200 rounded-full flex items-center justify-center z-10">
                      <IconComp className="w-4 h-4 text-gray-500" />
                    </div>
                    {i < matter.timeline.length - 1 && (
                      <div className="w-px h-full bg-gray-200 flex-1" />
                    )}
                  </div>
                  <div className="pb-6">
                    <p className="text-sm font-medium text-gray-900">{event.action}</p>
                    <p className="text-xs text-gray-500 mt-0.5">{event.detail}</p>
                    <p className="text-xs text-gray-400 mt-1">{event.time}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {activeTab === 'Tasks' && (
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6">
          <h3 className="text-sm font-semibold text-gray-900 mb-4">
            Tasks ({matter.tasks.filter((t) => t.done).length}/{matter.tasks.length} complete)
          </h3>
          <div className="space-y-3">
            {matter.tasks.map((task) => (
              <div key={task.id} className="flex items-center gap-3">
                {task.done ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-500 flex-shrink-0" />
                ) : (
                  <Circle className="w-5 h-5 text-gray-300 flex-shrink-0" />
                )}
                <span className={`text-sm ${task.done ? 'text-gray-400 line-through' : 'text-gray-700'}`}>
                  {task.text}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
