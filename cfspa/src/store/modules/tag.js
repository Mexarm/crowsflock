import auth from '../../services/auth';
import axios from 'axios';

const baseUrl = auth.settings.baseUrl + 'api/tag/';

export default {
	namespaced: true,
	state: {
		tags: [],
		headers: [],
		totalTags: 0
	},
	getters: {
		tags(state) {
			return state.tags;
		},
		headers(state) {
			return state.headers;
		},
		totalTags(state) {
			return state.totalTags;
		}
	},
	mutations: {
		setTags(state, payload) {
			state.tags = payload;
		},
		setFields(state, payload) {
			state.fields = payload;
		},
		setHeaders(state, payload) {
			state.headers = payload;
		},
		setTotalTags(state, payload) {
			state.totalTags = payload;
		}
	},
	actions: {
		getTags({ commit }, { pagination, searchTxt }) {
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

			commit('setLoading', true, { root: true });
			axios
				.get(baseUrl, { params })
				.then(resp => resp.data)
				.then(data => {
					commit('setLoading', false, { root: true });
					commit('setTags', data.results);
					commit('setTotalTags', data.count);
				});
			// .catch(error => {
			// 	commit('setLoading', false);
			// 	commit('setAlert', {
			// 		message: error.message,
			// 		type: 'error'
			// 	});
			// });
		},
		getHeaders({ commit }) {
			commit('setLoading', true, { root: true });
			axios
				.options(baseUrl)
				.then(resp => resp.data)
				.then(data => data.actions)
				.then(actions => actions.POST)
				.then(fields => {
					commit('setLoading', true, { root: true });
					let headers = [];
					const fields_list = Object.keys(fields);
					for (const field of fields_list) {
						headers.push({
							text: fields[field].label,
							value: field
						});
					}
					return headers;
				})
				.then(headers => {
					commit('setHeaders', headers);
				});
		},
		save({ commit }, payload) {
			return axios
				.post(baseUrl, payload)
				.then(response => {
					if (response.status === 201) {
						commit('setAlert', {
							message:
								response.data.name + ', ' + response.statusText,
							type: 'success'
						},  { root: true });
						return response;
					}
				})
				.catch(error => {
					commit('setAlert', {
						message: error,
						type: 'error'
					}, { root: true });
				});
		}
	}
};
