<template>
  <v-container>

    <v-layout
      text-xs-center
      wrap
    >

      <v-flex>
        <v-card>
          <v-card-title class="justify-center">
            <div>
              <h3 class="headline mb-0">Tags</h3>
            </div>
            <!-- <v-card-text>
            <p class="text-xs-center">Center align on all viewport sizes</p>
          </v-card-text> -->
          </v-card-title>
        </v-card>
      </v-flex>

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
          <td class="text-xs-right">{{ props.item.created_by }}</td>
          <td class="text-xs-right">{{ props.item.created_on | formatDate}}</td>
          <td class="text-xs-right">{{ props.item.modified_by }}</td>
          <td class="text-xs-right">{{ props.item.modified_on | formatDate}}</td>
        </template>
      </v-data-table>

      <div class="text-xs-center pt-2">
        {{ pagination }}<br />
        {{ tags}}
      </div>

    </v-layout>
    <v-layout>
      <v-btn @click="getDataFromApi"></v-btn>

    </v-layout>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      // search: "",
      // pagination: {},
      pagination: {},
      headers: [],
      tags: [],
      totalTags: 0,
      loading: true
    };
  },
  methods: {
    getDataFromApi() {
      let pagetext = "";
      if (this.pagination) {
        if (this.pagination.page > 1) {
          pagetext = "?page=" + this.pagination.page;
        }
      }
      let url = "http://127.0.0.1:8000/api/tag/" + pagetext;
      this.loading = true;
      return axios.get(url).then(resp => {
        this.loading = false;

        return resp.data;
      });
    },
    getFieldsFromApi() {
      this.loading = true;
      return axios.options("http://127.0.0.1:8000/api/tag/").then(resp => {
        this.loading = false;
        return resp.data;
      });
    }
  },
  watch: {
    pagination: {
      handler() {
        this.getDataFromApi().then(data => {
          this.tags = data.results;
          this.totalTags = data.count;
        });
      },
      deep: true
    }
  },

  mounted() {
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
