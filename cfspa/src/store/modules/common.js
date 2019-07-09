import axios from "axios";
import { getParams } from "../../utils";
import { settings } from "../../services";

const baseUrl = settings.baseUrl;

const getters = {
  items(state) {
    return state.items;
  },
  headers(state) {
    return state.headers;
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
  setItems(state, payload) {
    state.items = payload;
  },
  setHeaders(state, payload) {
    state.headers = payload;
  },
  setTotalItems(state, payload) {
    state.totalItems = payload;
  }
};

const actions = {
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
  getHeaders({ commit, getters }) {
    commit("setLoading", true, { root: true });
    axios
      .options(baseUrl + getters.api)
      .then(resp => resp.data)
      .then(data => data.actions)
      .then(actions => actions.POST)
      .then(fields => {
        commit("setLoading", true, { root: true });
        let headers = [];
        for (const field of getters.listDisplay) {
          headers.push({
            text: fields[field].label,
            value: field
          });
        }
        return headers;
      })
      .then(headers => {
        commit("setHeaders", headers);
      });
  },
  save({ getters, dispatch }, payload) {
    return axios
      .post(baseUrl + getters.api, payload)
      .then(response => {
        if (response.status === 201) {
          dispatch(
            "setAlertTimeout",
            {
              message: response.data.name + ", " + response.statusText,
              type: "success"
            },
            { root: true }
          );
          return response;
        }
      })
      .catch(error => {
        dispatch(
          "setAlertTimeout",
          { message: error, type: "error" },
          { root: true }
        );
      });
  }
};

export { getters, mutations, actions };
