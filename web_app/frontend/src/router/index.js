import { createRouter, createWebHistory } from 'vue-router'
import TextSummarizer from '../views/TextSummarizer.vue'
import BookRecommender from '../views/BookRecommender.vue'

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
        path: '/book-recommender',
        name: 'BookRecommender',
        component: BookRecommender,
        meta: {
            title: 'Book Recommender',
        }
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router