<template>
<div>
  <section class="section">
    <div class="container">

      <button v-on:click.prevent="get_data">Explore Jobs</button>
      <br><br>

      <div class="card-deck">
        <div class="card" v-if="jobs.length > 0" v-for="job in jobs" v-bind:key="job.id" style="width: 24rem;">

          <div class="card-block">
            <h4 class="card-title">{{ job.job_name }}</h4>
            <p class="card-text">Common skills for this job:</p>
            <ul>
               <li v-for="(skill, i) in job.skills.has" v-bind:key="i" class="skill_has">{{ skill }}</li>
               <li v-for="(skill, i) in job.skills.missing" v-bind:key="i" class="skill_missing">{{ skill }}</li>
            </ul>
            <a href="#" class="btn btn-primary">Learn More</a>
          </div>

        </div>
      </div>
    </div>
  </section>
</div>
</template>

<script>
import { fetchJobDescriptions } from '@/api'

// [data]
//  - jobs: an array of jobs and skills to be shown in KPI cards.
//          One "job" is of the form 
//          {"job_name": str, "skills": {"has": [], "missing": []}}
// [methods]
//  - get_data: hit the server and ask for relevant jobs. Will
//              be deprecated soon in favor of response to a resume
export default {
  data() {
    return {
      jobs: []
    }
  },
  //beforeMount() {
  //  fetchJobDescriptions(3).then(response => {
  //    this.jobs = response
  //  })
  //},
  methods: {
    get_data: function(){
      this.$http.get("/api/data")
      .then(function(data) {
        this.jobs = JSON.parse(data.bodyText).job_data;
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding-left: 0;
  padding-top: 10px;
  padding-bottom: 10px;
}
</style>
