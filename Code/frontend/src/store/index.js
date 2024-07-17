import { createStore } from "vuex";
import axios from "axios";
import router from "@/router";

const store = createStore({
	state() {
		return {
			accessToken: localStorage.getItem("accessToken"),
			user: JSON.parse(localStorage.getItem("user")),
		};
	},
	mutations: {
		logout(state) {
			localStorage.clear();
			state.accessToken = null;
			state.user = null;
			router.go();
		},

		loginHandler(state, data) {
			state.accessToken = data.access_token;
			state.user = data.user;
			localStorage.setItem("accessToken", data.access_token);
			localStorage.setItem("user", JSON.stringify(data.user));
		},

		getUserData(state, user) {
			state.user = user;
			localStorage.setItem("user", JSON.stringify(user));
		},
	},
	actions: {
		async loginHandler({ commit }, login_details) {
			const path = "http://127.0.0.1:5000/login";
			return axios
				.post(path, login_details)
				.then((response) => {
					commit("loginHandler", response.data);
					return response;
				})
				.catch((response) => {
					return response.response;
				});
		},

		async registerHandler({ commit }, register_details) {
			const path = "http://127.0.0.1:5000/register";
			return axios
				.post(path, register_details)
				.then((response) => {
					commit("loginHandler", response.data);
					return response.status;
				})
				.catch((response) => {
					return response;
				});
		},

		getUserData({ commit }, access_token) {
			if (access_token == null) return "Not Logged In!";
			const path = "http://127.0.0.1:5000/get-user-data";
			return axios
				.get(path, {
					headers: {
						Authorization: `Bearer ${access_token}`,
					},
				})
				.then((response) => {
					commit("getUserData", response.data);
					return "Successfully Received the Data!";
				})
				.catch((response) => {
					return `Received the following error: ${response.response.data}`;
				});
		},
	},
	getters: {
		isLoggedIn(state) {
			return state.accessToken ? true : false;
		},
	},
});

export default store;
