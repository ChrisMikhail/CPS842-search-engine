import {
  Sidebar,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarTrigger,
  useSidebar,
} from '@/components/ui/sidebar';
import SearchHistory from './SearchHistory';
import Logo from './Logo';
import { ModeToggle } from './ui/mode-toggle';
import { cn } from '@/lib/utils';

export default function AppSidebar() {
  const { open } = useSidebar();
  return (
    <Sidebar variant="sidebar" collapsible="icon" className="h-screen">
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem className="flex flex-row items-center">
            {/* <SidebarMenuButton className="data-[slot=sidebar-menu-button]:p-1.5!"> */}
            <SidebarTrigger className="hover:cursor-pointer" />
            {open && <Logo />}
            {/* </SidebarMenuButton> */}
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SearchHistory />
      <SidebarFooter className={cn('border-t', !open && 'mt-auto')}>
        <ModeToggle />
      </SidebarFooter>
    </Sidebar>
  );
}
