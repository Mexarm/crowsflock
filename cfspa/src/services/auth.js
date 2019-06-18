// import Vue from 'vue'
import axios from "axios";

// export default {
function authenticate(request) {
  return (
    axios
      .post("http://localhost:8000/api/token/", request)
      // return Vue.http.post('https://crossorigin.me/http://postb.in/VWOhALuu', request)
      .then(response => Promise.resolve(response.data))
      .catch(error => Promise.reject(error))
  );
}

function refreshToken(data) {
  return (
    axios
      .post("http://localhost:8000/api/token/refresh/", data)
      // return Vue.http.post('https://crossorigin.me/http://postb.in/VWOhALuu', request)
      .then(response => Promise.resolve(response.data.access))
      .catch(error => Promise.reject(error))
  );
}
// };

export default { authenticate, refreshToken };
