import { searchQuery } from '@/lib/api';
import { createContext, useContext, useState } from 'react';
import { useNavigate } from 'react-router';

const SearchContext = createContext();

export function SearchProvider({ children }) {
  const navigate = useNavigate();

  const [query, setQuery] = useState('');
  const [allQueries, setAllQueries] = useState([]);
  const [results, setResults] = useState([]);

  const handleSubmit = async () => {
    if (query.trim()) {
      try {
        const { status, data } = await searchQuery(query);
        if (status == 200) {
          setResults(data);
          navigate(`/${query}`);
        }
      } catch (error) {
        console.log(error);
      }
      setAllQueries((prev) => [...prev, query]);
      setQuery('');
    }
  };
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  let queryCount = 0;
  allQueries.forEach((query) => queryCount++);

  return (
    <SearchContext.Provider
      value={{
        query,
        setQuery,
        allQueries,
        setAllQueries,
        queryCount,
        handleSubmit,
        handleKeyDown,
        results,
      }}
    >
      {children}
    </SearchContext.Provider>
  );
}
export function useSearch() {
  return useContext(SearchContext);
}
