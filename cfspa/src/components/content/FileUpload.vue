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
            accept=".csv,.txt"
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
        <v-btn
          :disabled="!files.every(item => item.allowed) || files.length == 0"
          @click="uploadFiles"
          >Upload Now</v-btn
        >
        <div v-if="state === 'running'">
          cargando {{ fileCount }} archivo(s)... {{ progress }}
          <v-progress-linear v-model="progress"></v-progress-linear>
        </div>
        <v-alert>{{ error }}</v-alert>
      </form>
    </div>
  </v-layout>
</template>

<script>
// import firebase from "firebase/app";
// import "firebase/storage";
import { mapGetters } from "vuex";
import filesize from "filesize";
// const db = firebase.firestore();
import axios from "axios";

export default {
  data: () => ({
    //file: null,
    state: "",
    progress: 0,
    uploadFieldName: "uploadfield",
    files: [],
    fileCount: 0,
    dataStorageFolder: "data",
    imageStorageFolder: "public",
    allowed: ["csv", "txt"]
    //uploadedFile: null
  }),
  computed: {
    ...mapGetters(["alert", "loading"])
  },
  // file.type : ['image/tiff' , 'image/jpeg', 'image/png', 'image/gif']
  // file.type : ['application/pdf' , 'application/vnd.oasis.opendocument.spreadsheet' <-ods, 'text/plain', 'text/csv']
  // file.name , file.size, file.lastModified, file.lastModifiedDate, file.type

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
    },
    uploadFiles() {
      const files = this.$refs.file_input.files;
      let formData = new FormData();
      if (files && files.length > 0) {
        const file = files[0];
        formData.append("file", file);
      }
      const vue = this;
      let config = {
        onUploadProgress: function(progressEvent) {
          vue.progress = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
        }
      };

      axios
        .post("http://127.0.0.1:8000/api/attachment/")
        .then(resp => resp.data)
        .then(data => {
          this.state = "running";
          let uploadUrl =
            "http://127.0.0.1:8000/api/attachment/" + data.id + "/file/";
          return axios.put(uploadUrl, formData, config);
        })
        .then(resp => resp.data)
        .then(data => {
          this.$emit("uploadCompleted", data);
          this.state = "";
        });
    }

    //   const files = this.$refs.file_input.files;
    //   if (files && files.length > 0) {
    //     const ref = firebase.storage().ref();
    //     const uploadedFiles = [];
    //     let promises = [];
    //     let folder = "userfiles/";

    //     Array.from(Array(files.length).keys()).map(i => {
    //       let file = files[i];
    //       let fileData = {};
    //       fileData.name = +new Date() + "-" + file.name;
    //       fileData.originalName = file.name;

    //       let metadata = {
    //         contentType: file.type
    //       };
    //       fileData.path = folder + fileData.name;
    //       //   let task = ref.child(fileData.path).put(file, metadata); //metadata not saved ???
    //       let p = new Promise((resolve, reject) => {
    //         task.on(
    //           "state_changed",
    //           function (snapshot) {
    //             // Observe state change events such as progress, pause, and resume
    //             // Get task progress, including the number of bytes uploaded and the total number of bytes to be uploaded
    //             this.progress =
    //               snapshot.bytesTransferred / snapshot.totalBytes * 100;
    //             switch (snapshot.state) {
    //               case firebase.storage.TaskState.PAUSED: // or 'paused'
    //                 this.state = "paused";
    //                 break;
    //               case firebase.storage.TaskState.RUNNING: // or 'running'
    //                 this.state = "running";
    //                 break;
    //             }
    //           }.bind(this),
    //           function (error) {
    //             // Handle unsuccessful uploads
    //             //this.$store.commit("setError", error);
    //             reject(error);
    //           }.bind(this),
    //           function () {
    //             // Handle successful uploads on complete
    //             // For instance, get the download URL: https://firebasestorage.googleapis.com/...
    //             this.state = "done";
    //             this.progress = 0;
    //             task
    //               .then(snapshot => snapshot.ref.getDownloadURL())
    //               .then(url => {
    //                 fileData.url = url;
    //                 let dsRef = db.collection("datasets").doc();
    //                 fileData.id = dsRef.id
    //                 dsRef
    //                   .set({
    //                     url,
    //                     original_name: fileData.originalName,
    //                     path: fileData.path,
    //                     created_on: firebase.firestore.FieldValue.serverTimestamp()
    //                   })
    //                   .then(() => {
    //                     uploadedFiles.push(fileData);
    //                     resolve(fileData);
    //                   });
    //               })
    //               .catch(error => {
    //                 reject(error);
    //               });
    //           }.bind(this)
    //         );
    //       });
    //       promises.push(p);
    //     });
    //     Promise.all(promises).then((data) => {
    //       //eslint-disable-next-line
    //       console.log('data', data);
    //       //this.uploadedFile = data
    //       this.files = [];
    //       this.fileCount = 0;
    //       this.$refs.file_input.value = null;
    //       this.$emit('uploaded', data)
    //     });
    //   }
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
