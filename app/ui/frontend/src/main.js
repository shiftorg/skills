// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App'
import router from './router'
import VueResource from 'vue-resource'
import InputTag from 'vue-input-tag'
import feather from 'vue-icon'

Vue.component('input-tag', InputTag);

Vue.config.productionTip = false
Vue.use(VueResource);
Vue.use(BootstrapVue);
Vue.use(feather, 'v-icon');

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
