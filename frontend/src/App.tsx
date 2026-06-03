import { useState } from 'react';
import Layout, { PageKey } from './components/Layout';
import Dashboard from './pages/Dashboard';
import AmbientDocumentation from './pages/AmbientDocumentation';
import ClaimsQueue from './pages/ClaimsQueue';
import DenialManagement from './pages/DenialManagement';
import RulesExplorer from './pages/RulesExplorer';

export default function App() {
  const [page, setPage] = useState<PageKey>('dashboard');

  return (
    <Layout currentPage={page} onNavigate={setPage}>
      {page === 'dashboard' && <Dashboard />}
      {page === 'documentation' && <AmbientDocumentation />}
      {page === 'claims' && <ClaimsQueue />}
      {page === 'denials' && <DenialManagement />}
      {page === 'rules' && <RulesExplorer />}
    </Layout>
  );
}
