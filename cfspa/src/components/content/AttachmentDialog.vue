
 <template>
  <v-dialog
    v-model="dialog"
    max-width="500px"
    @keydown.esc="cancel"
    @keydown.enter="save"
  >
    <template v-slot:activator="{ on }">
      <v-btn color="primary" dark class="mb-2" v-on="on">New Attachment</v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">{{ formTitle }}</span>
      </v-card-title>

      <v-card-text>
        <v-container grid-list-md>
          <v-layout wrap>
            <v-flex xs12 sm6 md4>
              <v-text-field
                v-model="editedItem.description"
                :error-messages="descriptionErrors"
                count="256"
                required
                label="description"
                @input="$v.editedItem.description.$touch()"
                @blur="$v.editedItem.description.$touch()"
              ></v-text-field>
              <v-text-field
                v-model="editedItem.rename"
                :error-messages="renameErrors"
                count="256"
                label="rename file to"
                @input="$v.editedItem.rename.$touch()"
                @blur="$v.editedItem.rename.$touch()"
              ></v-text-field>
            </v-flex>
          </v-layout>
        </v-container>
        <app-file-upload></app-file-upload>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" flat @click="close">Cancel</v-btn>
        <v-btn
          color="blue darken-1"
          flat
          @click="save"
          :disabled="$v.$invalid || !isValidUpload"
          >Save</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

 <script>
import { required, minLength, maxLength } from "vuelidate/lib/validators";
import AppFileUpload from "./FileUpload";
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      editedItem: {
        description: "",
        rename: ""
      },
      dialog: false
    };
  },
  validations: {
    editedItem: {
      description: {
        required,
        minLength: minLength(3),
        maxLength: maxLength(256)
      },
      rename: {
        maxLength: maxLength(256)
      }
    }
  },
  computed: {
    ...mapGetters({
      isValidUpload: "attachment/isValidUpload"
    }),
    formTitle() {
      return this.editedIndex === -1 ? "New Item" : "Edit Item";
    },
    descriptionErrors() {
      const errors = [];
      if (!this.$v.editedItem.description.$dirty) return errors;
      !this.$v.editedItem.description.minLength &&
        errors.push("description must be more than 3 characters long");
      !this.$v.editedItem.description.maxLength &&
        errors.push("description must be less than 256 characters long");
      !this.$v.editedItem.description.required &&
        errors.push("Name is required.");
      return errors;
    },
    renameErrors() {
      const errors = [];
      if (!this.$v.editedItem.rename.$dirty) return errors;
      !this.$v.editedItem.description.maxLength &&
        errors.push("description must be less than 256 characters long");
      return errors;
    }
  },
  methods: {
    save() {
      this.close();
      this.$emit("savedObject", { name: this.editedItem.name });
      this.editedItem = {};
    },
    close() {
      this.dialog = false;
    }
  },
  components: {
    AppFileUpload
  }
};
</script>
