<template>
  <v-container>
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

    <v-layout
      text-xs-center
      wrap
    >
      <v-data-table
        :headers="headers"
        :items="tags"
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
    </v-layout>
    <v-layout>
      <v-btn @click="retrieveData"></v-btn>

    </v-layout>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      headers: [
        // { text: "id", value: "id" },
        // { text: "name", align: "left", sortable: false, value: "name" },
        // { text: "created by", value: "created_by" },
        // { text: "creted on ", value: "created_on" },
        // { text: "modified by", value: "modified_by" },
        // { text: "modified on ", value: "modified_on" }
      ],
      tags: []
    };
  },
  methods: {
    retrieveData() {
      axios.get("http://127.0.0.1:8000/api/tag/").then(resp => {
        this.tags = resp.data.results;
      });
    }
  },

  created() {
    axios
      .options("http://127.0.0.1:8000/api/tag/")
      .then(resp => resp.data.actions)
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
        this.headers[1].sortable = false;
      });

    axios.get("http://127.0.0.1:8000/api/tag/").then(resp => {
      this.tags = resp.data.results;
    });
  }
};
</script>

<style>
</style>
