import Vue from "vue";
import VueClipboard from "vue-clipboard2";
import VueMaterial from "vue-material";
import "vue-material/dist/theme/default.css";
import "vue-material/dist/vue-material.min.css";
import App from "./App.vue";
import vuetify from '@/plugins/vuetify'

Vue.config.productionTip = false;

Vue.use(VueClipboard);
Vue.use(VueMaterial);

new Vue({
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
