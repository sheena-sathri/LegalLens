import { NavLink } from 'react-router-dom';
import { Scale, DoorOpen, ClipboardList, MessageSquare, FileText, BarChart3, Shield, Settings } from 'lucide-react';

const navItems = [
  { to: '/intake', label: 'Legal Front Door', icon: DoorOpen },
  { to: '/matters', label: 'Matters', icon: ClipboardList },
  { to: '/assistant', label: 'AI Assistant', icon: MessageSquare },
  { to: '/documents', label: 'Documents', icon: FileText },
  { to: '/analytics', label: 'Analytics', icon: BarChart3 },
  { to: '/privacy', label: 'Privacy & Safety', icon: Shield },
];

export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 bottom-0 w-60 bg-slate-900 text-white flex flex-col z-50">
      <div className="px-5 pt-6 pb-4">
        <div className="flex items-center gap-2.5">
          <Scale className="w-7 h-7 text-indigo-400" />
          <div>
            <div className="text-lg font-bold tracking-tight">LegalLens</div>
            <div className="text-xs text-slate-400">AI Legal Hub</div>
          </div>
        </div>
      </div>

      <div className="h-px bg-slate-700 mx-4" />

      <nav className="flex-1 px-3 py-3 space-y-0.5 overflow-y-auto scrollbar-thin">
        {navItems.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-indigo-600/20 text-indigo-300'
                  : 'text-slate-300 hover:bg-slate-800 hover:text-white'
              }`
            }
          >
            <Icon className="w-[18px] h-[18px] shrink-0" />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="h-px bg-slate-700 mx-4" />

      <div className="px-3 py-2">
        <NavLink
          to="/settings"
          className={({ isActive }) =>
            `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
              isActive
                ? 'bg-indigo-600/20 text-indigo-300'
                : 'text-slate-300 hover:bg-slate-800 hover:text-white'
            }`
          }
        >
          <Settings className="w-[18px] h-[18px] shrink-0" />
          Settings
        </NavLink>
      </div>

      <div className="px-5 py-4">
        <p className="text-[11px] text-slate-500 leading-relaxed">
          Built for enterprise<br />legal teams
        </p>
      </div>
    </aside>
  );
}
