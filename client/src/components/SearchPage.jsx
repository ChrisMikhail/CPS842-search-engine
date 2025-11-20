import { useSearch } from '@/hooks/context/SearchContext';
import { Separator } from './ui/separator';
import LinkHeader from './LinkHeader';
import SearchBar from './SearchBar';

export default function SearchPage() {
  const { results } = useSearch();
  return (
    <main className="w-full h-full p-5">
      <SearchBar className="max-w-full" />
      <Separator className="my-5" />
      <div className=" w-full h-full">
        {results.map((result, index) => (
          <div className="mb-5" key={index}>
            <LinkHeader
              link={result.link}
              linkIcon={result.link_icon}
              title={result.title}
              siteName={result.site_name}
            />

            <p>{result.snippet}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
