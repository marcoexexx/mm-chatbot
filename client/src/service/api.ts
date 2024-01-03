import axios from 'axios';


const api1 = axios.create({
  baseURL: 'http://localhost:8000/api/v1/',
});

const api2 = axios.create({
  baseURL: 'http://localhost:8000/api/v1/',
});


const apis = [api1, api2];

let currentApiIndex = 0;

const switchApi = () => {
  currentApiIndex = (currentApiIndex + 1) % apis.length;
  return apis[currentApiIndex];
}

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    // If request fails, switch to the next API
    const isApiError = error.config && error.config.baseURL.includes('api');
    if (isApiError) {
      const newApi = switchApi();
      error.config.baseURL = newApi.defaults.baseURL;
      return axios.request(error.config);
    }
    return Promise.reject(error);
  }
)


export async function sendFn(payload: {txt: string, lang: "en" | "my"}) {
  const api = switchApi()
  const { data } = await api.post("/chatbot", {
    user_input: payload.txt,
    lang: payload.lang
  })

  return data.bot as string
}

