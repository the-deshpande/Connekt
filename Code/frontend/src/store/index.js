import { createStore } from "vuex";
import axios from "axios";

const store = createStore({
	state() {
		return {
			accessToken: localStorage.getItem("accessToken"),
			user: JSON.parse(localStorage.getItem("userDetails")),
		};
	},
	mutations: {
		logout(state) {
			localStorage.clear();
			state.accessToken = "";
			state.user = {};
		},

		loginHandler(state, access_token) {
			state.accessToken = access_token;
			localStorage.setItem("accessToken", access_token);
		},

		getUserData(state, user) {
			state.user = user;
			localStorage.setItem("userDetails", JSON.stringify(user));
		},
	},
	actions: {
		loginHandler({ commit }, login_details) {
			const path = "http://127.0.0.1:5000/login";
			return axios
				.post(path, login_details)
				.then((response) => {
					commit("loginHandler", response.data.access_token);
					return response.response.status;
				})
				.catch((response) => {
					return response.response.status;
				});
		},

		registerHandler({ commit }, register_details) {
			const path = "http://127.0.0.1:5000/register";
			return axios
				.post(path, register_details)
				.then((response) => {
					commit("loginHandler", response.data.access_token);
				})
				.catch((response) => {
					alert(response.response.data.message);
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
		userData(state) {
			return state.user;
		},
	},
});

export default store;
