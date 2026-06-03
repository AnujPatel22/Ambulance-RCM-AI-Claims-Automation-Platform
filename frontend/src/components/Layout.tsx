import {
  Activity,
  Ambulance,
  ClipboardCheck,
  FileSearch,
  LayoutDashboard,
  PenLine
} from 'lucide-react';
import { ReactNode } from 'react';

export type PageKey = 'dashboard' | 'documentation' | 'claims' | 'denials' | 'rules';

type LayoutProps = {
  currentPage: PageKey;
  onNavigate: (page: PageKey) => void;
  children: ReactNode;
};

const navItems: Array<{ key: PageKey; label: string; icon: ReactNode }> = [
  { key: 'dashboard', label: 'Dashboard', icon: <LayoutDashboard size={18} /> },
  { key: 'documentation', label: 'Ambient Docs', icon: <PenLine size={18} /> },
  { key: 'claims', label: 'Claims Queue', icon: <ClipboardCheck size={18} /> },
  { key: 'denials', label: 'Denials', icon: <Activity size={18} /> },
  { key: 'rules', label: 'Rules', icon: <FileSearch size={18} /> }
];

export default function Layout({ currentPage, onNavigate, children }: LayoutProps) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">
            <Ambulance size={24} />
          </div>
          <div>
            <strong>Ambulance RCM</strong>
            <span>AI claims demo</span>
          </div>
        </div>

        <nav className="nav-list" aria-label="Primary">
          {navItems.map((item) => (
            <button
              key={item.key}
              className={currentPage === item.key ? 'nav-button active' : 'nav-button'}
              onClick={() => onNavigate(item.key)}
              type="button"
              title={item.label}
            >
              {item.icon}
              <span>{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-note">
          <span>Synthetic data only</span>
          <strong>No PHI used</strong>
        </div>
      </aside>

      <main className="main-content">{children}</main>
    </div>
  );
}
