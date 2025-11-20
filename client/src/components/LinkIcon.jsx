import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';

export default function LinkIcon({ linkIcon, title }) {
  return (
    <Avatar className="w-8 h-8">
      <AvatarImage src={linkIcon} alt={title} />
      <AvatarFallback />
    </Avatar>
  );
}
