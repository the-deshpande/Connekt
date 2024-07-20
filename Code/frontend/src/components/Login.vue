<script setup>
import { reactive } from "vue";
import router from "@/router";
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
	cnfPassword: "",
	email: "",
	type: 0,
});

let influencerRegister = reactive({
	platform: "",
	reach: 0,
	niche: "",
});

let sponsorRegister = reactive({
	company: "",
	industry: "",
	budget: 0,
});

async function registerHandler() {
	var re = /\S+@\S+\.\S+/;
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
	if (registerDetails.cnfPassword != registerDetails.password) {
		alert("Passwords don't match!");
		return;
	}
	if (!re.test(registerDetails.email)) {
		alert("Enter correct Email ID");
		return;
	}

	if (
		registerDetails.type == 1 &&
		(influencerRegister.niche == "" ||
			influencerRegister.platform == "" ||
			influencerRegister.reach == 0)
	) {
		alert("Kindly fill all fields");
		return;
	}

	if (
		registerDetails.type == 2 &&
		(sponsorRegister.industry == "" ||
			sponsorRegister.company == "" ||
			sponsorRegister.budget == 0)
	) {
		alert("Kindly fill all fields");
		return;
	}

	let response;
	if (registerDetails.type == 1) {
		response = await store.dispatch("registerHandler", [
			registerDetails,
			influencerRegister,
		]);
	} else {
		response = await store.dispatch("registerHandler", [
			registerDetails,
			sponsorRegister,
		]);
	}
	registerDetails.email = "";
	registerDetails.password = "";
	registerDetails.first_name = "";
	registerDetails.last_name = "";
	registerDetails.type = 0;

	influencerRegister.niche = "";
	influencerRegister.platform = "";
	influencerRegister.reach = 0;

	sponsorRegister.industry = "";
	sponsorRegister.company = "";
	sponsorRegister.budget = 0;

	if (response.status == 200 || response.status == 201) {
		router.push("/");
	} else {
		alert(response);
	}
}

async function loginHandler() {
	if (loginDetails.email == "" || loginDetails.password == "") {
		alert("Kindly fill all fields");
		return;
	}
	let response = await store.dispatch("loginHandler", loginDetails);

	loginDetails.email = "";
	loginDetails.password = "";

	if (response.status == 200) {
		router.push("/");
	} else {
		alert(response.data.message);
	}
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
								class="btn btn-green text-white fs-4"
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
								<label class="form-label text-white fs-4">Confirm</label>
							</div>
							<div class="col-9">
								<input
									class="form-control"
									type="password"
									v-model="registerDetails.cnfPassword" />
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
									<option value="1">Influencer</option>
									<option value="2">Sponsor</option>
								</select>
							</div>
						</div>

						<div v-if="registerDetails.type == 1">
							<div class="row my-4">
								<div class="col-3">
									<label class="form-label text-white fs-4" for="platform"
										>Platform</label
									>
								</div>
								<div class="col-9">
									<select
										class="form-select"
										id="platform"
										v-model="influencerRegister.platform">
										<option>Instagram</option>
										<option>Youtube</option>
										<option>Tiktok</option>
										<option>Twitter (X)</option>
									</select>
								</div>
							</div>
							<div class="row my-4">
								<div class="col-3">
									<label class="form-label text-white fs-4" for="niche"
										>Niche</label
									>
								</div>
								<div class="col-9">
									<select
										class="form-select"
										id="niche"
										v-model="influencerRegister.niche">
										<option>Healthcare</option>
										<option>Gaming</option>
										<option>Tech</option>
										<option>Vlog</option>
									</select>
								</div>
							</div>
							<div class="row my-4">
								<div class="col-3">
									<label class="form-label text-white fs-4" for="reach"
										>Reach</label
									>
								</div>
								<div class="col-9">
									<input
										class="form-select"
										id="reach"
										v-model="influencerRegister.reach"
										type="number" />
								</div>
							</div>
						</div>

						<div v-if="registerDetails.type == 2">
							<div class="row my-4">
								<div class="col-3">
									<label class="form-label text-white fs-4" for="company"
										>Company</label
									>
								</div>
								<div class="col-9">
									<input
										class="form-select"
										id="company"
										v-model="sponsorRegister.company"
										type="text" />
								</div>
							</div>
							<div class="row my-4">
								<div class="col-3">
									<label class="form-label text-white fs-4" for="industry"
										>Industry</label
									>
								</div>
								<div class="col-9">
									<select
										class="form-select"
										id="industry"
										v-model="sponsorRegister.industry">
										<option>Healthcare</option>
										<option>Gaming</option>
										<option>Tech</option>
										<option>Vlog</option>
									</select>
								</div>
							</div>
							<div class="row my-4">
								<div class="col-3">
									<label class="form-label text-white fs-4" for="budget"
										>Budget</label
									>
								</div>
								<div class="col-9">
									<input
										class="form-select"
										id="budget"
										v-model="sponsorRegister.budget"
										type="number" />
								</div>
							</div>
						</div>

						<div class="row my-4">
							<input
								type="button"
								class="btn btn-green fs-4 text-white"
								value="Register"
								@click="registerHandler()" />
						</div>
					</form>
				</div>
				<div v-else>
					<p class="text-white fs-1 text-center">You are Good to Go!</p>
				</div>
			</div>
		</div>
	</main>
</template>

<style lang="scss" scoped>
.container {
	min-height: 70vh;
}
.page-link.active {
	border-color: #9cdba6;
	border-width: 2px;
}
.btn-green {
	background-color: rgba(70, 133, 133, 1);
}
.btn-green:hover {
	background-color: rgba(70, 133, 133, 0.8);
}
</style>
