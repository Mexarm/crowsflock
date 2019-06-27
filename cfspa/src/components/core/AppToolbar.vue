<template>
  <v-toolbar
    app
    color="primary"
    dark
    fixed
    height="58px"
    id="app-toolbar"
  >
    <v-toolbar-side-icon
      dark
      @click.stop="sideNav = !sideNav"
      class="hidden-sm-and-up"
    ></v-toolbar-side-icon>
    <router-link
      to="/"
      class="d-flex ml-3"
    >
      <img
        src="@/assets/crow.png"
        height="38px"
        width="38px"
        alt="vapp"
      >
    </router-link>
    <v-fade-transition mode="out-in">
      <v-toolbar-title class="pb-1 hidden-xs-only">crowsflock</v-toolbar-title>
    </v-fade-transition>
    <v-spacer></v-spacer>
    <v-toolbar-items class="hidden-xs-only">
      <!-- menu desplegable -->
      <!-- <div class="text-xs-center"> -->
      <v-menu
        offset-y
        v-if="userIsAuthenticated"
      >
        <template v-slot:activator="{ on }">
          <v-btn
            flat
            v-on="on"
          >
            <v-icon
              left
              dark
            >home
            </v-icon>
            Menu
          </v-btn>
        </template>
        <v-list>
          <v-list-tile
            v-for="(item, index) in menuItems"
            :key="index"
            :to="item.link"
          >

            <v-icon left>{{item.icon}}

            </v-icon>
            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>
      <!-- </div> -->
      <!-- menu -->

      <!-- <v-btn
        flat
        v-for="item in menuItems"
        :key="item.title"
        :to="item.link"
      >
        <v-icon
          left
          dark
        >{{ item.icon }}
        </v-icon>
        {{ item.title }}
      </v-btn> -->

      <v-btn
        v-if="userIsAuthenticated"
        flat
        @click="onLogout"
      >
        <v-icon
          left
          dark
        >exit_to_app</v-icon>
        Logout
      </v-btn>

      <v-btn
        v-if="!userIsAuthenticated"
        flat
        :to="{ name: 'SignIn'}"
      >
        <v-icon
          left
          dark
        >lock_open</v-icon>
        Login
      </v-btn>
    </v-toolbar-items>
  </v-toolbar>

</template>

<script>
export default {
  computed: {
    sideNav: {
      get() {
        return this.$store.getters.sideNav;
      },
      set(value) {
        this.$store.dispatch("updateSideNav", value);
      }
    },
    menuItems() {
      return this.$store.getters.menuItems;
    },
    userIsAuthenticated() {
      return this.$store.getters.userIsAuthenticated;
    }
  },
  methods: {
    onLogout() {
      this.$store.dispatch("signOutUser");
    }
  }
};
</script>


<style>
#app-toolbar .toolbar__title {
  margin-left: 0.5em;
  font-weight: 300;
  font-size: 21px;
  position: relative;
  top: 1px;
}

#app-toolbar .toolbar__items .btn {
  text-transform: capitalize;
  font-size: 16px;
  font-weight: 300;
}
</style>