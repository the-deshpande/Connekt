import { createStore } from "vuex";
import axios from "axios";

const store = createStore({
	state() {
		return {
			accessToken: localStorage.getItem("accessToken"),
			user: {},
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
		},
	},
	actions: {
		loginHandler({ commit }, login_details) {
			const path = "http://127.0.0.1:5000/login";
			axios.post(path, login_details).then((response) => {
				commit("loginHandler", response.data.access_token);
			});
		},

		registerHandler({ commit }, register_details) {
			const path = "http://127.0.0.1:5000/register";
			axios.post(path, register_details).then((response) => {
				commit("loginHanfler", response.data.access_token);
			});
		},

		getUserData({ commit }, access_token) {
			const path = "http://127.0.0.1:5000/get-user-data";
			axios
				.get(path, {
					headers: {
						Authorization: `Bearer ${access_token}`,
					},
				})
				.then((response) => {
					commit("getUserData", response.data);
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
