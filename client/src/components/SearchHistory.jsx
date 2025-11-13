import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from './ui/sidebar';
import { NavLink } from 'react-router';
import { useSearchHistory } from '@/hooks/context/SearchHistoryContext';
import { ScrollArea, ScrollBar } from './ui/scroll-area';

export default function SearchHistory() {
  const { allQueries } = useSearchHistory();

  return (
    <SidebarGroup className="group-data-[collapsible=icon]:hidden mt-auto">
      {/* <ScrollArea> */}
      {/* <ScrollBar /> */}
      <SidebarGroupLabel>Searches</SidebarGroupLabel>
      <SidebarMenu>
        {allQueries.map((query, index) => (
          <SidebarMenuItem key={index}>
            <SidebarMenuButton asChild>
              <NavLink to={`/${index}`} title={query}>
                {query}
              </NavLink>
            </SidebarMenuButton>
          </SidebarMenuItem>
        ))}
      </SidebarMenu>
      {/* </ScrollArea> */}
    </SidebarGroup>
  );
}
