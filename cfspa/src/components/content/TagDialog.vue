
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
                        label="name"
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
                >Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
 </template>

 <script>
 export default {
     data() {
         return {
             editedItem : {},
             dialog: false
         }
	},
	computed: {
		formTitle () {
			return this.editedIndex === -1 ? "New Item" : "Edit Item";
		}
	},
     methods: {
         save(){
            this.close();
			this.$emit('savedObject', {name: this.editedItem.name});
			this.editedItem = {}

         },
         close() {
             this.dialog = false
         }
     }
 }
 </script>
