<template>
  <v-layout sm-12>
    <div>
      <form ref="fileForm">
        <div class="dropbox">
          <input
            id="file_input"
            ref="file_input"
            type="file"
            :name="uploadFieldName"
            :disabled="state === 'running'"
            @input="
              filesChanged(
                $event.target.name,
                $event.target.files,
                $event.target.accept
              );
              fileCount = $event.target.files.length;
            "
            :accept="allowed.map(item => '.' + item).join(',')"
            class="input-file"
          />
          <p v-if="state !== 'running'">
            <v-icon left>cloud_upload</v-icon>
            Arrastre su Archivo aqui <br />o haga
            <a>click para selecionarlo</a>
          </p>
        </div>
        <span v-for="file in files" :key="file.name">
          <v-chip
            label
            :color="file.allowed ? 'green' : 'red'"
            text-color="white"
          >
            <v-icon v-if="file.allowed" left>cloud_upload</v-icon>
            <v-icon v-if="!file.allowed" left>cloud_off</v-icon
            >{{ file.name }} ({{
              file.allowed ? file.size : " tipo de archivo no valido"
            }})
          </v-chip>
        </span>
      </form>
    </div>
  </v-layout>
</template>

<script>
import { mapGetters } from "vuex";
import filesize from "filesize";
// import axios from "axios";

export default {
  props: {
    allowed: Array
  },
  data: () => ({
    state: "",
    // progress: 0,
    uploadFieldName: "uploadfield",
    files: [],
    fileCount: 0
    // dataStorageFolder: "data",
    // imageStorageFolder: "public",
    // allowed: ["csv", "txt"]
  }),
  // file.type : ['image/tiff' , 'image/jpeg', 'image/png', 'image/gif']
  // file.type : ['application/pdf' , 'application/vnd.oasis.opendocument.spreadsheet' <-ods, 'text/plain', 'text/csv']
  // file.name , file.size, file.lastModified, file.lastModifiedDate, file.type
  computed: {
    ...mapGetters(["alert", "loading"])
  },
  methods: {
    filesChanged(name, files) {
      this.state = "";
      this.files.length = 0;
      Array.from(Array(files.length).keys()).map(x => {
        let tokens = files[x].name.split(".");
        this.files.push({
          name: files[x].name,
          allowed:
            this.allowed.indexOf(tokens[tokens.length - 1].toLowerCase()) !==
            -1,
          size: filesize(files[x].size)
        });
      });
      // this.$store.dispatch(
      //   "attachment/setIsValidUpload",
      //   this.files.every(file => file.allowed) && this.files.length > 0
      // );
      this.$emit("changed", {
        filesList: this.files,
        fileInputRef: this.$refs.file_input
      });
    },
    clearInput() {
      const input = this.$refs.file_input;
      input.type = "text";
      input.type = "file";
      this.files = [];
      this.$emit("changed", {
        filesList: this.files,
        fileInputRef: this.$refs.file_input
      });
    }
  },
  mounted() {
    this.clearInput();
  }
};
</script>

<style scoped>
.dropbox {
  outline: 2px dashed grey;
  /* the dash box */
  outline-offset: -10px;
  background: lightcyan;
  color: dimgray;
  padding: 10px 10px;
  min-height: 200px;
  /* minimum height */
  position: relative;
  cursor: pointer;
}
.input-file {
  opacity: 0;
  /* invisible but it's there! */
  width: 100%;
  height: 200px;
  position: absolute;
  cursor: pointer;
}
.dropbox:hover {
  background: lightblue;
  /* when mouse over to the drop zone, change color */
}
.dropbox p {
  font-size: 1.2em;
  text-align: center;
  padding: 50px 0;
}
</style>
