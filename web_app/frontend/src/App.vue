<template>
  <TopNavigation />
  <router-view/>
</template>

<script>
import TopNavigation from './components/TopNavigation.vue'

export default {
  name: 'App',
  components: {
    TopNavigation
  }
}
</script>

<style>
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  background-color: rgb(245, 245, 245);
  color: #2c3e50;
  margin-top: 60px;
  height: 100%;
}

button { 
  border-color: #B58D74 !important;
  background-color: #B58D74 !important;
  color: white !important;
}

button:active, button:hover { 
  border-color: #B58D74 !important;
  background-color: #8a5636 !important;
} 

/* #main {
  background-color: white;
  border-radius: 0.5cm;
} */

</style>
