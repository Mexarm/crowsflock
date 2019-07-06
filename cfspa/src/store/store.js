import Vue from 'vue';
import Vuex from 'vuex';

import state from './state';
import getters from './getters';
import mutations from './mutations';
import actions from './actions';

import tag from './modules/tag';

Vue.use(Vuex);

export const store = new Vuex.Store({
	state,
	getters,
	mutations,
	actions,
	modules: {
		tag
	}
});
