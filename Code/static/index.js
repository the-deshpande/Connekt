var login_page = {
	login: true,
	login_details: {
		username: "",
		password: "",
	},
	register_details: {
		first_name: "",
		last_name: "",
		password: "",
		username: "",
		email: "",
		type: 0,
	},
};
const app = {
	data() {
		return {
			user: {},
			loggedIn: false,
			login_page: window.login_page,
		};
	},
	methods: {
		getAdminData: function () {
			axios.get("http://127.0.0.1:5000/loggedin").then((response) => {
				this.loggedIn = response.data;
			});
		},
		loginHandler: function () {
			console.log(login_page.login_details);
			if (
				login_page.login_details.username != "" &&
				login_page.login_details.password != ""
			) {
				axios
					.post("http://127.0.0.1:5000/login", this.login_page.login_details)
					.then((response) => {
						console.log(response);
						if (response.data) {
							this.getAdminData();
							window.location.href = "http://127.0.0.1:5000";
						}
					});
			}
		},
		logout: function () {
			if (!this.loggedIn) {
				alert("You are not Logged In!");
			} else {
				axios.get("https://127.0.0.1:5000/logout").then((response) => {
					console.log(response);
					if (response.data) {
						this.loggedIn = false;
						window.location.href = "http://127.0.0.1:5000/login";
					}
				});
			}
		},
	},
	created() {
		this.getAdminData();
	},
	delimiters: ["[[", "]]"],
};

Vue.createApp(app).mount("#app");
