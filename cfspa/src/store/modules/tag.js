import auth from "../../services/auth";
import axios from "axios";

const baseUrl = auth.settings.baseUrl + "api/tag/";

export default {
  namespaced: true,
  state: {
    items: [],
    headers: [],
    totalItems: 0
  },
  getters: {
    items(state) {
      return state.items;
    },
    headers(state) {
      return state.headers;
    },
    totalItems(state) {
      return state.totalItems;
    },
    listDisplay() {
      return [
        "id",
        "name",
        "slug",
        "created_by",
        "created_on",
        "modified_by",
        "modified_on"
      ];
    }
  },
  mutations: {
    setItems(state, payload) {
      state.items = payload;
    },
    setHeaders(state, payload) {
      state.headers = payload;
    },
    setTotalItems(state, payload) {
      state.totalItems = payload;
    }
  },
  actions: {
    getItems({ commit }, { pagination, searchTxt }) {
      const page =
        typeof pagination === "object" &&
        typeof pagination.page === "number" &&
        pagination.page > 1
          ? pagination.page
          : false;
      const ordering =
        typeof pagination === "object" &&
        typeof pagination.sortBy === "string" &&
        pagination.sortBy.length > 0
          ? pagination.sortBy
          : false;
      const descending =
        typeof pagination === "object" &&
        typeof pagination.descending === "boolean" &&
        pagination.descending
          ? "-"
          : "";

      const rowsPerPage =
        typeof pagination === "object" &&
        typeof pagination.rowsPerPage === "number" &&
        pagination.rowsPerPage > 0
          ? pagination.rowsPerPage
          : false;

      const search =
        typeof searchTxt === "string" && searchTxt.length > 0
          ? searchTxt
          : false;

      const params = {};

      if (page) {
        params.page = page;
      }

      if (ordering) {
        params.ordering = descending + ordering;
      }

      if (search) {
        params.search = search;
      }
      if (rowsPerPage) {
        params.page_size = rowsPerPage;
      }

      commit("setLoading", true, { root: true });
      axios
        .get(baseUrl, { params })
        .then(resp => resp.data)
        .then(data => {
          commit("setLoading", false, { root: true });
          commit("setItems", data.results);
          commit("setTotalItems", data.count);
        });
      // .catch(error => {
      // 	commit('setLoading', false);
      // 	commit('setAlert', {
      // 		message: error.message,
      // 		type: 'error'
      // 	});
      // });
    },
    getHeaders({ commit, getters }) {
      commit("setLoading", true, { root: true });
      axios
        .options(baseUrl)
        .then(resp => resp.data)
        .then(data => data.actions)
        .then(actions => actions.POST)
        .then(fields => {
          commit("setLoading", true, { root: true });
          let headers = [];
          //   const fields_list = Object.keys(fields);
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
    save({ commit }, payload) {
      return axios
        .post(baseUrl, payload)
        .then(response => {
          if (response.status === 201) {
            commit(
              "setAlert",
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
          commit(
            "setAlert",
            {
              message: error,
              type: "error"
            },
            { root: true }
          );
        });
    }
  }
};
