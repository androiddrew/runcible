<template>
  <div>
    <h1>{{ msg }}</h1>
  </div>
</template>
<script>
import appService from "../app.service.js";
export default {
  name: "ping",
  data() {
    return {
      msg: ""
    };
  },
  methods: {
    getMessage() {
      appService
        .getPing()
        .then(data => (this.msg = data))
        .catch(error => {
          this.msg = "Network Error: " + error;
        });
    }
  },
  created() {
    this.getMessage();
  }
};
</script>
