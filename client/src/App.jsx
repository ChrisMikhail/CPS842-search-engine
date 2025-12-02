import './App.css';
import HomePage from './components/HomePage';
import { ThemeProvider } from '@/components/theme-provider';
import { SidebarProvider } from './components/ui/sidebar';
import AppSidebar from './components/AppSidebar';
import { useState } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { SearchProvider } from './hooks/context/SearchContext';
import AppHeader from './components/AppHeader';

function App() {
  const location = useLocation();
  const showBackground = location.pathname === '/' || location.pathname === '/search';
  return (
    <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
      <SearchProvider>
        <SidebarProvider>
          <AppSidebar />
          {showBackground ? (
            <div className="app-bg">
              <div className="app-root w-full min-h-screen flex flex-col">
                {/* <AppHeader /> */}
                <Outlet />
              </div>
            </div>
          ) : (
            <div className="app-root w-full min-h-screen flex flex-col">
              {/* <AppHeader /> */}
              <Outlet />
            </div>
          )}
        </SidebarProvider>
      </SearchProvider>
    </ThemeProvider>
  );
}

export default App;
