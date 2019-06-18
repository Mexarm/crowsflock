<template>
  <v-container>
    <v-layout
      text-xs-center
      wrap
    >
      <v-flex xs12>
        <v-img
          :src="require('../assets/crow.png')"
          class="my-3"
          contain
          height="200"
        ></v-img>
      </v-flex>

      <v-flex mb-4>
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
      </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      mydata: { data: "nothing" }
    };
  },
  methods: {
    retrieveData() {
      axios.get("http://127.0.0.1:8000/api/tag/").then(resp => {
        // eslint-disable-next-line
        this.mydata = resp.data;
        //console.log(resp.data);
      });
    }
  }
};
</script>

<style>
</style>
