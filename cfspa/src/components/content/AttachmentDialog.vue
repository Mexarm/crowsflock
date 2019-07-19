 <template>
  <v-dialog
    persistent
    :value="value.dialog"
    @input="input($event)"
    max-width="680px"
    @keydown.esc="close"
    @keydown.enter="acceptDialog"
  >
    <template v-slot:activator="{ on }">
      <div class="text-xs-center">
        <v-btn
          v-on="on"
          round
          color="primary"
          class="ml-4 mt-3"
          dark
          small
        >
          <v-icon dark>add</v-icon> new
        </v-btn>
      </div>
    </template>

    <v-card>
      <v-card-title>
        <span class="headline">{{ formTitle }}</span>
      </v-card-title>

      <v-card-text>
        <v-container
          grid-list-md
          fluid
        >
          <v-layout
            row
            wrap
          >
            <v-flex xs12>
              <v-text-field
                box
                :error-messages="descriptionErrors"
                counter="256"
                required
                label="description"
                hint="describe your attachment, so it will be easier to find it later"
                :value="editedItem.description"
                @input="updateDescription($event)"
                @blur="$v.editedItem.description.$touch()"
                :loading="loading || $v.$pending"
              ></v-text-field>
              <v-text-field
                box
                v-model="editedItem.rename"
                :error-messages="renameErrors"
                counter="256"
                label="rename file to"
                hint="your file will be renamed on send"
                @input="$v.editedItem.rename.$touch()"
                @blur="$v.editedItem.rename.$touch()"
                :disabled="loading"
              ></v-text-field>
              <v-text-field
                box
                v-model="editedItem.original_filename"
                label="File"
                hint="uploaded file"
                :readonly="true"
              >
                <template v-slot:append>

                  <v-btn
                    flat
                    icon
                    class="pa-0 ma-0"
                    color="green"
                    @click="onDownload"
                    v-if="editedItem.original_filename"
                  >
                    <v-icon>cloud_download</v-icon>
                  </v-btn>
                  <v-btn
                    flat
                    icon
                    class="pa-0 ma-0"
                    color="red"
                    @click="onDownload"
                    v-if="editedItem.original_filename"
                  >
                    <v-icon>delete_forever</v-icon>
                  </v-btn>
                </template>

              </v-text-field>
            </v-flex>
          </v-layout>
        </v-container>

        <!-- ====== file Selector ======= -->
        <v-container
          grid-list-md
          fluid
        >
          <v-layout
            row
            wrap
          >
            <v-flex xs12>
              <div v-if="showFileSelector">
                <span v-if="!loading">
                  <app-file-selector
                    @changed="onfileSelectorChanged"
                    :allowed="allowed"
                  ></app-file-selector>
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
              </div>
            </v-flex>
          </v-layout>
        </v-container>
        <!-- ===================== -->
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          :disabled="loading"
          color="blue darken-1"
          flat
          @click="close"
        >Cancel</v-btn>
        <v-btn
          color="blue darken-1"
          flat
          @click="acceptDialog"
          :disabled="$v.$invalid || !fileSelectorValid || loading"
        >{{ isNew ? "upload" : "update" }}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { required, minLength, maxLength } from "vuelidate/lib/validators";
import AppFileSelector from "./FileSelector";
import { mapGetters } from "vuex";
import { triggerFileDownload } from "../../utils";

import _ from "lodash";

export default {
  props: {
    allowed: Array, //["csv", "txt"]
    value: Object
  },
  data() {
    return {
      editedItem: {
        id: null,
        description: "",
        original_filename: "",
        rename: "",
        url: null
      },
      filesList: [],
      fileInputRef: null
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
            this.$store
              .dispatch("attachment/filterItems", { description: value })
              .then(data => resolve(data.count == 0))
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
      loading: "loading",
      progress: "progress",
      item: "attachment/item",
      api: "attachment/api"
    }),
    fileSelectorValid() {
      return (
        this.filesList.every(file => file.allowed) && this.filesList.length > 0
      );
    },
    showFileSelector() {
      return this.isNew || !this.editedItem.original_filename;
    },
    isNew() {
      return this.value.itemId == null;
    },
    formTitle() {
      return this.isNew ? "New" : "Edit";
    },
    descriptionErrors() {
      const errors = [];
      if (!this.$v.editedItem.description.$dirty) return errors;
      !this.$v.editedItem.description.minLength &&
        errors.push("description must be more than 3 characters long");
      !this.$v.editedItem.description.maxLength &&
        errors.push("description must be less than 256 characters long");
      !this.$v.editedItem.description.required &&
        errors.push("description is required.");
      let keyNeedsValidation =
        this.isNew || !(this.item.description === this.editedItem.description);
      keyNeedsValidation &&
        !this.$v.editedItem.description.$pending &&
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
    resetEditedItem() {
      this.editedItem.id = null;
      this.editedItem.description = "";
      this.editedItem.original_filename = "";
      this.editedItem.rename = "";
      this.editedItem.url = null;
    },
    input(value) {
      let newVal = {
        dialog: value,
        itemId: this.value.itemId
      };
      this.$emit("input", newVal);
    },
    getItem() {
      let itemId = this.value.itemId;
      if (itemId) {
        this.$store
          .dispatch("attachment/getItemById", itemId)
          .then(item => {
            this.editedItem.id = item.id;
            this.editedItem.original_filename = item.original_filename;
            this.editedItem.description = item.description;
            this.editedItem.rename = item.rename;
            return item;
          })
          .then(item => this.$store.dispatch("attachment/getFileUrl", item.id))
          .then(data => {
            this.editedItem.url = data.file;
          });
      }
    },
    itemExists() {},
    updateDescription: _.debounce(function(value) {
      this.editedItem.description = value;
      this.$v.editedItem.description.$touch();
    }, 300),
    close() {
      let newVal = {
        dialog: false,
        itemId: null
      };
      this.$v.$reset();
      this.$emit("input", newVal);
    },
    onfileSelectorChanged(obj) {
      this.filesList = obj.filesList;
      this.fileInputRef = obj.fileInputRef;
    },
    onDownload() {
      triggerFileDownload(this.editedItem.url);
    },
    acceptDialog() {
      let item = _.clone(this.editedItem);
      if (this.isNew) {
        this.$emit("createItem", {
          item,
          fileInputRef: this.fileInputRef
        });
      } else {
        this.$emit("updateItem"),
          {
            item,
            fileInputRef: this.fileInputRef
          };
      }
    }
  },
  watch: {
    value: {
      //watch dialog prop if false close dialog??
      handler(value) {
        if (value.itemId) {
          this.getItem();
        } else {
          this.editedItem.description = "";
          this.editedItem.rename = "";
        }
      },
      deep: true
    }
  },
  components: {
    AppFileSelector
  }
};
</script>
