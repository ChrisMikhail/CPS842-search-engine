import { cn } from '@/lib/utils';
import { NavLink } from 'react-router-dom';

export default function Logo({ className }) {
  return (
    <NavLink to={'/search'} className={cn(className)}>
      Stronghold
    </NavLink>
  );
}
