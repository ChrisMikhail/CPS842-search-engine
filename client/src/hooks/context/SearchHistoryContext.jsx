import { createContext, useContext, useState } from 'react';

const SearchHistoryContext = createContext();

export function SearchHistoryProvider({ children }) {
  const [allQueries, setAllQueries] = useState([]);
  return (
    <SearchHistoryContext.Provider value={{ allQueries, setAllQueries }}>
      {children}
    </SearchHistoryContext.Provider>
  );
}
export function useSearchHistory() {
  return useContext(SearchHistoryContext);
}
