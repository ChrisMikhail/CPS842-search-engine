import { cn } from '@/lib/utils';
import logo from '../../public/minecraft-logo-svg-vector.svg';
import { NavLink } from 'react-router';

export default function Logo({ className }) {
  return (
    <NavLink to={'/search'} className={cn(className)}>
      MineFox
    </NavLink>
  );
}
