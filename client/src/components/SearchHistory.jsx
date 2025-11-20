import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from './ui/sidebar';
import { NavLink } from 'react-router';
import { useSearch } from '@/hooks/context/SearchContext';
import { ScrollArea, ScrollBar } from './ui/scroll-area';

export default function SearchHistory() {
  const { allQueries } = useSearch();

  return (
    <SidebarGroup className="group-data-[collapsible=icon]:hidden mt-auto">
      <SidebarGroupLabel>Searches</SidebarGroupLabel>
      <ScrollArea className="max-h-120">
        <SidebarMenu>
          {allQueries.map((query, index) => (
            <SidebarMenuItem key={index}>
              <SidebarMenuButton asChild>
                <NavLink to={`/${index}`} title={query} className="truncate">
                  {query}
                </NavLink>
              </SidebarMenuButton>
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </ScrollArea>
    </SidebarGroup>
  );
}
