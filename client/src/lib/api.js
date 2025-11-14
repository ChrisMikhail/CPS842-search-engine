import axios from 'axios';
const API_URL = 'http://127.0.0.1:8000';

// Configure axios defaults
axios.defaults.headers.post['Content-Type'] = 'application/json';
axios.defaults.headers.put['Content-Type'] = 'application/json';

export const searchQuery = async (query) => {
  const { data, status } = await axios.get(`${API_URL}/search?q=${query}`);

  return { status, data };
};
