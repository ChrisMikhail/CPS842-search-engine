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
      <div className="text-center mb-12 flex flex-col gap-3 items-center">
        <Logo className={'text-5xl font-semibold mb-3'} />
      </div>

      <SearchBar />
    </div>
  );
}
