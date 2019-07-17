<template>
  <v-container grid-list-md text-xs-center fluid>
    <v-layout row wrap>
      <v-flex xs12>
        <v-card>
          <v-card-title class="pt-0 pb-0">
            <p class="headline ml-3 mb-0 pt-2">Attachments</p>
            <!-- @upload-completed="onUploadCompleted" -->
            <app-attachment-dialog
              v-model="dialogModel"
              :allowed="[
                'csv',
                'pdf',
                'xls',
                'xlsx',
                'doc',
                'docx',
                'ppt',
                'jpg',
                'png',
                'txt',
                'zip',
                'rar'
              ]"
              @createItem="onCreatedItem"
              @updateItem="onUpdatedItem"
            ></app-attachment-dialog>
            <v-spacer></v-spacer>
            <v-text-field
              class="ma-0 pa-0"
              append-icon="search"
              label="Search"
              single-line
              hide-details
              clearable
              @input="update"
              :value="search"
            ></v-text-field>
          </v-card-title>
          <v-card-text>
            <app-alert
              v-if="alert"
              @dismissed="onDismissed"
              :text="alert.message"
              :type="alert.type"
            ></app-alert>
            <v-data-table
              :headers="headers"
              :items="items"
              :pagination.sync="pagination"
              :total-items="totalItems"
              :loading="loading"
              :rows-per-page-items="[5, 10, 25, 50]"
              flat
            >
              <template v-slot:items="props">
                <!-- <td>{{ props.item.id }}</td> -->
                <td class="text-xs-left">
                  <v-icon
                    @click="editItem(props.item.id)"
                    class="pr-2"
                    small
                    color="secondary"
                    >edit</v-icon
                  >
                  {{ props.item.description }}
                </td>
                <td class="text-xs-left">
                  {{ props.item.original_filename }}
                </td>
                <td class="text-xs-left">
                  <v-icon
                    @click="editItem(props.item.id)"
                    class="pr-2"
                    small
                    color="green"
                    v-if="props.item.size"
                    >cloud_download</v-icon
                  >
                  {{ props.item.size | formatFileSize }}
                </td>
                <td class="text-xs-left">{{ props.item.rename }}</td>
                <td class="text-xs-left">
                  {{ props.item.created_on | formatDate }} by
                  {{
                    props.item.created_by ? props.item.created_by.username : ""
                  }}
                  <!-- {{
                    props.item.modified_by
                      ? props.item.modified_by.username
                      : ""
                  }}
                  {{ props.item.modified_on | formatDate }} -->
                </td>
                <!-- <td class="text-xs-right">
                  {{ props.item.created_on | formatDate }}
                </td>
                <td class="text-xs-right">
                  {{
                    props.item.modified_by
                      ? props.item.modified_by.username
                      : ""
                  }}
                </td>
                <td class="text-xs-right">
                  {{ props.item.modified_on | formatDate }}
                </td> -->
              </template>
              <template v-slot:no-results>
                <v-alert :value="true" color="error" icon="warning"
                  >Your search for "{{ search }}" found no results.</v-alert
                >
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import _ from "lodash";
import AppAttachmentDialog from "./AttachmentDialog";

export default {
  data() {
    return {
      dialogModel: {
        dialog: false,
        itemId: null
      },
      // editedItemId: null,
      // dialog: false,
      search: "",
      pagination: {
        rowsPerPage: 10
      }
    };
  },
  computed: {
    ...mapGetters({
      items: "attachment/items",
      headers: "attachment/headers",
      listDisplay: "attachment/listDisplay",
      totalItems: "attachment/totalItems",
      loading: "loading",
      alert: "alert"
    })
  },
  methods: {
    // dialogDismissed() {
    //   this.editedItemId = null;
    // },
    editItem(itemId) {
      this.dialogModel.itemId = itemId;
      this.dialogModel.dialog = true;
      // this.editedItemId = itemId;
      // this.dialog = true;
    },
    update: _.debounce(function(value) {
      this.search = value;
    }, 300),
    // onUploadCompleted(payload) {
    //   let obj = payload.obj;
    //   this.$store.dispatch("setAlertTimeout", {
    //     message: obj.description + " uploaded sucessfully!",
    //     type: "success"
    //   });
    //   this.$store.dispatch("attachment/getItems", {
    //     pagination: this.pagination,
    //     searchTxt: this.search
    //   });
    // },
    // onUploadError(error) {
    //   this.$store.dispatch("setAlertTimeout", error);
    // },
    // close() {
    //   this.dialog = false;
    // },
    onCreatedItem(payload) {
      this.$store
        .dispatch("attachment/create", payload.item)
        .then(data =>
          this.$store.dispatch("attachment/uploadFile", {
            id: data.id,
            fileInputRef: payload.fileInputRef
          })
        )
        .then(() => {
          return this.$store
            .dispatch("attachment/getItems", {
              pagination: this.pagination,
              searchTxt: this.search
            })
            .then(() => {
              this.$store.dispatch(
                "setAlertTimeout",
                {
                  message: "file uploaded",
                  type: "success"
                },
                { root: true }
              );
            });
        })
        .then(() => {
          this.dialogModel.dialog = false; //close dialog
          this.dialogModel.itemId = null;
        });
    },
    onUpdatedItem(payload) {
      //eslint-disable-next-line
      console.log(payload);
    },
    onDismissed() {
      this.$store.dispatch("clearAlert");
    }
  },
  watch: {
    pagination: {
      handler() {
        this.$store.dispatch("attachment/getItems", {
          pagination: this.pagination,
          searchTxt: this.search
        });
      },
      deep: true
    },
    search: {
      handler() {
        this.$store.dispatch("attachment/getItems", {
          pagination: this.pagination,
          searchTxt: this.search
        });
      }
    }
    // dialog(val) {
    //   val || this.close();
    // }
  },
  mounted() {
    this.$store.dispatch("attachment/getApiOptions");
    this.$store.dispatch("attachment/getItems", {
      pagination: this.pagination,
      searchTxt: this.search
    });
  },
  components: {
    AppAttachmentDialog
  }
};
</script>