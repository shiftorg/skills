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
      skills_to_send: []
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
      this.$http.post("/api/predict", this.parsed_skills)
      .then(function(data) {
        var skills_response  = JSON.parse(data.bodyText).content;
        this.jobs = skills_response;
        console.log("Response from Flask:");
        console.log(skills_response);
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
