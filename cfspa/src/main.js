import Vue from "vue";
import "./plugins/vuetify";
import App from "./App.vue";

import moment from "moment";
import filesize from "filesize";
import Vuelidate from "vuelidate";
import axios from "axios";

import createAuthRefreshInterceptor from "axios-auth-refresh";

import { getAccessToken, settings } from "./services";
import router from "./router";
import { store } from "./store";

import AppAlert from "./components/core/AppAlert";

//axios interceptors
// Function that will be called to refresh authorization
const refreshAuthLogic = failedRequest =>
  axios
    .post(settings.baseUrl + settings.tokenApiRefresh, {
      refresh: localStorage.getItem("refresh")
    })
    .then(tokenRefreshResponse => {
      localStorage.setItem(
        settings.ACCESS_TOKEN_KEY,
        tokenRefreshResponse.data.access
      );
      failedRequest.response.config.headers["Authorization"] =
        "Bearer " + tokenRefreshResponse.data.access;
      return Promise.resolve();
    });

// Instantiate the interceptor (you can chain it as it returns the axios instance)
createAuthRefreshInterceptor(axios, refreshAuthLogic);

axios.interceptors.request.use(request => {
  request.headers["Authorization"] = "Bearer " + getAccessToken();
  return request;
});

Vue.component("app-alert", AppAlert);
Vue.config.productionTip = false;

Vue.filter("formatDate", function(value) {
  if (value) {
    return moment(String(value)).format("MM/DD/YYYY hh:mm");
  }
});
Vue.filter("formatFileSize", function(value) {
  if (value) {
    return filesize(value);
  }
});

Vue.use(Vuelidate);

new Vue({
  render: h => h(App),
  store,
  router,
  created() {
    this.$store.dispatch("tryAutoLogin");
  }
}).$mount("#app");
