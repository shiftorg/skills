<template>
<div>
  <section class="section">
    <div class="container">
      <div class="card-deck">
        <div class="card" v-for="job in jobs" v-bind:key="job.id">

          <div class="card-block">
            <h4 class="card-title">{{ job.job_title }}</h4>
            <p class="card-text">Common skills for this job:</p>
            <ul>
               <li v-for="(skill, i) in job.skills" v-bind:key="i">{{ skill }}</li>
            </ul>
            <a href="#" class="btn btn-primary">Learn More</a>
          </div>

          <div class="card-footer">
            <small class="text-muted">match: {{ job.match }}</small>
          </div>

        </div>
      </div>
    </div>
  </section>
</div>
</template>

<script>
import { fetchJobDescriptions } from '@/api'

export default {
  data() {
    return {
      jobs: []
    }
  },
  beforeMount() {
    fetchJobDescriptions(3).then(response => {
      this.jobs = response
    })
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
