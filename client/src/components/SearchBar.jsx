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
    <InputGroup
      className={cn(
        'w-full max-w-3xl flex flex-row items-start p-2 gap-2',
        className,
      )}
    >
      <InputGroupTextarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search crafting recipes"
        className={'w-full p-0 min-h-10 text-lg'}
        onKeyDown={handleKeyDown}
      />

      <InputGroupButton
        onClick={handleSubmit}
        disabled={!query.trim()}
        className="size-10 rounded-md flex items-center justify-center border disabled:opacity-30 disabled:cursor-not-allowed hover:cursor-pointer bg-amber-400 hover:bg-amber-700 dark:hover:bg-amber-700"
      >
        <NavLink to={`/${query}`}>
          <ArrowUp className="w-5 h-5 text-secondary" />
          <span className="sr-only">Send</span>
        </NavLink>
      </InputGroupButton>
    </InputGroup>
  );
}
