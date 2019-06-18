import Vue from "vue";
import "./plugins/vuetify";
import App from "./App.vue";

import axios from "axios";
import router from "./router";
import { store } from "./store/store";

import AppAlert from "./components/core/AppAlert";

import { getAccessToken, refreshAccessToken } from "./store/utils/utils";

Vue.component("app-alert", AppAlert);
Vue.config.productionTip = false;

//axios interceptors

axios.interceptors.request.use(config => {
  //console.log('request interceptor:', config)
  const token = getAccessToken();
  if (token !== null) {
    config.headers.Authorization = "Bearer " + token;
  }
  return config;
});

axios.interceptors.response.use(undefined, function(err) {
  if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
    return refreshAccessToken()
      .then(function(token) {
        // setTokens(success.access_token, success.refresh_token);
        err.config.__isRetryRequest = true;
        err.config.headers.Authorization = "Bearer " + token;
        return axios(err.config);
      })
      .catch(function(error) {
        // console.log("Refresh login error: ", error);
        throw error;
      });
  }
  throw err;
});

new Vue({
  render: h => h(App),
  store,
  router
}).$mount("#app");
