import './App.css';
import HomePage from './components/HomePage';
import { ThemeProvider } from '@/components/theme-provider';
import { SidebarProvider } from './components/ui/sidebar';
import AppSidebar from './components/AppSidebar';
import { useState } from 'react';
import { Outlet } from 'react-router';
import { SearchProvider } from './hooks/context/SearchContext';
import AppHeader from './components/AppHeader';

function App() {
  return (
    <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
      <SearchProvider>
        <SidebarProvider>
          <AppSidebar />
          <main className="w-screen h-screen flex flex-col">
            {/* <AppHeader /> */}
            <Outlet />
          </main>
        </SidebarProvider>
      </SearchProvider>
    </ThemeProvider>
  );
}

export default App;
