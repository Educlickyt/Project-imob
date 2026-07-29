import axios from 'axios';

const publicApi = axios.create({
  baseURL: 'http://localhost:8000/v1'
});

export default publicApi;
