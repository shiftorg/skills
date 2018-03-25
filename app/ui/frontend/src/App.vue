<template>
  <div id="app">
    <router-view name="resume_form"></router-view>
    <router-view name="jobs"></router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style lang="css">

/*****************/
/* Main elements */
/*****************/
body, html {
    padding-bottom: 0px;
    margin-bottom: 0px;
}

/******************/
/* Navigation Bar */
/******************/
.navbar-nav a {
    color: white;
}

/***************/
/* Site Footer */
/***************/
footer {
    width: 100%;
    background-color: #f7f7f9;
    bottom: 0;
    margin: 0;
    padding: 0;
}

.footer-text {
    text-align: left;
    color: black;
    padding-top: 10px;
    padding-left: 40px;
    padding-bottom: 0px;
    background-color: #f7f7f9;
}
</style>
