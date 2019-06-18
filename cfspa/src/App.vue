<template>
  <v-app>

    <!-- <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>crows</span>
        <span class="font-weight-light">flock</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        flat
        href="https://github.com/vuetifyjs/vuetify/releases/latest"
        target="_blank"
      >
        <span class="mr-2">Latest Release</span>
      </v-btn>
    </v-toolbar> -->

    <!-- <v-content>
      <MainContent />
    </v-content> -->

    <!-- <app-drawer></app-drawer> -->
    <app-toolbar></app-toolbar>
    <main>
      <v-content>
        <router-view></router-view>
      </v-content>
    </main>
    <app-footer></app-footer>

  </v-app>
</template>

<script>
//import MainContent from "./components/MainContent";
import appFooter from "./components/core/AppFooter";
import appToolbar from "./components/core/AppToolbar";
//import appDrawer from "./components/core/AppDrawer";

export default {
  name: "App",
  components: {
    //  MainContent,
    //  appDrawer,
    appToolbar,
    appFooter
  },
  data() {
    return {
      //
    };
  }
};
</script>
