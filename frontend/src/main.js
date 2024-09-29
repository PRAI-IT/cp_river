import { createApp } from 'vue'

import router from '@/config/router/router.js'

import '@/config/css/reset.css'
import '@/config/css/index.css'

import App from './App.vue'

import {createPinia} from "pinia";
const pinia = createPinia()

const appVue = createApp(App)

appVue
	.use(pinia)
	.use(router)
	.mount('#app')
