import authService from "../../services/auth";

const settings = {};

settings.ACCESS_TOKEN_KEY = "token";
settings.REFRESH_TOKEN_KEY = "refresh";

function parseJwt(token) {
  var base64Url = token.split(".")[1];
  var base64 = base64Url.replace("-", "+").replace("_", "/");
  return JSON.parse(window.atob(base64));
}

function getUser(access) {
  let parsedToken = parseJwt(access);

  const user = {
    // first_name: parsedToken.user.first_name,
    // last_name: parsedToken.user.last_name,
    // email: parsedToken.user.email,
    user_id: parsedToken.user_id
    // groups: parsedToken.user_groups
  };
  return user;
}

function expiredJwt(token) {
  let parsedToken = parseJwt(token);
  let now = new Date();
  return parsedToken.exp * 1000 <= now.getTime();
}

function getAccessToken() {
  return localStorage.getItem(settings.ACCESS_TOKEN_KEY);
}

function getRefreshToken() {
  return localStorage.getItem(settings.REFRESH_TOKEN_KEY);
}

function setAccessToken(access) {
  localStorage.setItem(settings.ACCESS_TOKEN_KEY, access);
}
function setTokens(access, refresh) {
  setAccessToken(access);
  localStorage.setItem(settings.REFRESH_TOKEN_KEY, refresh);
}

function removeTokens() {
  localStorage.removeItem(settings.ACCESS_TOKEN_KEY);
  localStorage.removeItem(settings.REFRESH_TOKEN_KEY);
}

function jwtSecondsToExpire(token) {
  let parsed = parseJwt(token);
  let now = new Date();
  return parsed.exp - now.getTime() / 100;
}

function accessTokenExpireSoon() {
  return jwtSecondsToExpire() < 5.0;
}
function refreshTokenExpired() {
  let refresh = getRefreshToken();
  return expiredJwt(refresh);
}

function refreshAccessToken() {
  let refresh = getRefreshToken();
  return authService.refreshToken({ refresh }).then(token => {
    setAccessToken(token);
    return token;
  });
}

export {
  parseJwt,
  getUser,
  expiredJwt,
  getAccessToken,
  getRefreshToken,
  accessTokenExpireSoon,
  refreshAccessToken,
  refreshTokenExpired,
  setTokens,
  removeTokens
};
