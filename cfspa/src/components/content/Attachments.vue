<template>
  <v-container
    grid-list-md
    text-xs-center
    fluid
  >
    <v-layout
      row
      wrap
    >
      <v-flex xs12>
        <v-card>
          <v-card-title class="pt-0 pb-0">
            <p class="headline ml-3 mb-0 pt-2">Attachments</p>
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
                <td class="text-xs-left">
                  <v-icon
                    @click="editItem(props.item.id)"
                    class="pr-2"
                    small
                    color="secondary"
                  >edit</v-icon>
                  {{ props.item.description }}
                </td>
                <td class="text-xs-left">
                  {{ props.item.original_filename }}
                </td>
                <td class="text-xs-left">
                  <v-icon
                    @click="downloadFile(props.item.id, props.item.original_filename)"
                    class="pr-2"
                    small
                    color="green"
                    v-if="props.item.size"
                  >cloud_download</v-icon>
                  {{ props.item.size | formatFileSize }}
                </td>
                <td class="text-xs-left">{{ props.item.rename }}</td>
                <td class="text-xs-left">
                  {{ props.item.created_on | formatDate }} by
                  {{
                    props.item.created_by ? props.item.created_by.username : ""
                  }}
                </td>
              </template>
              <template v-slot:no-results>
                <v-alert
                  :value="true"
                  color="error"
                  icon="warning"
                >Your search for "{{ search }}" found no results.</v-alert>
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
import { triggerFileDownload } from "../../utils";

export default {
  data() {
    return {
      dialogModel: {
        dialog: false,
        itemId: null
      },
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
    editItem(itemId) {
      this.dialogModel.itemId = itemId;
      this.dialogModel.dialog = true;
    },
    update: _.debounce(function(value) {
      this.search = value;
    }, 300),
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
    downloadFile(attachmentId, original_filename) {
      // function onStartedDownload(id) {
      //   //eslint-disable-next-line
      //   console.log(`Started downloading: ${id}`);
      // }

      // function onFailed(error) {
      //   //eslint-disable-next-line
      //   console.log(`Download failed: ${error}`);
      // }
      this.$store.dispatch("attachment/getFileUrl", attachmentId).then(data => {
        // let downloadUrl = data.file;
        // return (downloading = browser.downloads.download({
        //   url: downloadUrl,
        //   filename: original_filename,
        //   conflictAction: "uniquify"
        // }));
        // var uriContent =
        //   "data:application/octet-stream," + encodeURIComponent(data.file);
        triggerFileDownload(data.file);
        // var element = document.createElement("a");
        // element.setAttribute("href", data.file);
        // element.style.display = "none";
        // document.body.appendChild(element);
        // element.click();
        // document.body.removeChild(element);
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