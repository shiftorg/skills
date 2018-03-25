<template>
<div>
  <section class="section">
    <h1>Paste in your resume!</h1>
    <p>
      <textarea v-model="resume_text" class="resume_upload_form" style="width: 500px; height:500px;"></textarea>
    </p>

    <button v-on:click.prevent="send_resume">Submit</button>

    <h2>response from flask</h2>
    <p>
    {{prediction_on_resume}}
    </p>
    <br>
  </section>
</div>
</template>

<script>
// [data]
//  - resume_text: raw text provided by the use
//  - prediction_on_resume: whatever response the server sends
//                          in response to this resume
// [methods]
//  - send_resume: take the form input with a user's resumse,
//                 send it to the server, store the server's
//                 response
export default {
  data() {
    return {
      resume_text: "",
      prediction_on_resume: {}
    }
  },
  methods: {
    // send a resume from the front-end to Flask and store
    // the response
    send_resume: function(){
      this.$http.post("/api/resume", this.resume_text)
      .then(function(data) {
        this.prediction_on_resume = JSON.parse(data.bodyText);
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
