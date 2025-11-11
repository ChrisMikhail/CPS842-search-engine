import './App.css';
import HomePage from './components/HomePage';
import { ThemeProvider } from '@/components/theme-provider';
import { SidebarProvider } from './components/ui/sidebar';
import AppSidebar from './components/AppSidebar';

function App() {
  return (
    <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
      <SidebarProvider>
        <AppSidebar />
        <HomePage />
      </SidebarProvider>
    </ThemeProvider>
  );
}

export default App;
