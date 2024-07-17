import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/components/HomePage.vue";
import Login from "@/components/Login.vue";
import store from "@/store";
import Users from "@/components/Users.vue";
import Campaigns from "@/components/Campaigns.vue";
import Contracts from "@/components/Contracts.vue";

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: "/",
			name: "HomePage",
			component: HomePage,
		},
		{
			path: "/login",
			name: "Login",
			component: Login,
		},
		{
			path: "/users",
			name: "Users",
			component: Users,
		},
		{
			path: "/campaigns",
			name: "Campaigns",
			component: Campaigns,
		},
		{
			path: "/contracts",
			name: "Contracts",
			component: Contracts,
		},
	],
});

router.beforeEach((to, from, next) => {
	const publicPages = ["/login"];
	const authRequired = !publicPages.includes(to.path);

	if (authRequired && !store.getters.isLoggedIn) {
		next("/login");
	} else {
		next();
	}
});

export default router;
