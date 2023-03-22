import { createRouter, createWebHistory } from 'vue-router'
import TextSummarizer from '../views/TextSummarizer.vue'

const routes = [
    {
        path: '/text-summarizer',
        name: 'TextSummarizer',
        component: TextSummarizer,
        meta: {
            title: 'Text Summarizer',
        }
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router