<script setup>
import router from "@/router";
import { onMounted, reactive, computed, onUpdated } from "vue";
import store from "@/store";

let login = true;
let loginDetails = reactive({
	email: "",
	password: "",
});
let registerDetails = reactive({
	first_name: "",
	last_name: "",
	password: "",
	email: "",
	type: 0,
});

function registerHandler() {
	if (
		registerDetails.email == "" ||
		registerDetails.password == "" ||
		registerDetails.first_name == "" ||
		registerDetails.last_name == "" ||
		registerDetails.type == 0
	) {
		alert("Kindly fill all fields");
		return;
	}

	store.dispatch("registerHandler", registerDetails);
	registerDetails.email = "";
	registerDetails.password = "";
	registerDetails.first_name = "";
	registerDetails.last_name = "";
	registerDetails.type = 0;
}

function loginHandler() {
	if (loginDetails.email == "" || loginDetails.password == "") {
		alert("Kindly fill all fields");
		return;
	}
	store.dispatch("loginHandler", loginDetails);
	loginDetails.email = "";
	loginDetails.password = "";
}
</script>
<template>
	<main class="mb-4 container">
		<div class="row text-white">
			<div class="col-lg-8 col-md-10 mx-auto">
				<div v-if="!store.getters.isLoggedIn">
					<ul class="pagination justify-content-center">
						<li class="page-item">
							<a
								class="page-link text-white bg-dark"
								href="#"
								:class="{ active: login }"
								@click="login = true">
								Login
							</a>
						</li>
						<li class="page-item">
							<a
								class="page-link text-white bg-dark"
								href="#"
								:class="{ active: !login }"
								@click="login = false">
								Register
							</a>
						</li>
					</ul>

					<form v-if="login">
						<div class="row my-4">
							<div class="col-3">
								<label class="form-label text-white fs-4">Email</label>
							</div>
							<div class="col-9">
								<input
									class="form-control"
									type="email"
									v-model="loginDetails.email" />
							</div>
						</div>
						<div class="row my-4">
							<div class="col-3">
								<label class="form-label text-white fs-4">Password</label>
							</div>
							<div class="col-9">
								<input
									class="form-control"
									type="password"
									v-model="loginDetails.password" />
							</div>
						</div>
						<div class="row my-4">
							<input
								type="button"
								class="btn btn-secondary fs-4"
								value="Login"
								@click="loginHandler()" />
						</div>
					</form>

					<form v-else>
						<div class="row my-4">
							<div class="col-3">
								<label class="form-label text-white fs-4">First Name</label>
							</div>
							<div class="col-9">
								<input
									class="form-control"
									type="text"
									v-model="registerDetails.first_name" />
							</div>
						</div>

						<div class="row my-4">
							<div class="col-3">
								<label class="form-label text-white fs-4">Last Name</label>
							</div>
							<div class="col-9">
								<input
									class="form-control"
									type="text"
									v-model="registerDetails.last_name" />
							</div>
						</div>

						<div class="row my-4">
							<div class="col-3">
								<label class="form-label text-white fs-4">Email</label>
							</div>
							<div class="col-9">
								<input
									class="form-control"
									type="email"
									v-model="registerDetails.email" />
							</div>
						</div>

						<div class="row my-4">
							<div class="col-3">
								<label class="form-label text-white fs-4">Password</label>
							</div>
							<div class="col-9">
								<input
									class="form-control"
									type="password"
									v-model="registerDetails.password" />
							</div>
						</div>

						<div class="row my-4">
							<div class="col-3">
								<label class="form-label text-white fs-4" for="user-type"
									>Type</label
								>
							</div>
							<div class="col-9">
								<select
									class="form-select"
									id="user-type"
									v-model="registerDetails.type">
									<!-- <option selected>Choose...</option> -->
									<option value="1">Influencer</option>
									<option value="2">Sponsor</option>
								</select>
							</div>
						</div>

						<div class="row my-4">
							<input
								type="button"
								class="btn btn-secondary fs-4"
								value="Register"
								@click="registerHandler()" />
						</div>
					</form>
				</div>
				<div v-else>
					<p class="text-white fs-1 text-center">You are already logged in!</p>
				</div>
			</div>
		</div>
	</main>
</template>

<style lang="scss" scoped>
.page-link.active {
	border-color: #9cdba6;
	border-width: 2px;
}
</style>
