import authService from "../services/auth";
// import {
//   getUser,
//   getAccessToken,
//   removeTokens,
//   setTokens
// } from "./utils/utils";

export default {
  updateSideNav({ commit }, payload) {
    commit("setSideNav", payload);
  },
  signInUser({ commit }, payload) {
    commit("setAlert", null);
    commit("setLoading", true);
    authService.authenticate(payload).then(resp => {
      commit("setLoading", false);
      authService.setTokens(resp.access, resp.refresh);
      commit("setUser", authService.getUser(resp.access));
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
      commit("setAlert", { message, type: 'error' });
    });
  },
  signOutUser({ commit }) {
    authService.removeTokens();
    commit("setUser", null);
  },

  checkAuth({ commit }) {
    var token = authService.getAccessToken();
    if (token) {
      commit("setUser", authService.getUser(token));
    } else {
      commit("setUser", null);
    }
  },

  clearAlert({ commit }) {
    commit("setAlert", null);
  }
};
