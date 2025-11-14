import React, { useState } from 'react';
import { Sparkles, ArrowUp, Hammer } from 'lucide-react';
import {
  InputGroup,
  InputGroupButton,
  InputGroupTextarea,
} from './ui/input-group';
import { ModeToggle } from './ui/mode-toggle';
import Logo from './Logo';
import { useSearch } from '@/hooks/context/SearchContext';
import { NavLink, useNavigate } from 'react-router';
import SearchBar from './SearchBar';

//TODO: add a clear button (X)
export default function HomePage() {
  return (
    <div className=" h-full w-full flex flex-col items-center justify-center ">
      {/* Main Content */}
      <div className="text-center mb-12 flex flex-col gap-3 items-center">
        <Logo className={'text-5xl font-semibold mb-3'} />
      </div>

      {/* Search Input */}
      <SearchBar />
      {/* <InputGroup className="w-full max-w-3xl">
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
          <NavLink to={`/${query}`}>
            <ArrowUp className="w-5 h-5 text-secondary" />
            <span className="sr-only">Send</span>
          </NavLink>
        </InputGroupButton>
      </InputGroup> */}
      {/* </main> */}
    </div>
  );
}
