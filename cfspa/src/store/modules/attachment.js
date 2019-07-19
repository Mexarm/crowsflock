import { getters, mutations, actions } from "./common";
import { settings } from "../../services";
import Axios from "axios";
const baseUrl = settings.baseUrl;

const listDisplay = [
  // "id",
  "description",
  "original_filename",
  "size",
  "rename"
  // "created_by",
  // "created_on",
  // "modified_by",
  // "modified_on"
];
const api = "api/attachment/";

const state = {
  item: null,
  items: [],
  apiOptions: {},
  // headers: [],
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
    },
    getFileUrl({ getters }, payload) {
      return Axios.get(baseUrl + getters.api + payload + "/file/").then(
        resp => resp.data
      );
    },
    uploadFile({ commit, getters }, payload) {
      let files = payload.fileInputRef.files;
      let id = payload.id;

      let formData = new FormData();
      if (files && files.length > 0) {
        const file = files[0];
        formData.append("file", file);
      }

      let config = {
        onUploadProgress: function(progressEvent) {
          commit(
            "setProgress",
            Math.round((progressEvent.loaded * 100) / progressEvent.total),
            { root: true }
          );
        }
      };

      let uploadUrl = baseUrl + getters.api + id + "/file/";
      commit("setLoading", true, { root: true });
      commit("setProgress", 0, { root: true });
      return Axios.put(uploadUrl, formData, config).then(resp => {
        commit("setLoading", false, { root: true });
        commit("setProgress", 0, { root: true });
        return resp.data;
      });
      //   const files = this.fileInputRef.files;
      //   let formData = new FormData();
      //   if (files && files.length > 0) {
      //     const file = files[0];
      //     formData.append("file", file);
      //   }
      //   const vue = this;
      //   let config = {
      //     onUploadProgress: function(progressEvent) {
      //       vue.progress = Math.round(
      //         (progressEvent.loaded * 100) / progressEvent.total
      //       );
      //     }
      //   };

      //   let attachmentObj = null;
      //   this.$store.commit("setLoading", true);
      //   axios
      //     .post("http://127.0.0.1:8000/api/attachment/", this.editedItem)
      //     .then(resp => resp.data)
      //     .then(data => {
      //       attachmentObj = data;
      //       let uploadUrl =
      //         "http://127.0.0.1:8000/api/attachment/" + data.id + "/file/";
      //       return axios.put(uploadUrl, formData, config);
      //     })
      //     .then(resp => resp.data)
      //     .then(data => {
      //       this.$store.commit("setLoading", false);
      //       this.$nextTick(() => {
      //         this.$v.$reset();
      //         this.editedItem = { description: "", rename: "" };
      //         this.progress = 0;
      //       });
      //       this.$emit("upload-completed", { obj: attachmentObj, file: data });
      //       this.close();
      //     })
      //     .catch(err => {
      //       this.$store.commit("setLoading", false);
      //       this.close();
      //       this.$emit("error", { message: err.response.data, type: "error" });
      //     });
      // }
    }
  }
};
