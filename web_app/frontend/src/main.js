import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// import axios from 'axios'

// import bootstrap
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap.js"

createApp(App)
.use(router)
.mount('#app')