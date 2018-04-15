import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import Router from 'vue-router'
import ResumeForm from '@/components/ResumeForm'


Vue.use(Router)
Vue.use(BootstrapVue)

export default new Router({
  routes: [
    {
      path: '/',
      components: {
        resume_form: ResumeForm
      }
    }
  ]
})
