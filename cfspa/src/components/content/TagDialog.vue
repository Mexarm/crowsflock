
 <template>

  <v-dialog
    v-model="dialog"
    max-width="500px"
    @keydown.esc="cancel"
  >
    <template v-slot:activator="{ on }">
      <v-btn
        color="primary"
        dark
        class="mb-2"
        v-on="on"
      >New Tag</v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">{{ formTitle }}</span>
      </v-card-title>

      <v-card-text>
        <v-container grid-list-md>
          <v-layout wrap>
            <v-flex
              xs12
              sm6
              md4
            >
              <v-text-field
                v-model="editedItem.name"
                :error-messages="nameErrors"
                count="32"
                required
                label="name"
                @input="$v.editedItem.name.$touch()"
                @blur="$v.editedItem.name.$touch()"
              ></v-text-field>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="blue darken-1"
          flat
          @click="close"
        >Cancel</v-btn>
        <v-btn
          color="blue darken-1"
          flat
          @click="save"
          :disabled="$v.$invalid"
        >Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

 <script>
import { required, minLength, maxLength } from 'vuelidate/lib/validators'

export default {
  data () {
    return {
      editedItem: {
        name: ''
      },
      dialog: false
    }
  },
  validations: {
    editedItem: {
      name: {
        required,
        minLength: minLength(3),
        maxLength: maxLength(32)
      }
    }
  },
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? "New Item" : "Edit Item";
    },
    nameErrors () {
      const errors = []
      if (!this.$v.editedItem.name.$dirty) return errors
      !this.$v.editedItem.name.minLength && errors.push('Name must be more than 3 characters long')
      !this.$v.editedItem.name.maxLength && errors.push('Name must be less than 32 characters long')
      !this.$v.editedItem.name.required && errors.push('Name is required.')
      return errors
    },
  },
  methods: {
    save () {
      this.close();
      this.$emit('savedObject', { name: this.editedItem.name });
      this.editedItem = {}

    },
    close () {
      this.dialog = false
    }
  }
}
 </script>
