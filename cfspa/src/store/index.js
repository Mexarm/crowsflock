import Vue from "vue";
import Vuex from "vuex";

import state from "./state";
import getters from "./getters";
import mutations from "./mutations";
import actions from "./actions";

import tag from "./modules/tag";
import attachment from "./modules/attachment";

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== "production";

export const store = new Vuex.Store({
  state,
  getters,
  mutations,
  actions,
  modules: {
    tag,
    attachment
  },
  strict: debug
});
