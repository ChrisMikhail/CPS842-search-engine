import { cn } from '@/lib/utils';
import logo from '../../public/minecraft-logo-svg-vector.svg';

export default function Logo({ className }) {
  return <img src={logo} alt="Logo" className={cn(className)} />;
}
