// import Vue from 'vue'
import axios from "axios";

const settings = {};

settings.ACCESS_TOKEN_KEY = "token";
settings.REFRESH_TOKEN_KEY = "refresh";
settings.baseUrl = "http://127.0.0.1:8000/";
function authenticate(request) {
  return (
    axios
      .post("http://localhost:8000/api/token/", request)
      // return Vue.http.post('https://crossorigin.me/http://postb.in/VWOhALuu', request)
      .then(response => Promise.resolve(response.data))
      .catch(error => Promise.reject(error))
  );
}

function parseJwt(token) {
  var base64Url = token.split(".")[1];
  var base64 = base64Url.replace("-", "+").replace("_", "/");
  return JSON.parse(window.atob(base64));
}

function getUser(access) {
  let parsedToken = parseJwt(access);

  const user = {
    user_id: parsedToken.user_id
  };
  return user;
}

function getAccessToken() {
  return localStorage.getItem(settings.ACCESS_TOKEN_KEY);
}
function removeTokens() {
  localStorage.removeItem(settings.ACCESS_TOKEN_KEY);
  localStorage.removeItem(settings.REFRESH_TOKEN_KEY);
}

function setAccessToken(access) {
  localStorage.setItem(settings.ACCESS_TOKEN_KEY, access);
}
function setTokens(access, refresh) {
  setAccessToken(access);
  localStorage.setItem(settings.REFRESH_TOKEN_KEY, refresh);
}

export default {
  authenticate,
  getAccessToken,
  removeTokens,
  getUser,
  setTokens,
  settings
};
