<template>
  <v-container>
    <v-layout
      row
      v-if="alert"
    >
      <v-flex
        xs12
        sm6
        offset-sm3
      >
        <app-alert
          @dismissed="onDismissed"
          :text="alert.message"
          :type="alert.type"
        ></app-alert>
      </v-flex>
    </v-layout>
    <v-layout row>
      <v-flex
        xs12
        sm6
        offset-sm3
      >
        <v-card>
          <v-card-text>
            <v-container>
              <form @submit.prevent="onSignin">
                <v-layout row>
                  <v-flex xs12>
                    <v-text-field
                      name="username"
                      label="username"
                      id="username"
                      v-model="username"
                      type="text"
                      required
                    ></v-text-field>
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex xs12>
                    <v-text-field
                      name="password"
                      label="Password"
                      id="password"
                      v-model="password"
                      type="password"
                      required
                    ></v-text-field>
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex xs12>
                    <v-btn
                      type="submit"
                      :disabled="loading"
                      :loading="loading"
                    >
                      Sign in
                      <span
                        slot="loader"
                        class="custom-loader"
                      >
                        <v-icon light>cached</v-icon>
                      </span>
                    </v-btn>
                  </v-flex>
                </v-layout>
              </form>
            </v-container>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
/* import {
  required,
  email,
  numeric,
  minValue,
  minLength,
  sameAs,
  requiredUnless
} from 'vuelidate/lib/validators' */
export default {
  data() {
    return {
      username: "",
      password: ""
    };
  },
  computed: {
    user() {
      return this.$store.getters.user;
    },
    alert() {
      return this.$store.getters.alert;
    },
    loading() {
      return this.$store.getters.loading;
    }
  },
  watch: {
    user(value) {
      if (value !== null && value !== undefined) {
        this.$router.push("/");
      }
    }
  },
  methods: {
    onSignin() {
      this.$store.dispatch("signInUser", {
        username: this.username,
        password: this.password
      });
    },
    onDismissed() {
      this.$store.dispatch("clearAlert");
    }
  }
};
</script>
