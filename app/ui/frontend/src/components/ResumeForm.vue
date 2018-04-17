<template>
<div>
  <section class="section">

    <div class="row">
      <div class="col-lg">

        <h3>Paste your resume</h3>
        <p>
          <textarea v-model="resume_text" class="resume_upload_form" style="width: 500px; height:150px;"></textarea>
        </p>

        <button v-on:click.prevent="send_resume">Submit</button>
      </div>
      <div class="col-lg">
        <h3>Your Skills</h3>
        <p>
        Did we miss anything? Add/Edit/Delete your skills.
        </p>
        <p>
          <input-tag :tags.sync="skills_to_send"></input-tag>
        </p>
        <button v-on:click.prevent="send_skills">Show Recommendations</button>
        <br>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container" id="#job_cards">
      <!----MODALS START---->
      <b-modal id="modal-skills-ref-id" ref="skillsModalRef" hide-footer size="lg">
      <div class="d-block text-center">
        <h3>Skills associated with this job</h3>
        <div><iframe id="modal-skills-ref-id-iframe" src="" frameborder="0" style="height:1200px;width:100%;display:block;" height="100%" width="100%"></iframe></div>
      </div>
      </b-modal>

      <b-modal id="modal-jobs-ref-id" ref="jobsModalRef" hide-footer size="lg">
      <div class="d-block text-center">
        <h3>Companies, locations, titles and trends for this job</h3>
        <div><iframe id="modal-jobs-ref-id-iframe" src="" frameborder="0" style="height:1200px;width:100%;display:block;" height="100%" width="100%"></iframe></div>
      </div>
      </b-modal>

      <b-modal id="modal-salaries-ref-id" ref="salariesModalRef" hide-footer size="lg">
      <div class="d-block text-center">
        <h3>Salaries for this job</h3>
        <div><iframe id="modal-salaries-ref-id-iframe" src="" frameborder="0" style="height:1200px;width:100%;display:block;" height="100%" width="100%"></iframe></div>
      </div>
      </b-modal>

      <!----MODALS END--->

      <br>
      <br>

      <b-card-group deck class="mb-3">
        <b-card no-body v-if="jobs.length > 0" v-for="(job, index) in jobs" v-bind:key="job.id" border-variant="primary" header-bg-variant="primary" header-text-variant="white" align="center">
            <h5 slot="header"> {{ job.job_name }} </h5>
            <h7 slot="footer"> {{getRank(index)}} </h7>
            <p class="card-text" align="center"> {{job.job_name_specific}} </p>
            <b-list-group>
              <b-list-group-item disabled v-for="(skill, i) in job.skills.has.all" v-bind:key="i">
                <strike>{{ skill }}</strike>
                <!--v-icon name="check"></v-icon-->
              </b-list-group-item>
            </b-list-group>
            <b-list-group>
              <b-list-group-item v-for="(skill, i) in job.skills.missing.all" v-bind:key="i">
                <b>{{ skill }}</b>
                <!--v-icon name="uncheck"></v-icon-->
              </b-list-group-item>
            </b-list-group>
            <div>
              <!-- the modal buttons-->
              <button v-on:click="show_skills(job.job_name)">Skills</button>
              <button v-on:click="show_jobs(job.job_name)">Jobs</button>
              <button v-on:click="show_salaries(job.job_name)">Salaries</button>
            </div>
        </b-card>
      </b-card-group>
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
      this.$http.post("/api/predict", this.skills_to_send)
      .then(function(data) {
        var skills_response  = JSON.parse(data.bodyText).predictions;
        this.jobs = skills_response;

        // Scroll this thing into view
        document.getElementById("#job_cards").scrollIntoView();
      })
    },
    get_iframe_src: function(job_name, base_url) {
      var url_encoded_job_name = encodeURIComponent(job_name);
      var query_param = "query:'jobType:%20%22".concat(url_encoded_job_name, "%22%20OR%20searchTerm:%20%22", url_encoded_job_name, "%22'");
      var url = base_url.replace("REPLACE_QUERY_TERM", query_param);

      return url;
    },
    update_html_in_modal: function(src_url, modal_iframe_id) {
      // We have to edit the html on the modal based on the job name and the modal type
      //var inner = document.getElementById(modal_id).innerHTML;
      //console.log(inner);
      //console.log(iframe_html);
      //var inner_replace = inner.replace("REPLACE_ME", iframe_html);
      //console.log(inner_replace);
      document.getElementById(modal_iframe_id).src = src_url;
      document.getElementById(modal_iframe_id).name = Date.now();
    },
    show_jobs: function(job_name) {
      console.log("SHOW JOBS.. JOB NAME: " + job_name);
      var base_url = "http://34.235.155.212:5601/app/kibana#/dashboard/dd5be340-4078-11e8-878a-e7a4605920c3?random=REPLACE_RANDOM&embed=true&_g=()&_a=(filters:!(),options:(darkTheme:!f),panels:!((col:1,id:f2ba0fc0-36e9-11e8-bc51-3d1df9db5706,panelIndex:1,row:1,size_x:6,size_y:3,type:visualization),(col:7,id:'9d9c34a0-36e9-11e8-bc51-3d1df9db5706',panelIndex:2,row:4,size_x:6,size_y:3,type:visualization),(col:7,id:'2133c180-36e9-11e8-bc51-3d1df9db5706',panelIndex:3,row:1,size_x:6,size_y:3,type:visualization),(col:1,id:'901a10a0-36e8-11e8-bc51-3d1df9db5706',panelIndex:4,row:4,size_x:6,size_y:3,type:visualization)),query:(query_string:(analyze_wildcard:!t,REPLACE_QUERY_TERM)),timeRestore:!f,title:Jobs,uiState:(P-1:(vis:(legendOpen:!f)),P-2:(vis:(legendOpen:!f)),P-3:(vis:(legendOpen:!f)),P-4:(vis:(legendOpen:!f))),viewMode:view)";

      var base_url = base_url.replace("REPLACE_RANDOM", Date.now());
      // Get the iframe html, Show the modal and edit the html in the modal
      var src_url = this.get_iframe_src(job_name, base_url);
      console.log("SHOW JOBS.. src_url: " + src_url);
      this.$refs.jobsModalRef.show();
      this.update_html_in_modal(src_url, "modal-jobs-ref-id-iframe");
    },
    show_salaries: function(job_name) {
      console.log("SHOW SALARIES.. JOB NAME: " + job_name);
      var base_url = "http://34.235.155.212:5601/app/kibana#/dashboard/ae76e200-4078-11e8-878a-e7a4605920c3?random=REPLACE_RANDOM&embed=true&_g=()&_a=(filters:!(),options:(darkTheme:!f),panels:!((col:1,id:'7ffab460-3a88-11e8-a300-439e4674ea29',panelIndex:1,row:1,size_x:6,size_y:3,type:visualization),(col:7,id:'79876e00-3a30-11e8-8de6-81a699545c9e',panelIndex:2,row:1,size_x:6,size_y:3,type:visualization),(col:1,id:ce3585d0-3a7c-11e8-a300-439e4674ea29,panelIndex:3,row:4,size_x:6,size_y:3,type:visualization)),query:(query_string:(analyze_wildcard:!t,REPLACE_QUERY_TERM)),timeRestore:!f,title:Salaries,uiState:(P-1:(vis:(legendOpen:!f)),P-2:(vis:(legendOpen:!f)),P-3:(vis:(legendOpen:!f))),viewMode:view)";

      var base_url = base_url.replace("REPLACE_RANDOM", Date.now());

      // Get the iframe html, Show the modal and edit the html in the modal
      var src_url = this.get_iframe_src(job_name, base_url);
      console.log("SHOW SALARIES.. src_url: " + src_url);
      this.$refs.salariesModalRef.show();
      this.update_html_in_modal(src_url, "modal-salaries-ref-id-iframe");
    },
    show_skills: function(job_name) {
      var root = window.location.host;
      // TODO - We need a way to pass in the term, lambda, topic query parameters to the lda_viz endpoint to show topic specific lda
      // Until then, just showing the modal for a generic page
      var url = 'http://' + root + '/lda_viz';

      this.$refs.skillsModalRef.show();
      this.update_html_in_modal(url, "modal-skills-ref-id-iframe");
    },
    getRank: function(index) {
      if (index == 0) {
        return "1st Match";
      }
      
      if (index == 1) {
        return "2nd Match";
      }

      if (index == 2) {
        return "3rd Match";
      }
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
