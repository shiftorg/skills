import Vue from 'vue'
import Router from 'vue-router'
import Jobs from '@/components/Jobs'
import ResumeForm from '@/components/ResumeForm'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      components: {
        jobs: Jobs,
        resume_form: ResumeForm
      }
    }
  ]
})
