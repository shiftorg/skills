import Vue from 'vue'
import Router from 'vue-router'
import ResumeForm from '@/components/ResumeForm'

Vue.use(Router)

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
