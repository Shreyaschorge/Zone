const USER_INFO = 'user_info';

const getLocalRefreshToken = () => {
  const _user = localStorage.getItem(USER_INFO);
  if (_user) {
    return JSON.parse(_user)?.refresh_token;
  }
};

const getLocalAccessToken = () => {
  const _user = localStorage.getItem(USER_INFO);
  if (_user) {
    return JSON.parse(_user)?.access_token;
  }
};

const updateLocalAccessToken = (token) => {
  const _user = localStorage.getItem(USER_INFO);
  if (_user) {
    let user = JSON.parse(_user);
    user.access_token = token;
    localStorage.setItem(USER_INFO, JSON.stringify(user));
  }
};

const getUser = () => {
  const _user = localStorage.getItem(USER_INFO);
  if (_user) {
    return JSON.parse(_user);
  }
};

const setUser = (user) => {
  localStorage.setItem(USER_INFO, JSON.stringify(user));
};

const removeUser = () => {
  localStorage.removeItem(USER_INFO);
};

const Token = {
  getLocalRefreshToken,
  getLocalAccessToken,
  updateLocalAccessToken,
  getUser,
  setUser,
  removeUser,
};

export default Token;
