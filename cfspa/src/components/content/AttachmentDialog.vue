
 <template>
  <v-dialog
    v-model="dialog"
    max-width="500px"
    @keydown.esc="cancel"
    @keydown.enter="uploadFiles"
  >
    <template v-slot:activator="{ on }">
      <!-- <v-btn color="primary" dark class="mb-2" v-on="on">New Attachment</v-btn> -->
      <v-btn class="ml-4 mt-3" dark small flat color="primary" v-on="on">
        <v-icon dark>add</v-icon>
        new
      </v-btn>
      <!-- <v-btn flat color="primary" class="ma-0 pa-0" v-on="on">New</v-btn> -->
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">{{ formTitle }}</span>
      </v-card-title>

      <v-card-text>
        <v-container grid-list-md>
          <v-layout wrap>
            <v-flex xs12 sm6 md4>
              <v-text-field
                :error-messages="descriptionErrors"
                count="256"
                required
                label="description"
                @input="
                  $v.editedItem.description.$touch();
                  updateDescription($event);
                "
                :value="editedItem.description"
                @blur="$v.editedItem.description.$touch()"
              ></v-text-field>
              <v-text-field
                v-model="editedItem.rename"
                :error-messages="renameErrors"
                count="256"
                label="rename file to"
                @input="$v.editedItem.rename.$touch()"
                @blur="$v.editedItem.rename.$touch()"
              ></v-text-field>
            </v-flex>
          </v-layout>
        </v-container>
        <span v-if="!loading">
          <app-file-upload
            @changed="fileUploadChanged"
            :allowed="allowed"
          ></app-file-upload>
        </span>
        <div v-if="loading && progress < 100">
          cargando archivo(s)...{{ progress }}
          <v-progress-linear v-model="progress"></v-progress-linear>
        </div>
        <div v-if="loading && progress == 100">
          finalizando la carga ...
          <v-progress-circular
            indeterminate
            color="primary"
          ></v-progress-circular>
        </div>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn :disabled="loading" color="blue darken-1" flat @click="close"
          >Cancel</v-btn
        >
        <v-btn
          color="blue darken-1"
          flat
          @click="uploadFiles"
          :disabled="$v.$invalid || !isValidUpload || loading"
          >upload</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

 <script>
import { required, minLength, maxLength } from "vuelidate/lib/validators";
import AppFileUpload from "./FileUpload";
import { mapGetters } from "vuex";
import axios from "axios";
import _ from "lodash";

export default {
  props: {
    allowed: Array //[".csv", ".txt"]
  },
  data() {
    return {
      editedItem: {
        description: "",
        rename: ""
      },
      dialog: false,
      progress: 0,
      // state: "",
      filesList: [],
      fileInputRef: null,
      callingApi: false
    };
  },
  validations: {
    editedItem: {
      description: {
        required,
        minLength: minLength(3),
        maxLength: maxLength(256),
        isUnique(value) {
          // standalone validator ideally should not assume a field is required
          if (value === "") return true;
          // api async call,
          return new Promise((resolve, reject) => {
            // setTimeout(() => {
            //   resolve(typeof value === 'string' && value.length % 2 !== 0)
            // }, 350 + Math.random() * 300)
            this.callingApi = true;
            axios
              .get("http://127.0.0.1:8000/api/attachment/", {
                params: {
                  description: value
                }
              })
              .then(resp => resp.data)
              // .then(data => {
              //   //eslint-disable-next-line
              //   console.log("data:", data, data.count === 0);
              //   return data;
              // })
              .then(data => {
                this.callingApi = false;
                return resolve(data.count == 0);
              })
              .catch(err => reject(err));
          });
        }
      },
      rename: {
        maxLength: maxLength(256)
      }
    }
  },
  computed: {
    ...mapGetters({
      loading: "loading"
    }),
    isValidUpload() {
      return (
        this.filesList.every(file => file.allowed) && this.filesList.length > 0
      );
    },
    formTitle() {
      return this.editedIndex === -1 ? "New Item" : "Edit Item";
    },
    descriptionErrors() {
      const errors = [];
      if (!this.$v.editedItem.description.$dirty) return errors;
      !this.$v.editedItem.description.minLength &&
        errors.push("description must be more than 3 characters long");
      !this.$v.editedItem.description.maxLength &&
        errors.push("description must be less than 256 characters long");
      !this.$v.editedItem.description.required &&
        errors.push("Name is required.");
      !this.$v.editedItem.description.isUnique &&
        errors.push("description already exists");
      return errors;
    },
    renameErrors() {
      const errors = [];
      if (!this.$v.editedItem.rename.$dirty) return errors;
      !this.$v.editedItem.description.maxLength &&
        errors.push("description must be less than 256 characters long");
      return errors;
    }
  },
  methods: {
    // save() {
    //   this.$emit("savedObject", { name: this.editedItem.name });
    //   this.editedItem = {};
    //   this.close();
    // },
    updateDescription: _.debounce(function(value) {
      this.editedItem.description = value;
    }, 500),
    close() {
      this.dialog = false;
    },
    fileUploadChanged(obj) {
      this.filesList = obj.filesList;
      this.fileInputRef = obj.fileInputRef;
    },
    uploadFiles() {
      const files = this.fileInputRef.files;
      let formData = new FormData();
      if (files && files.length > 0) {
        const file = files[0];
        formData.append("file", file);
      }
      const vue = this;
      let config = {
        onUploadProgress: function(progressEvent) {
          vue.progress = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
        }
      };

      let attachmentObj = null;
      this.$store.commit("setLoading", true);
      axios
        .post("http://127.0.0.1:8000/api/attachment/", this.editedItem)
        .then(resp => resp.data)
        .then(data => {
          attachmentObj = data;
          let uploadUrl =
            "http://127.0.0.1:8000/api/attachment/" + data.id + "/file/";
          return axios.put(uploadUrl, formData, config);
        })
        .then(resp => resp.data)
        .then(data => {
          this.$store.commit("setLoading", false);

          this.$nextTick(() => {
            this.$v.$reset();
            this.editedItem = { description: "", rename: "" };
            this.progress = 0;
          });
          this.$emit("upload-completed", { obj: attachmentObj, file: data });
          this.close();
        })
        .catch(err => {
          this.$store.commit("setLoading", false);
          this.close();
          this.$emit("error", { message: err.response.data, type: "error" });
        });
    }
  },
  components: {
    AppFileUpload
  }
};
</script>
