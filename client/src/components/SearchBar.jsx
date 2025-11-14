import { ArrowUp } from 'lucide-react';

import {
  InputGroup,
  InputGroupButton,
  InputGroupTextarea,
} from '@/components/ui/input-group';
import { NavLink } from 'react-router';
import { useSearch } from '@/hooks/context/SearchContext';
import { cn } from '@/lib/utils';

export default function SearchBar({ className }) {
  const { query, setQuery, handleSubmit, handleKeyDown } = useSearch();
  return (
    <InputGroup className="w-full max-w-3xl">
      <InputGroupTextarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search crafting recipes"
        rows={1}
        className={cn(
          'w-full text-base rounded-2xl focus:outline-none resize-none p-9',
          className,
        )}
        onKeyDown={handleKeyDown}
      />

      <InputGroupButton
        onClick={handleSubmit}
        disabled={!query.trim()}
        className="absolute right-2 bottom-2 w-10 h-10 rounded-full flex items-center justify-center border-2 disabled:opacity-30 disabled:cursor-not-allowed hover:cursor-pointer bg-amber-400 hover:bg-amber-700  dark:hover:bg-amber-700"
      >
        <NavLink to={`/${query}`}>
          <ArrowUp className="w-5 h-5 text-secondary" />
          <span className="sr-only">Send</span>
        </NavLink>
      </InputGroupButton>
    </InputGroup>
  );
}
