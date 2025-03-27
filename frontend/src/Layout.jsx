
import React from "react";
import { Link } from "react-router-dom";

const Layout = ({ children }) => {
  return (
    <div className="flex h-screen bg-slate-900 text-white">
      <aside className="w-64 bg-slate-800 p-4 space-y-4 shadow-xl">
        <h1 className="text-xl font-bold text-cyan-400 mb-6">Cate Explorer</h1>
        <nav className="flex flex-col space-y-2">
          <Link to="/" className="hover:text-cyan-300">📚 Agency Explorer</Link>
          <Link to="/metrics" className="hover:text-cyan-300">📊 Metrics Dashboard</Link>
        </nav>
      </aside>
      <main className="flex-1 overflow-y-auto p-6">{children}</main>
    </div>
  );
};

export default Layout;
