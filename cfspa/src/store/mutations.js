export default {
  setUser(state, payload) {
    state.user = payload;
  },
  setLoading(state, payload) {
    state.loading = payload;
  },
  setProgress(state, payload) {
    state.progress = payload;
  },
  setAlert(state, payload) {
    state.alert = payload;
  },
  setSideNav(state, payload) {
    state.sideNav = payload;
  }
};
