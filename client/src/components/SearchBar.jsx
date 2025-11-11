import { Search } from 'lucide-react';

import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from '@/components/ui/input-group';

export default function SearchBar() {
  return (
    <div className="w-full">
      <InputGroup>
        <InputGroupInput
          placeholder="Ask anything crafting"
          className="border-0 focus-visible:border-0"
        />
        <InputGroupAddon>
          <Search />
        </InputGroupAddon>
        <InputGroupAddon align="inline-end">
          <InputGroupButton></InputGroupButton>
        </InputGroupAddon>
      </InputGroup>
    </div>
  );
}
