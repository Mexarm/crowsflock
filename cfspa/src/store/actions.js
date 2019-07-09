import {
  authenticate,
  setTokens,
  getUser,
  settings,
  removeTokens,
  getAccessToken
} from "../services";
// import {
//   getUser,
//   getAccessToken,
//   removeTokens,
//   setTokens
// } from "./utils/utils";
import router from "../router";

export default {
  updateSideNav({ commit }, payload) {
    commit("setSideNav", payload);
  },
  signInUser({ commit, dispatch }, payload) {
    commit("setAlert", null);
    commit("setLoading", true);

    authenticate(payload)
      .then(resp => {
        commit("setLoading", false);
        setTokens(resp.access, resp.refresh);
        commit("setUser", getUser(resp.access));
      })
      .catch(err => {
        err = err.response;
        // eslint-disable-next-line
        console.log(err);
        commit("setLoading", false);
        //console.log('error:', err)
        //let message = err.detail;
        let message = "Error autenticandose";
        if (err.status === 401) {
          message = err.data.detail;
          //message = "No Autorizado verifique credenciales";
        }
        if (err.status === 0) {
          message = "Error de conexion";
        }
        dispatch("setAlertTimeout", { message, type: "error" });
      });
  },
  tryAutoLogin({ commit }) {
    let token = localStorage.getItem(settings.ACCESS_TOKEN_KEY);
    let refresh = localStorage.getItem(settings.REFRESH_TOKEN_KEY);
    // @TODO: verify if refresh is not expired
    if (token && refresh) {
      commit("setUser", getUser(token));
    }
  },
  signOutUser({ commit }) {
    removeTokens();
    commit("setUser", null);
    router.replace("/signin");
  },

  checkAuth({ commit }) {
    var token = getAccessToken();
    if (token) {
      commit("setUser", getUser(token));
    } else {
      commit("setUser", null);
    }
  },
  setAlertTimeout({ commit, dispatch }, payload) {
    commit("setAlert", payload);
    setTimeout(() => {
      dispatch("clearAlert");
    }, 3000);
  },
  clearAlert({ commit }) {
    commit("setAlert", null);
  }
};
