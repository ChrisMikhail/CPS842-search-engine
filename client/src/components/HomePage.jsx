import React, { useState, useRef, useEffect } from 'react';
import { Sparkles, ArrowUp, Hammer } from 'lucide-react';
import {
  InputGroup,
  InputGroupButton,
  InputGroupText,
  InputGroupTextarea,
} from './ui/input-group';
import { ModeToggle } from './ui/mode-toggle';
import Logo from './Logo';
import { SidebarTrigger } from './ui/sidebar';

export default function HomePage() {
  const [query, setQuery] = useState('');
  const [allQueries, setAllQueries] = useState([]);

  const handleSubmit = () => {
    if (query.trim()) {
      console.log('Searching:', query);
      // Handle search submission
      setAllQueries((prev) => [...prev, query]);
      setQuery('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="min-h-screen w-screen flex flex-col">
      {/* Main Content */}
      <main className="flex-1 flex flex-col items-center justify-center w-full px-4">
        {/* Logo and Title */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl mb-6 border-2">
            <Hammer className="w-10 h-10" />
          </div>
          {/* <Logo className="size-100 m-0" /> */}
          <h1 className="text-5xl font-semibold mb-3">MineFox</h1>
          <ModeToggle />
        </div>

        {/* Search Input */}
        <InputGroup className="w-full max-w-3xl">
          <InputGroupTextarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search crafting recipes"
            rows={1}
            className="w-full text-base rounded-2xl focus:outline-none resize-none p-9 "
            onKeyDown={handleKeyDown}
          />
          <InputGroupButton
            onClick={handleSubmit}
            disabled={!query.trim()}
            className="absolute right-2 bottom-2 w-10 h-10 rounded-full flex items-center justify-center border-2 disabled:opacity-30 disabled:cursor-not-allowed hover:cursor-pointer bg-amber-400 hover:bg-amber-700  dark:hover:bg-amber-700"
          >
            <ArrowUp className="w-5 h-5 text-secondary" />
            <span className="sr-only">Send</span>
          </InputGroupButton>
        </InputGroup>
        {allQueries.map((query) => (
          <p>{query}</p>
        ))}
      </main>
    </div>
  );
}
