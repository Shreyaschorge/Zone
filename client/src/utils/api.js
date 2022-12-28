import axios from 'axios';
import Token from './manageToken';

const BASE_URL = '/api';

const Axios = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

Axios.interceptors.request.use(
  (config) => {
    const token = Token.getLocalAccessToken();
    if (token) {
      if (config.headers) {
        config.headers.Authorization = 'Bearer ' + token;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

Axios.interceptors.response.use(
  (res) => res,
  async (err) => {
    const originalConfig = err.config;

    if (originalConfig.url !== '/users/login' && err.response) {
      if (
        err.response.status === 401 &&
        err.response.data.status_code === 4001
      ) {
        Token.removeUser();
        window.location.reload();
      } else if (
        err.response.status === 401 &&
        err.config &&
        !err.config.__isRetryRequest
      ) {
        originalConfig._retry = true;

        try {
          // send refresh_token to fetch new access_token.
          const res = await axios.post(
            BASE_URL + '/users/refresh',
            {},
            {
              headers: {
                Authorization: `Bearer ${Token.getLocalRefreshToken()}`,
              },
            }
          );

          // check if we get the access_token, if yes, that means refresh_token is not expired.
          // fetch access_token and update it in local_storage.
          if (res.data.data && res.data.data.access_token) {
            Token.updateLocalAccessToken(res.data.data.access_token);
          } else {
            // if refresh_token expires log user out of the application.
            Token.removeUser();
          }

          return Axios(originalConfig);
        } catch (_error) {
          return Promise.reject(_error);
        }
      }
    }

    return Promise.reject(err);
  }
);

export default Axios;
