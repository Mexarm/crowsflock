import auth from '../../services/auth';
import axios from 'axios';

const baseUrl = auth.settings.baseUrl + 'api/tag/';

export default {
	state: {
		tags: {},
		headers : [],
		totalTags: 0,
		fields: {}
	},
	getters: {
		tags(state) {
			return state.tags;
		},
		fields(state) {
			return state.fields;
		}
	},
	mutations: {
		setTags(state, payload) {
			state.tags = payload;
		},
		setFields(state, payload) {
			state.fields = payload;
		}
	},
	actions: {
		getfromApi({ commit }, { pagination, searchTxt }) {
			const page =
				typeof pagination === 'object' &&
				typeof pagination.page === 'number' &&
				pagination.page > 1
					? pagination.page
					: false;
			const ordering =
				typeof pagination === 'object' &&
				typeof pagination.sortBy === 'string' &&
				pagination.sortBy.length > 0
					? pagination.sortBy
					: false;
			const descending =
				typeof pagination === 'object' &&
				typeof pagination.descending === 'boolean' &&
				pagination.descending
					? '-'
					: '';

			const rowsPerPage =
				typeof pagination === 'object' &&
				typeof pagination.rowsPerPage === 'number' &&
				pagination.rowsPerPage > 0
					? pagination.rowsPerPage
					: false;

			const search =
				typeof searchTxt === 'string' && searchTxt.length > 0
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

			commit('setLoading', true, { root: true});
			return axios.get(baseUrl, { params }).then(resp => {
				commit('setLoading', false, { root: true});
				commit('setTags', resp.data);
			})
			.catch(error => {
				commit('setLoading', false);
				commit('setAlert', { message: error.message, type: 'error'});
			})
		}
	}
};
