import { getters, mutations, actions } from "./common";

const listDisplay = [
  "id",
  "description",
  "original_filename",
  "size",
  "rename",
  "created_by",
  "created_on",
  "modified_by",
  "modified_on"
];
const api = "api/attachment/";

const state = {
  items: [],
  headers: [],
  totalItems: 0,
  listDisplay: listDisplay,
  api: api,
  isValidUpload: false
};

export default {
  namespaced: true,
  state,
  getters: {
    ...getters,
    isValidUpload(state) {
      return state.isValidUpload;
    }
  },
  mutations: {
    ...mutations,
    setIsValidUpload(state, payload) {
      state.isValidUpload = payload;
    }
  },
  actions: {
    ...actions,
    setIsValidUpload({ commit }, payload) {
      commit("setIsValidUpload", payload);
    }
  }
};
