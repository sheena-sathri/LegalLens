import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
});

export const searchAsk = async (question) => {
  const res = await api.post('/search/ask', { question });
  return res.data;
};

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await api.post('/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
};

export const listDocuments = async () => {
  const res = await api.get('/documents/');
  return res.data;
};

export const classifyDocument = async (docId) => {
  const res = await api.post(`/analysis/classify/${docId}`);
  return res.data;
};

export const extractClauses = async (docId) => {
  const res = await api.post(`/analysis/extract/${docId}`);
  return res.data;
};

export const compareDocuments = async (docIds) => {
  const res = await api.post('/analysis/compare', { document_ids: docIds });
  return res.data;
};

export const getAuditReport = async () => {
  const res = await api.get('/governance/audit/report');
  return res.data;
};

export const healthCheck = async () => {
  const res = await axios.get('/health');
  return res.data;
};

export default api;
