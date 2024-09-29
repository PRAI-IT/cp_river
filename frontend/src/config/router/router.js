import { createRouter, createWebHistory } from 'vue-router'
const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: '/',
			name: 'index',
			component: () => import('@/components/RiverIndex.vue')
		},

	],
	scrollBehavior (to, from, savedPosition) {
		if (savedPosition) return savedPosition
		else return { top: 0 };
	}
})
export default router
