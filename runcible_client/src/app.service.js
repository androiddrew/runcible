import axios from "axios";

axios.defaults.baseURL = "http://localhost:5000";

const appService = {
  getPing() {
    return new Promise((resolve, reject) => {
      axios
        .get("/ping")
        .then(response => {
          resolve(response.data);
        })
        .catch(error => {
          reject(error.status);
        });
    });
  }
};

export default appService;
