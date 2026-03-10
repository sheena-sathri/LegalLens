import React, { useState, useEffect } from 'react';
import {
  Shield, Upload, FileSearch, ScanEye, Layers, Send, Brain, ClipboardList,
  Check, X, Server, Cloud, Eye, Lock, Database, Key, Download,
  CheckCircle2, XCircle, ArrowRight
} from 'lucide-react';
import { getAuditReport } from '../services/api';
import { integrations } from '../data/mockData';

const pipelineSteps = [
  { icon: Upload, label: 'Upload', desc: 'Document received via intake channel' },
  { icon: FileSearch, label: 'Extract', desc: 'Text extraction & OCR processing' },
  { icon: ScanEye, label: 'PII Scan', desc: 'Automatic PII detection & redaction' },
  { icon: Layers, label: 'Chunk', desc: 'Smart chunking with overlap' },
  { icon: Send, label: 'Send to LLM', desc: 'Redacted chunks sent to model' },
  { icon: Brain, label: 'Analysis', desc: 'AI-powered clause & risk analysis' },
  { icon: ClipboardList, label: 'Audit Log', desc: 'Every action immutably logged' },
];

const guarantees = [
  { text: 'No client data used for model training', safe: true },
  { text: 'PII automatically redacted before LLM processing', safe: true },
  { text: 'All API calls encrypted with TLS 1.3', safe: true },
  { text: 'Full audit trail for every document interaction', safe: true },
  { text: 'Raw documents never leave your infrastructure', safe: true },
  { text: 'No third-party data sharing without consent', safe: true },
];

const aiSteps = [
  { step: 1, title: 'Document Received', desc: 'File uploaded via Slack, email, or direct upload. Stored in your encrypted storage.' },
  { step: 2, title: 'Text Extraction', desc: 'Text is extracted locally. Original file remains in your infrastructure only.' },
  { step: 3, title: 'PII Detection & Redaction', desc: 'Names, dates, amounts, and identifiers are detected and replaced with tokens like [PARTY_A], [DATE_1].' },
  { step: 4, title: 'Smart Chunking', desc: 'Redacted text is split into overlapping chunks optimized for LLM context windows.' },
  { step: 5, title: 'LLM Analysis', desc: 'Only redacted chunks are sent to the model. The LLM never sees original PII or identifying information.' },
  { step: 6, title: 'Results Mapped Back', desc: 'AI analysis results are mapped back to original document with PII restored for your team only.' },
];

const modelComparison = [
  { feature: 'Data Privacy', selfHosted: 'Full control — no data leaves your network', api: 'Encrypted in transit, provider processes data' },
  { feature: 'Latency', selfHosted: '~200ms (local inference)', api: '~800ms (network round-trip)' },
  { feature: 'Cost', selfHosted: 'GPU infrastructure required', api: 'Pay-per-token, no infra needed' },
  { feature: 'Model Quality', selfHosted: 'Llama 3, Mistral, custom fine-tuned', api: 'GPT-4o, Claude 3.5 Sonnet' },
  { feature: 'Compliance', selfHosted: 'Ideal for air-gapped / regulated environments', api: 'SOC 2 certified providers' },
  { feature: 'Scalability', selfHosted: 'Limited by hardware', api: 'Virtually unlimited' },
];

const complianceBadges = [
  { name: 'SOC 2 Type II', icon: Shield },
  { name: 'ISO 27001', icon: Lock },
  { name: 'GDPR', icon: Database },
  { name: 'CCPA', icon: Key },
  { name: 'EU AI Act', icon: Brain },
];

export default function PrivacyPage() {
  const [auditData, setAuditData] = useState([]);
  const [auditLoading, setAuditLoading] = useState(true);
  const [auditError, setAuditError] = useState(null);

  useEffect(() => {
    getAuditReport()
      .then((data) => {
        setAuditData(Array.isArray(data) ? data : data?.entries || data?.report || []);
        setAuditLoading(false);
      })
      .catch((err) => {
        setAuditError('Unable to load audit data');
        setAuditLoading(false);
      });
  }, []);

  const exportCSV = () => {
    if (!auditData.length) return;
    const headers = Object.keys(auditData[0]);
    const csv = [headers.join(','), ...auditData.map((row) => headers.map((h) => `"${row[h] || ''}"`).join(','))].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'audit_report.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-black">Privacy & LLM Safety</h1>
        <p className="text-base text-black mt-1">How LegalLens keeps your most sensitive data secure</p>
      </div>

      <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6 mb-6">
        <h2 className="text-lg font-semibold text-black mb-6">Data Flow Pipeline</h2>
        <div className="flex items-start justify-between gap-2 mb-8 overflow-x-auto">
          {pipelineSteps.map((step, i) => (
            <React.Fragment key={step.label}>
              <div className="flex flex-col items-center text-center min-w-[100px]">
                <div className="w-12 h-12 rounded-full bg-indigo-50 flex items-center justify-center mb-2">
                  <step.icon className="w-6 h-6 text-indigo-600" />
                </div>
                <p className="text-sm font-semibold text-black">{step.label}</p>
                <p className="text-xs text-black mt-1 max-w-[120px]">{step.desc}</p>
              </div>
              {i < pipelineSteps.length - 1 && (
                <ArrowRight className="w-5 h-5 text-gray-300 mt-4 flex-shrink-0" />
              )}
            </React.Fragment>
          ))}
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {guarantees.map((g) => (
            <div key={g.text} className="flex items-start gap-2">
              {g.safe ? (
                <CheckCircle2 className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5" />
              ) : (
                <XCircle className="w-5 h-5 text-rose-500 flex-shrink-0 mt-0.5" />
              )}
              <span className="text-sm text-black">{g.text}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="flex gap-4 mb-6">
        <div className="flex-1 bg-white border border-gray-200 rounded-lg shadow-sm p-6 relative">
          <div className="absolute top-4 right-4">
            <span className="inline-flex items-center gap-1 bg-emerald-50 text-emerald-700 text-xs font-medium px-2.5 py-1 rounded-full ring-1 ring-inset ring-emerald-600/10">
              <CheckCircle2 className="w-3.5 h-3.5" /> Currently Active
            </span>
          </div>
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-lg bg-indigo-50 flex items-center justify-center">
              <Server className="w-5 h-5 text-indigo-600" />
            </div>
            <h3 className="text-lg font-semibold text-black">Self-Hosted / Air-Gapped</h3>
          </div>
          <p className="text-sm text-black mb-4">Full deployment within your infrastructure. No data ever leaves your network perimeter.</p>
          <ul className="space-y-2">
            <li className="flex items-center gap-2 text-sm text-black"><Check className="w-4 h-4 text-emerald-500" /> On-premise LLM inference (Llama 3, Mistral)</li>
            <li className="flex items-center gap-2 text-sm text-black"><Check className="w-4 h-4 text-emerald-500" /> Local vector database (ChromaDB)</li>
            <li className="flex items-center gap-2 text-sm text-black"><Check className="w-4 h-4 text-emerald-500" /> No external API calls</li>
            <li className="flex items-center gap-2 text-sm text-black"><Check className="w-4 h-4 text-emerald-500" /> FIPS 140-2 compliant encryption</li>
          </ul>
        </div>
        <div className="flex-1 bg-white border border-gray-200 rounded-lg shadow-sm p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center">
              <Cloud className="w-5 h-5 text-blue-600" />
            </div>
            <h3 className="text-lg font-semibold text-black">Hybrid</h3>
          </div>
          <p className="text-sm text-black mb-4">Documents stay on-premise. Only redacted chunks sent to cloud LLMs for analysis.</p>
          <ul className="space-y-2">
            <li className="flex items-center gap-2 text-sm text-black"><Check className="w-4 h-4 text-emerald-500" /> PII redacted before cloud transmission</li>
            <li className="flex items-center gap-2 text-sm text-black"><Check className="w-4 h-4 text-emerald-500" /> Access to GPT-4o, Claude 3.5 Sonnet</li>
            <li className="flex items-center gap-2 text-sm text-black"><Check className="w-4 h-4 text-emerald-500" /> TLS 1.3 encryption in transit</li>
            <li className="flex items-center gap-2 text-sm text-black"><Check className="w-4 h-4 text-emerald-500" /> Zero data retention agreements with providers</li>
          </ul>
        </div>
      </div>

      <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6 mb-6">
        <div className="flex items-center gap-3 mb-6">
          <Eye className="w-5 h-5 text-indigo-600" />
          <h2 className="text-lg font-semibold text-black">What the AI Sees</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {aiSteps.map((s) => (
            <div key={s.step} className="border border-gray-100 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <span className="w-7 h-7 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center text-sm font-bold">{s.step}</span>
                <h4 className="text-sm font-semibold text-black">{s.title}</h4>
              </div>
              <p className="text-sm text-black">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6 mb-6">
        <h2 className="text-lg font-semibold text-black mb-4">Integrations</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {integrations.map((intg) => (
            <div key={intg.name} className="border border-gray-200 rounded-lg p-4 flex items-center gap-3">
              <span className="text-2xl">{intg.icon}</span>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold text-black">{intg.name}</p>
                <p className="text-xs text-black truncate">{intg.desc}</p>
              </div>
              {intg.connected ? (
                <span className="inline-flex items-center gap-1 text-xs font-medium text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full">
                  <CheckCircle2 className="w-3 h-3" /> Connected
                </span>
              ) : (
                <span className="text-xs text-gray-400">Available</span>
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6 mb-6">
        <h2 className="text-lg font-semibold text-black mb-4">Model Selection Guide</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-medium text-black">Feature</th>
                <th className="text-left py-3 px-4 font-medium text-black">
                  <div className="flex items-center gap-2"><Server className="w-4 h-4 text-indigo-600" /> Self-Hosted</div>
                </th>
                <th className="text-left py-3 px-4 font-medium text-black">
                  <div className="flex items-center gap-2"><Cloud className="w-4 h-4 text-blue-600" /> API Models</div>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {modelComparison.map((row) => (
                <tr key={row.feature}>
                  <td className="py-3 px-4 font-medium text-black">{row.feature}</td>
                  <td className="py-3 px-4 text-black">{row.selfHosted}</td>
                  <td className="py-3 px-4 text-black">{row.api}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-black">Audit Trail</h2>
          <button
            onClick={exportCSV}
            disabled={!auditData.length}
            className="inline-flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Download className="w-4 h-4" /> Export CSV
          </button>
        </div>
        {auditLoading ? (
          <div className="text-center py-8 text-black">Loading audit data...</div>
        ) : auditError ? (
          <div className="text-center py-8 text-amber-600">{auditError}</div>
        ) : auditData.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50">
                  {Object.keys(auditData[0]).map((key) => (
                    <th key={key} className="text-left py-3 px-4 font-medium text-black capitalize">
                      {key.replace(/_/g, ' ')}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {auditData.slice(0, 20).map((row, i) => (
                  <tr key={i} className="hover:bg-gray-50">
                    {Object.values(row).map((val, j) => (
                      <td key={j} className="py-3 px-4 text-black">{String(val)}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-8 text-black">No audit entries found</div>
        )}
      </div>

      <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6">
        <h2 className="text-lg font-semibold text-black mb-4">Compliance & Certifications</h2>
        <div className="flex items-center justify-center gap-8">
          {complianceBadges.map((badge) => (
            <div key={badge.name} className="flex flex-col items-center gap-2">
              <div className="w-14 h-14 rounded-full bg-indigo-50 flex items-center justify-center">
                <badge.icon className="w-7 h-7 text-indigo-600" />
              </div>
              <span className="text-sm font-semibold text-black">{badge.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
