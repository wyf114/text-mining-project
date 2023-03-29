import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// import axios from 'axios'

// import bootstrap
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap.js"


// const store = createStore({
//     state () {
//         return {
//             book_text: null,
//         }
//     },
//     mutations: {
//         setCurrentLJ(state, book_text_obj) {
//             state.book_text = book_text_obj
//         },
//     }
// })

createApp(App)
.use(router)
.mount('#app')