import { createRouter, createWebHistory } from 'vue-router'
import TextSummarizer from '../views/TextSummarizer.vue'
import ChapterRecommender from '../views/ChapterRecommender.vue'

const routes = [
    {
        path: '/text-summarizer',
        name: 'TextSummarizer',
        component: TextSummarizer,
        meta: {
            title: 'Text Summarizer',
        }
    },

    {
        path: '/',
        name: 'ChapterRecommender',
        component: ChapterRecommender,
        meta: {
            title: 'Chapter Recommender',
        }
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router