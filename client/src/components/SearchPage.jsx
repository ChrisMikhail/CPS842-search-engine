import { useSearch } from '@/hooks/context/SearchContext';
import { Separator } from './ui/separator';
import { Link } from 'react-router';
import SearchBar from './SearchBar';

export default function SearchPage() {
  const { results } = useSearch();
  return (
    <main className="w-full h-full p-5">
      {/* <SearchBar className="h-1/2" /> */}
      <h1 className="font-bold text-2xl">Results</h1>
      <Separator className="mt-5" />
      <div className=" w-full h-full">
        {results.map((result, index) => (
          <div className="" key={index}>
            <a
              href={result.link}
              target="_blank"
              className="text-lg font-semibold hover:underline text-blue-800"
            >
              {result.title}
            </a>
            <p>{result.snippet}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
