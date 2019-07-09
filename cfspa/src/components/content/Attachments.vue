<template>
  <v-container>
    <v-layout text-xs-center wrap>
      <v-card>
        <v-card-title>
          <h3 class="headline mb-0">Attachments</h3>
          <v-spacer></v-spacer>
          <v-text-field
            append-icon="search"
            label="Search"
            single-line
            hide-details
            @input="update"
          ></v-text-field>

          <v-spacer></v-spacer>
          <app-attachment-dialog @savedObject="save"></app-attachment-dialog>
        </v-card-title>

        <v-layout row v-if="alert">
          <v-flex xs12 sm6 offset-sm3>
            <app-alert
              @dismissed="onDismissed"
              :text="alert.message"
              :type="alert.type"
            ></app-alert>
          </v-flex>
        </v-layout>

        <v-data-table
          :headers="headers"
          :items="items"
          :pagination.sync="pagination"
          :total-items="totalItems"
          :loading="loading"
          class="elevation-1"
        >
          <template v-slot:items="props">
            <td>{{ props.item.id }}</td>
            <td class="text-xs-left">{{ props.item.description }}</td>
            <td class="text-xs-left">{{ props.item.original_filename }}</td>
            <td class="text-xs-left">{{ props.item.size | formatFileSize }}</td>
            <td class="text-xs-left">{{ props.item.rename }}</td>
            <td class="text-xs-right">
              {{ props.item.created_by ? props.item.created_by.username : "" }}
            </td>
            <td class="text-xs-right">
              {{ props.item.created_on | formatDate }}
            </td>
            <td class="text-xs-right">
              {{
                props.item.modified_by ? props.item.modified_by.username : ""
              }}
            </td>
            <td class="text-xs-right">
              {{ props.item.modified_on | formatDate }}
            </td>
          </template>
          <template v-slot:no-results>
            <v-alert :value="true" color="error" icon="warning"
              >Your search for "{{ search }}" found no results.</v-alert
            >
          </template>
        </v-data-table>
      </v-card>
    </v-layout>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import _ from "lodash";
import AppAttachmentDialog from "./AttachmentDialog";

export default {
  computed: {
    ...mapGetters({
      items: "attachment/items",
      headers: "attachment/headers",
      totalItems: "attachment/totalItems",
      loading: "loading",
      alert: "alert"
    })
  },
  data() {
    return {
      dialog: false,
      search: "",
      pagination: {}
      //   editedIndex: -1,
      //   editedItem: {
      // name: ""
      //   },
    };
  },
  methods: {
    update: _.debounce(function(value) {
      this.search = value;
    }, 500),
    save(obj) {
      this.$store.dispatch("attachment/save", obj).then(() => {
        this.$store.dispatch("attachment/getTags", {
          pagination: this.pagination,
          searchTxt: this.search
        });
        this.close();
      });
    },
    close() {
      this.dialog = false;
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
      }
      //deep: true
    },
    search: {
      handler() {
        this.$store.dispatch("attachment/getItems", {
          pagination: this.pagination,
          searchTxt: this.search
        });
      }
    },
    dialog(val) {
      val || this.close();
    }
  },

  mounted() {
    this.$store.dispatch("attachment/getHeaders");
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

<style>
</style>
