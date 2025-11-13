import React from 'react';
import Logo from './Logo';

export default function AppHeader() {
  return (
    <div className="px-2 py-3 border-b ">
      <Logo className={'rounded-md hover:bg-accent p-2'} />
    </div>
  );
}
