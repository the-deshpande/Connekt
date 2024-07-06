const app = {
	data() {
		return { greeting: "Hello from Vue!" };
	},
	delimiters: ["[[", "]]"],
};

Vue.createApp(app).mount("#hello");
