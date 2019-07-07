import Vue from "vue";
import "./plugins/vuetify";
import App from "./App.vue";
import moment from "moment";

import axios from "axios";
import createAuthRefreshInterceptor from "axios-auth-refresh";
import auth from "./services/auth";

import router from "./router";
import { store } from "./store/store";

import AppAlert from "./components/core/AppAlert";

import Vuelidate from "vuelidate";

//axios interceptors

// Function that will be called to refresh authorization
const refreshAuthLogic = failedRequest =>
  axios
    .post("http://localhost:8000/api/token/refresh/", {
      refresh: localStorage.getItem("refresh")
    })
    .then(tokenRefreshResponse => {
      localStorage.setItem(
        auth.settings.ACCESS_TOKEN_KEY,
        tokenRefreshResponse.data.access
      );
      failedRequest.response.config.headers["Authorization"] =
        "Bearer " + tokenRefreshResponse.data.access;
      return Promise.resolve();
    });

// Instantiate the interceptor (you can chain it as it returns the axios instance)
createAuthRefreshInterceptor(axios, refreshAuthLogic);

axios.interceptors.request.use(request => {
  request.headers["Authorization"] = "Bearer " + auth.getAccessToken();
  return request;
});

//import { getAccessToken, refreshAccessToken } from "./store/utils/utils";

Vue.component("app-alert", AppAlert);
Vue.config.productionTip = false;

Vue.filter("formatDate", function(value) {
  if (value) {
    return moment(String(value)).format("MM/DD/YYYY hh:mm");
  }
});

Vue.use(Vuelidate);

new Vue({
  render: h => h(App),
  store,
  router
}).$mount("#app");
