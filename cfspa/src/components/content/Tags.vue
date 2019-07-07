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
import { mapGetters } from "vuex";
import _ from "lodash";
import AppTagDialog from "./TagDialog"

export default {
  computed: {
    ...mapGetters({
      tags: 'tag/tags',
      headers: 'tag/headers',
      totalTags: 'tag/totalTags',
      loading: 'loading',
      alert: 'alert'
    })
  },
  components: {
    AppTagDialog,
  },
  data () {
    return {
      dialog: false,
      search: "",
      pagination: {},
      //   editedIndex: -1,
      //   editedItem: {
      // name: ""
      //   },
    };
  },
  methods: {

    update: _.debounce(function (value) {
      this.search = value;
    }, 500),
    save (obj) {
      this.$store.dispatch('tag/save', obj).then(() => {
        this.$store.dispatch('tag/getTags', { pagination: this.pagination, searchTxt: this.search })
        this.close();
      });
    },
    close () {
      this.dialog = false;
    },
    onDismissed () {
      this.$store.dispatch('clearAlert')
    }
  },
  watch: {
    pagination: {
      handler () {
        this.$store.dispatch('tag/getTags', { pagination: this.pagination, searchTxt: this.search })
      }
      //deep: true
    },
    search: {
      handler () {
        this.$store.dispatch('tag/getTags', { pagination: this.pagination, searchTxt: this.search })
      }
    },
    dialog (val) {
      val || this.close();
    }
  },

  mounted () {
    this.$store.dispatch('tag/getTags', { pagination: this.pagination, searchTxt: this.search });
    this.$store.dispatch('tag/getHeaders');
  }
};
</script>

<style>
</style>
