import axios from "axios";
import { getParams } from "../../utils";
import { settings } from "../../services";

const baseUrl = settings.baseUrl;

const getters = {
  item(state) {
    return state.item;
  },
  items(state) {
    return state.items;
  },
  apiOptions(state) {
    return state.apiOptions;
  },
  headers(state) {
    let headers = [];
    if (!state.apiOptions) return headers;
    if (!state.apiOptions.hasOwnProperty(state.listDisplay[0])) return headers;
    for (const field of state.listDisplay) {
      let fldObj = state.apiOptions[field];
      headers.push({ text: fldObj.label, value: field });
    }
    return headers;
  },
  totalItems(state) {
    return state.totalItems;
  },
  listDisplay(state) {
    return state.listDisplay;
  },
  api(state) {
    return state.api;
  }
};

const mutations = {
  setItem(state, payload) {
    state.item = payload;
  },
  setItems(state, payload) {
    state.items = payload;
  },
  setApiOptions(state, payload) {
    state.apiOptions = payload;
  },
  setTotalItems(state, payload) {
    state.totalItems = payload;
  }
};

const actions = {
  getItemById({ commit, getters, dispatch }, payload) {
    commit("setLoading", true, { root: true });
    return axios
      .get(baseUrl + getters.api + payload + "/")
      .then(resp => resp.data)
      .then(data => {
        commit("setLoading", false, { root: true });
        commit("setItem", data);
        return data;
      })
      .catch(error => {
        commit("setLoading", false, { root: true });
        dispatch(
          "setAlertTimeout",
          {
            message: error.message,
            type: "error"
          },
          { root: true }
        );
      });
  },
  filterItems({ getters }, payload) {
    return axios
      .get(baseUrl + getters.api, {
        params: payload
      })
      .then(resp => resp.data);
  },
  getItems({ commit, getters, dispatch }, { pagination, searchTxt }) {
    const params = getParams(pagination, searchTxt);
    commit("setLoading", true, { root: true });
    axios
      .get(baseUrl + getters.api, { params })
      .then(resp => resp.data)
      .then(data => {
        commit("setLoading", false, { root: true });
        commit("setItems", data.results);
        commit("setTotalItems", data.count);
      })
      .catch(error => {
        commit("setLoading", false, { root: true });
        dispatch(
          "setAlertTimeout",
          {
            message: error.message,
            type: "error"
          },
          { root: true }
        );
      });
  },
  getApiOptions({ commit, getters }) {
    commit("setLoading", true, { root: true });
    axios
      .options(baseUrl + getters.api)
      .then(resp => resp.data)
      .then(data => data.actions)
      .then(actions => actions.POST)
      .then(fieldsObj => {
        commit("setLoading", false, { root: true });
        commit("setApiOptions", fieldsObj);
      });
  },
  create({ commit, getters, dispatch }, payload) {
    commit("setLoading", true, { root: true });
    return axios
      .post(baseUrl + getters.api, payload)
      .then(response => {
        if (response.status === 201) {
          commit("setLoading", false, { root: true });
          return response.data;
        }
      })
      .catch(error => {
        dispatch(
          "setAlertTimeout",
          { message: error, type: "error" },
          { root: true }
        );
      });
  },
  update() {}
};

export { getters, mutations, actions };
