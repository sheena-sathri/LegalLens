import { Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import IntakePage from './pages/IntakePage';
import MattersPage from './pages/MattersPage';
import MatterDetailPage from './pages/MatterDetailPage';
import AssistantPage from './pages/AssistantPage';
import DocumentsPage from './pages/DocumentsPage';
import AnalyticsPage from './pages/AnalyticsPage';
import PrivacyPage from './pages/PrivacyPage';
import SettingsPage from './pages/SettingsPage';

export default function App() {
  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 ml-60">
        <Routes>
          <Route path="/" element={<Navigate to="/intake" replace />} />
          <Route path="/intake" element={<IntakePage />} />
          <Route path="/matters" element={<MattersPage />} />
          <Route path="/matters/:id" element={<MatterDetailPage />} />
          <Route path="/assistant" element={<AssistantPage />} />
          <Route path="/documents" element={<DocumentsPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/privacy" element={<PrivacyPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </main>
    </div>
  );
}
