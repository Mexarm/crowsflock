<template>
  <v-container>
    <v-layout
      text-xs-center
      wrap
    >
      <!-- <v-flex xs12>
        <v-img
          :src="require('../assets/crow.png')"
          class="my-3"
          contain
          height="200"
        ></v-img>
      </v-flex> -->

      <!-- <v-flex mb-4>
        <h1 class="display-2 font-weight-bold mb-3">
          Welcome to CrowsFlock
        </h1>
        <p class="subheading font-weight-regular">
          Digital Comunication Platform
          data is : {{ mydata }}
          <v-btn
            v-on:click="retrieveData"
            small
          >Retrieve Data</v-btn>
        </p>
      </v-flex> -->

      <v-data-table
        :headers="headers"
        :items="tags"
        class="elevation-1"
      >
        <template v-slot:items="props">
          <td>{{ props.item.id }}</td>
          <td class="text-xs-right">{{ props.item.name }}</td>
          <td class="text-xs-right">{{ props.item.created_by }}</td>
          <td class="text-xs-right">{{ props.item.created_on | formatDate}}</td>
          <td class="text-xs-right">{{ props.item.modified_by }}</td>
          <td class="text-xs-right">{{ props.item.modified_on | formatDate}}</td>
        </template>
      </v-data-table>
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
        { text: "id", value: "id" },
        { text: "name", align: "left", sortable: false, value: "name" },
        { text: "created by", value: "created_by" },
        { text: "creted on ", value: "created_on" },
        { text: "modified by", value: "modified_by" },
        { text: "modified on ", value: "modified_on" }
      ],
      tags: []
    };
  },
  methods: {
    retrieveData() {
      axios.get("http://127.0.0.1:8000/api/tag/").then(resp => {
        this.tags = resp.data.results;

        //console.log(resp.data);
      });
    }
  }
};
</script>

<style>
</style>
