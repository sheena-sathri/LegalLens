import React, { useState, useEffect, useCallback } from 'react';
import { Upload, FileText, Search, GitCompare, Shield, Loader2, AlertTriangle, CheckCircle, X } from 'lucide-react';
import { Badge } from '../components/Badge';
import { uploadDocument, listDocuments, classifyDocument, extractClauses, compareDocuments } from '../services/api';

const riskColorMap = {
  LOW: 'emerald',
  MEDIUM: 'amber',
  HIGH: 'orange',
  CRITICAL: 'rose',
};

const tabs = [
  { id: 'classify', label: 'Classify', icon: Shield },
  { id: 'extract', label: 'Extract Clauses', icon: Search },
  { id: 'compare', label: 'Compare', icon: GitCompare },
];

export default function DocumentsPage() {
  const [documents, setDocuments] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [activeTab, setActiveTab] = useState('classify');
  const [uploading, setUploading] = useState(false);
  const [loadingDocs, setLoadingDocs] = useState(true);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [compareIds, setCompareIds] = useState([]);

  const fetchDocuments = useCallback(async () => {
    setLoadingDocs(true);
    try {
      const data = await listDocuments();
      setDocuments(Array.isArray(data) ? data : data.documents || []);
    } catch {
      setDocuments([]);
    } finally {
      setLoadingDocs(false);
    }
  }, []);

  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  const handleUpload = async (files) => {
    if (!files || files.length === 0) return;
    setUploading(true);
    setError(null);
    try {
      for (const file of files) {
        await uploadDocument(file);
      }
      await fetchDocuments();
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleFileInput = (e) => {
    handleUpload(e.target.files);
    e.target.value = '';
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    handleUpload(e.dataTransfer.files);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => setDragOver(false);

  const runAnalysis = async () => {
    setAnalysisLoading(true);
    setAnalysisResult(null);
    setError(null);
    try {
      let result;
      if (activeTab === 'classify' && selectedDoc) {
        result = await classifyDocument(selectedDoc.id);
      } else if (activeTab === 'extract' && selectedDoc) {
        result = await extractClauses(selectedDoc.id);
      } else if (activeTab === 'compare' && compareIds.length >= 2) {
        result = await compareDocuments(compareIds);
      }
      setAnalysisResult(result);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Analysis failed');
    } finally {
      setAnalysisLoading(false);
    }
  };

  const toggleCompareDoc = (id) => {
    setCompareIds((prev) =>
      prev.includes(id) ? prev.filter((d) => d !== id) : prev.length < 2 ? [...prev, id] : prev
    );
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '—';
    try {
      return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    } catch {
      return dateStr;
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Document Intelligence</h1>
        <p className="mt-1 text-sm text-gray-500">Upload, classify, extract clauses, and compare legal documents</p>
      </div>

      {error && (
        <div className="flex items-center justify-between bg-rose-50 text-rose-700 rounded-lg px-4 py-3 text-sm">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
          <button onClick={() => setError(null)}>
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`bg-white rounded-lg border-2 border-dashed p-8 text-center transition-colors ${
          dragOver ? 'border-indigo-400 bg-indigo-50' : 'border-gray-300'
        }`}
      >
        {uploading ? (
          <div className="flex flex-col items-center gap-2">
            <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
            <p className="text-sm text-gray-600">Uploading document...</p>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-3">
            <Upload className="w-8 h-8 text-gray-400" />
            <div>
              <p className="text-sm font-medium text-gray-700">Drag and drop files here, or</p>
              <label className="mt-1 inline-block cursor-pointer text-sm text-indigo-600 hover:text-indigo-700 font-medium">
                browse to upload
                <input type="file" className="hidden" onChange={handleFileInput} multiple accept=".pdf,.doc,.docx,.txt" />
              </label>
            </div>
            <p className="text-xs text-gray-400">PDF, DOC, DOCX, or TXT up to 10MB</p>
          </div>
        )}
      </div>

      <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
        <div className="border-b border-gray-200 px-6 pt-4">
          <div className="flex gap-6">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => { setActiveTab(tab.id); setAnalysisResult(null); }}
                className={`flex items-center gap-2 pb-3 px-1 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === tab.id
                    ? 'border-indigo-600 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        <div className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-gray-900">Document Library</h3>
            {activeTab === 'compare' ? (
              <button
                onClick={runAnalysis}
                disabled={compareIds.length < 2 || analysisLoading}
                className="px-4 py-2 bg-indigo-600 text-white text-sm rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
              >
                {analysisLoading && <Loader2 className="w-4 h-4 animate-spin" />}
                Compare Selected ({compareIds.length}/2)
              </button>
            ) : (
              <button
                onClick={runAnalysis}
                disabled={!selectedDoc || analysisLoading}
                className="px-4 py-2 bg-indigo-600 text-white text-sm rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
              >
                {analysisLoading && <Loader2 className="w-4 h-4 animate-spin" />}
                {activeTab === 'classify' ? 'Classify' : 'Extract Clauses'}
              </button>
            )}
          </div>

          {loadingDocs ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="w-6 h-6 text-indigo-500 animate-spin" />
              <span className="ml-2 text-sm text-gray-500">Loading documents...</span>
            </div>
          ) : documents.length === 0 ? (
            <div className="text-center py-12">
              <FileText className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <h4 className="text-sm font-medium text-gray-700">No documents yet</h4>
              <p className="text-sm text-gray-400 mt-1">Upload a document above to get started with AI-powered analysis</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-200">
                    {activeTab === 'compare' && <th className="pb-3 text-left font-medium text-gray-500 w-10"></th>}
                    <th className="pb-3 text-left font-medium text-gray-500">File</th>
                    <th className="pb-3 text-left font-medium text-gray-500">Type</th>
                    <th className="pb-3 text-left font-medium text-gray-500">Classification</th>
                    <th className="pb-3 text-left font-medium text-gray-500">Risk</th>
                    <th className="pb-3 text-left font-medium text-gray-500">Date</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {documents.map((doc) => (
                    <tr
                      key={doc.id}
                      onClick={() => activeTab !== 'compare' && setSelectedDoc(doc)}
                      className={`cursor-pointer transition-colors ${
                        selectedDoc?.id === doc.id && activeTab !== 'compare'
                          ? 'bg-indigo-50'
                          : 'hover:bg-gray-50'
                      }`}
                    >
                      {activeTab === 'compare' && (
                        <td className="py-3 pr-2">
                          <input
                            type="checkbox"
                            checked={compareIds.includes(doc.id)}
                            onChange={() => toggleCompareDoc(doc.id)}
                            className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                          />
                        </td>
                      )}
                      <td className="py-3 pr-4">
                        <div className="flex items-center gap-2">
                          <FileText className="w-4 h-4 text-gray-400" />
                          <span className="font-medium text-gray-900">{doc.filename || doc.name || 'Untitled'}</span>
                        </div>
                      </td>
                      <td className="py-3 pr-4 text-gray-500">{doc.file_type || doc.type || '—'}</td>
                      <td className="py-3 pr-4">
                        {doc.classification ? (
                          <Badge color="blue">{doc.classification}</Badge>
                        ) : (
                          <span className="text-gray-400">—</span>
                        )}
                      </td>
                      <td className="py-3 pr-4">
                        {doc.risk_level ? (
                          <Badge color={riskColorMap[doc.risk_level?.toUpperCase()] || 'gray'}>{doc.risk_level}</Badge>
                        ) : (
                          <span className="text-gray-400">—</span>
                        )}
                      </td>
                      <td className="py-3 text-gray-500">{formatDate(doc.uploaded_at || doc.created_at || doc.date)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {analysisResult && (
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-gray-900 flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-emerald-500" />
              Analysis Results
            </h3>
            <button onClick={() => setAnalysisResult(null)} className="text-gray-400 hover:text-gray-600">
              <X className="w-4 h-4" />
            </button>
          </div>

          {activeTab === 'classify' && (
            <div className="space-y-3">
              {analysisResult.classification && (
                <div className="flex items-center gap-3">
                  <span className="text-sm text-gray-500 w-28">Classification:</span>
                  <Badge color="indigo">{analysisResult.classification}</Badge>
                </div>
              )}
              {analysisResult.confidence != null && (
                <div className="flex items-center gap-3">
                  <span className="text-sm text-gray-500 w-28">Confidence:</span>
                  <div className="flex items-center gap-2 flex-1">
                    <div className="h-2 flex-1 max-w-xs bg-gray-100 rounded-full overflow-hidden">
                      <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${analysisResult.confidence}%` }} />
                    </div>
                    <span className="text-sm font-medium text-gray-700">{analysisResult.confidence}%</span>
                  </div>
                </div>
              )}
              {analysisResult.summary && (
                <div>
                  <span className="text-sm text-gray-500">Summary:</span>
                  <p className="mt-1 text-sm text-gray-700">{analysisResult.summary}</p>
                </div>
              )}
            </div>
          )}

          {activeTab === 'extract' && (
            <div className="space-y-3">
              {(analysisResult.clauses || analysisResult.extracted_clauses || []).map((clause, i) => (
                <div key={i} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-900">{clause.title || clause.clause_type || clause.name || `Clause ${i + 1}`}</span>
                    {clause.risk_level && (
                      <Badge color={riskColorMap[clause.risk_level?.toUpperCase()] || 'gray'}>{clause.risk_level}</Badge>
                    )}
                  </div>
                  <p className="text-sm text-gray-600">{clause.content || clause.text || clause.description || ''}</p>
                </div>
              ))}
              {(analysisResult.clauses || analysisResult.extracted_clauses || []).length === 0 && (
                <p className="text-sm text-gray-500">No clauses found in the analysis result.</p>
              )}
            </div>
          )}

          {activeTab === 'compare' && (
            <div className="space-y-3">
              {analysisResult.differences && (
                <div>
                  <span className="text-sm font-medium text-gray-700">Differences:</span>
                  {Array.isArray(analysisResult.differences) ? (
                    <ul className="mt-2 space-y-2">
                      {analysisResult.differences.map((diff, i) => (
                        <li key={i} className="text-sm text-gray-600 border-l-2 border-amber-400 pl-3">
                          {typeof diff === 'string' ? diff : diff.description || diff.detail || JSON.stringify(diff)}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="mt-1 text-sm text-gray-600">{JSON.stringify(analysisResult.differences, null, 2)}</p>
                  )}
                </div>
              )}
              {analysisResult.summary && (
                <div>
                  <span className="text-sm font-medium text-gray-700">Summary:</span>
                  <p className="mt-1 text-sm text-gray-600">{analysisResult.summary}</p>
                </div>
              )}
              {!analysisResult.differences && !analysisResult.summary && (
                <pre className="text-sm text-gray-600 whitespace-pre-wrap">{JSON.stringify(analysisResult, null, 2)}</pre>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
