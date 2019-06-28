import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Unicon from "vue-unicons";
import {
  uniHome,
  uniCloudWifi,
  uniQuestionCircle
} from "vue-unicons/src/icons";

Unicon.add([uniHome, uniCloudWifi, uniQuestionCircle]);
Vue.use(Unicon);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
