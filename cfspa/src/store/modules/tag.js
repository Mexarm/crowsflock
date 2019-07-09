import { getters, mutations, actions } from "./common";

const listDisplay = [
  "id",
  "name",
  "slug",
  "created_by",
  "created_on",
  "modified_by",
  "modified_on"
];

const api = "api/tag/";

const state = {
  items: [],
  headers: [],
  totalItems: 0,
  listDisplay: listDisplay,
  api: api
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
