<template>
  <v-container>
    <v-layout
      text-xs-center
      wrap
    >
      <v-card>
        <v-card-title>
          <h3 class="headline mb-0">Tags</h3>
          <v-spacer></v-spacer>
          <v-text-field
            append-icon="search"
            label="Search"
            single-line
            hide-details
            @input="update"
          ></v-text-field>

          <v-spacer></v-spacer>
          <app-tag-dialog @savedObject="save"></app-tag-dialog>
        </v-card-title>

        <v-layout
          row
          v-if="event"
        >
          <v-flex
            xs12
            sm6
            offset-sm3
          >
            <app-alert
              @dismissed="onDismissed"
              :text="event.message"
              :type="event.type"
            ></app-alert>
          </v-flex>
        </v-layout>

        <v-data-table
          :headers="headers"
          :items="tags"
          :pagination.sync="pagination"
          :total-items="totalTags"
          :loading="loading"
          class="elevation-1"
        >
          <template v-slot:items="props">
            <td>{{ props.item.id }}</td>
            <td class="text-xs-left">{{ props.item.name }}</td>
            <td class="text-xs-left">{{ props.item.slug }}</td>
            <td class="text-xs-right">{{ props.item.created_by ? props.item.created_by.username: '' }}</td>
            <td class="text-xs-right">{{ props.item.created_on | formatDate}}</td>
            <td class="text-xs-right">{{ props.item.modified_by ? props.item.modified_by.username:'' }}</td>
            <td class="text-xs-right">{{ props.item.modified_on | formatDate}}</td>
          </template>
          <template v-slot:no-results>
            <v-alert
              :value="true"
              color="error"
              icon="warning"
            >Your search for "{{ search }}" found no results.</v-alert>
          </template>
        </v-data-table>
      </v-card>
    </v-layout>
  </v-container>
</template>

<script>
import axios from "axios";
import _ from "lodash";
import auth from "../../services/auth";
import AppTagDialog from "./TagDialog"
const url = auth.settings.baseUrl + "api/tag/";

export default {
  components: {
    AppTagDialog,
  },
  data () {
    return {
      event: null,
      dialog: false,
      search: "",
      pagination: {},
      headers: [],
      tags: [],
      totalTags: 0,
    //   editedIndex: -1,
    //   editedItem: {
        // name: ""
    //   },
      loading: true
    };
  },
  methods: {
    getDataFromApi () {
      const page =
        typeof this.pagination === "object" &&
          typeof this.pagination.page === "number" &&
          this.pagination.page > 1
          ? this.pagination.page
          : false;
      const ordering =
        typeof this.pagination === "object" &&
          typeof this.pagination.sortBy === "string" &&
          this.pagination.sortBy.length > 0
          ? this.pagination.sortBy
          : false;
      const descending =
        typeof this.pagination === "object" &&
          typeof this.pagination.descending === "boolean" &&
          this.pagination.descending
          ? "-"
          : "";

      const search =
        typeof this.search === "string" && this.search.length > 0
          ? this.search
          : false;

      const rowsPerPage =
        typeof this.pagination === "object" &&
          typeof this.pagination.rowsPerPage === "number" &&
          this.pagination.rowsPerPage > 0
          ? this.pagination.rowsPerPage
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

      this.loading = true;
      return axios.get(url, { params }).then(resp => {
        this.loading = false;
        return resp.data;
      });
    },
    getFieldsFromApi () {
      this.loading = true;
      return axios.options(url).then(resp => {
        this.loading = false;
        return resp.data;
      });
    },
    saveToAPi (data) {
      return axios
        .post(url, data)
        .then(response => {
          if (response.status === 201) {
            this.event = {
              message: response.data.name + ', ' + response.statusText,
              type: "success"
            };
            return response;
          }
        })
        .catch(error => {
          this.event = {
            message: error,
            type: "error"
          };
        });
    },
    update: _.debounce(function (value) {
      this.search = value;
    }, 300),
    save (obj) {
      this.saveToAPi(obj).then(() => {
        this.close();
        this.getDataFromApi().then(data => {
          this.tags = data.results;
          this.totalTags = data.count;
        });
      });
    },
    close () {
      this.dialog = false;
    },
    onDismissed () {
      this.event = {}
    }
  },
  watch: {
    pagination: {
      handler () {
        this.getDataFromApi().then(data => {
          this.tags = data.results;
          this.totalTags = data.count;
        });
      }
      //deep: true
    },
    search: {
      handler () {
        this.getDataFromApi().then(data => {
          this.tags = data.results;
          this.totalTags = data.count;
        });
      }
    },
    dialog (val) {
      val || this.close();
    }
  },

  mounted () {
    this.getFieldsFromApi()
      .then(data => data.actions)
      .then(actions => actions.POST)
      .then(fields => {
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
        this.headers = headers;
      });
    this.getDataFromApi().then(data => {
      this.tags = data.results;
      this.totalTags = data.count;
    });
  }
};
</script>

<style>
</style>
