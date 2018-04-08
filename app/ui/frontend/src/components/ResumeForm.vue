<template>
<div>
  <section class="section">

    <div class="row">
      <div class="col-lg">

        <h1>Paste in your resume!</h1>
        <p>
          <textarea v-model="resume_text" class="resume_upload_form" style="width: 500px; height:500px;"></textarea>
        </p>

        <button v-on:click.prevent="send_resume">Parse Resume</button>
      </div>
      <div class="col-lg">
        <h2>Your Skills</h2>
        <p>
        Did we miss anything? Or add anything that doesn't look quite right? Edit your skills in the box below,
        then submit your profile to the service.
        </p>
        <p>
          <input-tag :tags.sync="skills_to_send"></input-tag>
        </p>
        <button v-on:click.prevent="send_skills">Send Skills</button>
        <br>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">

      <br>

      <p>
        We found a few jobs that might be a good fit for you! Skills in red below are skills associated with this jobs which you don't have yet.
      </p>

      <div class="card-deck">
        <div class="card" v-if="jobs.length > 0" v-for="job in jobs" v-bind:key="job.id" style="width: 24rem;">

          <div class="card-block">
            <h4 class="card-title">{{ job.job_name }}</h4>
            <p class="card-text">Common skills for this job:</p>
            <ul>
               <li v-for="(skill, i) in job.skills.has" v-bind:key="i" style="color: green">{{ skill }}</li>
               <li v-for="(skill, i) in job.skills.missing" v-bind:key="i" style="color: red">{{ skill }}</li>
            </ul>
          </div>
	<button v-on:click.prevent="more_info()">More Info..</button>
        </div>
      </div>
    </div>
  </section>
</div>
</template>

<script>
// [data]
//  - resume_text: raw text provided by the use
//  - parsed_skills: whatever response the server sends
//                   in response to this resume
// [methods]
//  - send_resume: take the form input with a user's resumse,
//                 send it to the server, store the server's
//                 response
export default {
  data() {
    return {
      resume_text: "",
      parsed_skills: "",
      skills_to_send: [],
      jobs: []
    }
  },
  methods: {
    // send a resume from the front-end to Flask and store
    // the response
    send_resume: function(){
      this.$http.post("/api/resume", this.resume_text)
      .then(function(data) {
        var skills = JSON.parse(data.bodyText).parsed_skills
        this.parsed_skills = skills;
        this.skills_to_send = skills;
      })
    },
    send_skills: function(){
      console.log("Sending skills to Flask");
      this.$http.post("/api/predict", this.skills_to_send)
      .then(function(data) {
        var skills_response  = JSON.parse(data.bodyText).content;
        this.jobs = skills_response;
        console.log("Response from Flask:");
        console.log(skills_response);
      })
    },
    more_info: function() {
      var base_url = "http://34.235.155.212:5601/app/kibana#/dashboard/1f46d3b0-36eb-11e8-bc51-3d1df9db5706?_g=()&_a=(filters:!(),options:(darkTheme:!f),panels:!((col:7,id:'901a10a0-36e8-11e8-bc51-3d1df9db5706',panelIndex:1,row:1,size_x:6,size_y:3,type:visualization),(col:1,id:f2ba0fc0-36e9-11e8-bc51-3d1df9db5706,panelIndex:2,row:4,size_x:6,size_y:3,type:visualization),(col:7,id:'2133c180-36e9-11e8-bc51-3d1df9db5706',panelIndex:3,row:4,size_x:6,size_y:3,type:visualization),(col:1,id:'51128180-36e8-11e8-bc51-3d1df9db5706',panelIndex:4,row:1,size_x:6,size_y:3,type:visualization),(col:1,id:'9d9c34a0-36e9-11e8-bc51-3d1df9db5706',panelIndex:5,row:7,size_x:6,size_y:3,type:visualization),(col:7,id:'79876e00-3a30-11e8-8de6-81a699545c9e',panelIndex:6,row:7,size_x:6,size_y:3,type:visualization),(col:1,id:ce3585d0-3a7c-11e8-a300-439e4674ea29,panelIndex:7,row:10,size_x:6,size_y:3,type:visualization)),query:(query_string:(analyze_wildcard:!t,REPLACE_QUERY_TERM)),timeRestore:!f,title:'Jobs%20Dashboard',uiState:(),viewMode:view)";
      var url_encoded_job_name = encodeURIComponent('data scientist');
      var query_param = "query:'jobType:%20%22".concat(url_encoded_job_name, "%22%20OR%20searchTerm:%20%22", url_encoded_job_name, "%22'");
      var url = base_url.replace("REPLACE_QUERY_TERM", query_param);
      var win = window.open(url, '_blank');
      win.focus();
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
