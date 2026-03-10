import React, { useState } from 'react';
import { Send, FileText, ClipboardCheck, HelpCircle, AlertTriangle, Users, ArrowRight } from 'lucide-react';
import { PriorityBadge, StatusBadge, Badge } from '../components/Badge';
import { matters, slackConversation, emailIntake } from '../data/mockData';

const recentRequests = matters.slice(0, 5);

const quickActions = [
  { label: 'Request NDA', icon: FileText, text: 'I need an NDA reviewed for a new vendor partnership. They want to begin a pilot program next month and we need to finalize confidentiality terms before sharing proprietary data.' },
  { label: 'Contract Review', icon: ClipboardCheck, text: 'Please review the attached master services agreement for our upcoming vendor engagement. Key areas of concern include liability caps, indemnification, and payment terms.' },
  { label: 'Policy Question', icon: HelpCircle, text: 'I have a question about our data retention policy. Specifically, what are the requirements for retaining customer data after contract termination in the EU?' },
  { label: 'Compliance Check', icon: AlertTriangle, text: 'We need a compliance check for our new product launch. Please verify that our data processing practices align with GDPR and CCPA requirements before we go live.' },
  { label: 'Vendor Onboarding', icon: Users, text: 'We need to onboard a new analytics vendor — DataStream Inc. Please initiate the standard vendor onboarding workflow including MSA, DPA, and security questionnaire.' },
];

const mockResult = {
  matterType: 'NDA Review',
  priority: 'High',
  routing: 'Sarah Chen — Contracts Team',
  eta: '2 business days',
  matterId: 'M-2024-0143',
  confidence: 94,
};

export default function IntakePage() {
  const [inputText, setInputText] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [animating, setAnimating] = useState(false);

  const handleSubmit = () => {
    if (!inputText.trim()) return;
    setAnimating(true);
    setSubmitted(false);
    setTimeout(() => {
      setSubmitted(true);
      setAnimating(false);
    }, 600);
  };

  const handleQuickAction = (text) => {
    setInputText(text);
    setSubmitted(false);
  };

  const formatDate = (dateStr) => {
    const d = new Date(dateStr);
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
  };

  const renderSlackMessage = (msg, idx) => {
    const avatarColors = ['bg-blue-500', 'bg-indigo-500', 'bg-emerald-500', 'bg-purple-500'];
    const color = msg.isBot ? 'bg-indigo-600' : avatarColors[idx % avatarColors.length];

    const formatBotMessage = (text) => {
      const parts = text.split(/(\*\*[^*]+\*\*)/g);
      return parts.map((part, i) => {
        if (part.startsWith('**') && part.endsWith('**')) {
          return <strong key={i} className="text-white font-semibold">{part.slice(2, -2)}</strong>;
        }
        return <span key={i}>{part}</span>;
      });
    };

    return (
      <div key={idx} className={`flex gap-3 px-4 py-2 hover:bg-white/5 ${idx > 0 ? 'mt-1' : ''}`}>
        <div className={`w-9 h-9 rounded-lg ${color} flex items-center justify-center text-white text-xs font-bold flex-shrink-0 mt-0.5`}>
          {msg.avatar}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-baseline gap-2">
            <span className="text-white font-bold text-sm">{msg.user}</span>
            {msg.isBot && <span className="text-[10px] bg-indigo-500/30 text-indigo-300 px-1.5 py-0.5 rounded font-medium">APP</span>}
            <span className="text-gray-500 text-xs">{msg.time}</span>
          </div>
          <div className="text-gray-300 text-sm mt-0.5 leading-relaxed whitespace-pre-line">
            {msg.isBot ? formatBotMessage(msg.message) : msg.message}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Welcome to LegalLens</h1>
        <p className="text-gray-500 mt-1">How can we help your legal team today?</p>
      </div>

      <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-5">
        <div className="relative">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Describe your legal request — e.g., 'I need an NDA reviewed for a new vendor...'"
            className="w-full h-28 px-4 py-3 border border-gray-200 rounded-lg text-sm text-gray-900 placeholder-gray-400 resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
          <button
            onClick={handleSubmit}
            disabled={!inputText.trim() || animating}
            className="absolute bottom-3 right-3 inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="w-4 h-4" />
            Submit
          </button>
        </div>

        <div className="mt-4">
          <p className="text-xs text-gray-400 mb-2 font-medium uppercase tracking-wide">Quick Actions</p>
          <div className="flex flex-wrap gap-2">
            {quickActions.map((action) => (
              <button
                key={action.label}
                onClick={() => handleQuickAction(action.text)}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-700 hover:border-indigo-200 transition-colors"
              >
                <action.icon className="w-3.5 h-3.5" />
                {action.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {(submitted || animating) && (
        <div className={`bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden transition-all duration-500 ${animating ? 'opacity-0 translate-y-4' : 'opacity-100 translate-y-0'}`}>
          <div className="bg-indigo-600 px-5 py-3 flex items-center gap-2">
            <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
            <span className="text-white text-sm font-medium">AI Classification Complete</span>
          </div>
          <div className="p-5">
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div>
                <p className="text-xs text-gray-400 font-medium uppercase tracking-wide mb-1">Matter Type</p>
                <p className="text-sm font-semibold text-gray-900">{mockResult.matterType}</p>
              </div>
              <div>
                <p className="text-xs text-gray-400 font-medium uppercase tracking-wide mb-1">Priority</p>
                <PriorityBadge priority={mockResult.priority} />
              </div>
              <div>
                <p className="text-xs text-gray-400 font-medium uppercase tracking-wide mb-1">Routing</p>
                <p className="text-sm text-gray-900">{mockResult.routing}</p>
              </div>
              <div>
                <p className="text-xs text-gray-400 font-medium uppercase tracking-wide mb-1">ETA</p>
                <p className="text-sm text-gray-900">{mockResult.eta}</p>
              </div>
              <div>
                <p className="text-xs text-gray-400 font-medium uppercase tracking-wide mb-1">Matter ID</p>
                <p className="text-sm font-mono text-indigo-600 font-semibold">{mockResult.matterId}</p>
              </div>
            </div>
            <div className="mt-4 pt-4 border-t border-gray-100 flex items-center gap-2">
              <Badge color="indigo">{mockResult.confidence}% Confidence</Badge>
              <span className="text-xs text-gray-400">Auto-classified by LegalLens AI</span>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="rounded-lg shadow-sm overflow-hidden border border-gray-200">
          <div className="bg-[#1A1D21] border-b border-gray-700/50">
            <div className="px-4 py-3 flex items-center gap-2">
              <span className="text-white font-bold text-sm"># legal-requests</span>
              <span className="text-gray-500 text-xs">|</span>
              <span className="text-gray-500 text-xs">3 members</span>
            </div>
          </div>
          <div className="bg-[#1A1D21] py-3">
            {slackConversation.map((msg, idx) => renderSlackMessage(msg, idx))}
          </div>
          <div className="bg-[#1A1D21] px-4 py-3 border-t border-gray-700/50">
            <div className="bg-[#222529] rounded-lg px-3 py-2 flex items-center gap-2">
              <span className="text-gray-500 text-sm">Message #legal-requests</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div className="px-5 py-3 border-b border-gray-200 bg-gray-50">
            <p className="text-sm font-semibold text-gray-900">Email Intake</p>
          </div>
          <div className="p-5 space-y-3">
            <div className="space-y-1.5 text-sm">
              <div className="flex gap-2">
                <span className="text-gray-400 w-16 flex-shrink-0">From</span>
                <span className="text-gray-900">{emailIntake.from}</span>
              </div>
              <div className="flex gap-2">
                <span className="text-gray-400 w-16 flex-shrink-0">To</span>
                <span className="text-gray-900">{emailIntake.to}</span>
              </div>
              <div className="flex gap-2">
                <span className="text-gray-400 w-16 flex-shrink-0">Subject</span>
                <span className="text-gray-900 font-medium">{emailIntake.subject}</span>
              </div>
              <div className="flex gap-2">
                <span className="text-gray-400 w-16 flex-shrink-0">Date</span>
                <span className="text-gray-900">{emailIntake.date}</span>
              </div>
            </div>
            <div className="border-t border-gray-100 pt-3">
              <p className="text-sm text-gray-700 whitespace-pre-line leading-relaxed">{emailIntake.body}</p>
            </div>
            <div className="bg-indigo-50 border border-indigo-100 rounded-lg p-4 mt-3">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-5 h-5 bg-indigo-600 rounded flex items-center justify-center">
                  <span className="text-white text-[10px] font-bold">AI</span>
                </div>
                <span className="text-sm font-semibold text-indigo-900">AI Analysis</span>
              </div>
              <div className="grid grid-cols-2 gap-y-2 gap-x-4 text-sm">
                <div>
                  <span className="text-indigo-400 text-xs uppercase tracking-wide">Classification</span>
                  <p className="text-indigo-900 font-medium">{emailIntake.analysis.classification}</p>
                </div>
                <div>
                  <span className="text-indigo-400 text-xs uppercase tracking-wide">Confidence</span>
                  <p className="text-indigo-900 font-medium">{emailIntake.analysis.confidence}%</p>
                </div>
                <div>
                  <span className="text-indigo-400 text-xs uppercase tracking-wide">Priority</span>
                  <PriorityBadge priority={emailIntake.analysis.priority} />
                </div>
                <div>
                  <span className="text-indigo-400 text-xs uppercase tracking-wide">Matter ID</span>
                  <p className="text-indigo-900 font-mono font-medium">{emailIntake.analysis.matterId}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
        <div className="px-5 py-3 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-sm font-semibold text-gray-900">Recent Requests</h2>
          <button className="inline-flex items-center gap-1 text-xs text-indigo-600 hover:text-indigo-700 font-medium">
            View all <ArrowRight className="w-3 h-3" />
          </button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 text-left">
                <th className="px-5 py-2.5 text-xs font-medium text-gray-500 uppercase tracking-wide">ID</th>
                <th className="px-5 py-2.5 text-xs font-medium text-gray-500 uppercase tracking-wide">Title</th>
                <th className="px-5 py-2.5 text-xs font-medium text-gray-500 uppercase tracking-wide">Type</th>
                <th className="px-5 py-2.5 text-xs font-medium text-gray-500 uppercase tracking-wide">Status</th>
                <th className="px-5 py-2.5 text-xs font-medium text-gray-500 uppercase tracking-wide">Priority</th>
                <th className="px-5 py-2.5 text-xs font-medium text-gray-500 uppercase tracking-wide">Assignee</th>
                <th className="px-5 py-2.5 text-xs font-medium text-gray-500 uppercase tracking-wide">Created</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {recentRequests.map((matter) => (
                <tr key={matter.id} className="hover:bg-gray-50 transition-colors cursor-pointer">
                  <td className="px-5 py-3 font-mono text-indigo-600 font-medium">{matter.id}</td>
                  <td className="px-5 py-3 text-gray-900 font-medium">{matter.title}</td>
                  <td className="px-5 py-3 text-gray-600">{matter.type}</td>
                  <td className="px-5 py-3"><StatusBadge status={matter.status} /></td>
                  <td className="px-5 py-3"><PriorityBadge priority={matter.priority} /></td>
                  <td className="px-5 py-3 text-gray-600">{matter.assignee.name}</td>
                  <td className="px-5 py-3 text-gray-400">{formatDate(matter.createdAt)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
