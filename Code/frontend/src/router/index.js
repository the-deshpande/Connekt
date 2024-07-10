import { createRouter, createWebHistory } from "vue-router";
import Ping from "@/components/Ping.vue";
import HomePage from "@/components/HomePage.vue";
import Login from "@/components/Login.vue";

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: "/",
			name: "HomePage",
			component: HomePage,
		},
		{
			path: "/ping",
			name: "Ping",
			component: Ping,
		},
		{
			path: "/login",
			name: "Login",
			component: Login,
		},
	],
});

// router.beforeEach(async (to) => {})

export default router;
