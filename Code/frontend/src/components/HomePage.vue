<script setup>
import store from "@/store";
import axios from "axios";
import { ref, reactive } from "vue";
import ActiveUsers from "./charts/ActiveUsers.vue";
import NichexIndustry from "./charts/NichexIndustry.vue";
import ContractxPlatform from "./charts/ContractxPlatform.vue";
import BudgetxIndustry from "./charts/BudgetxIndustry.vue";

let pageNumber = ref(0);

let stats;
if (store.getters.isLoggedIn && store.state.user.type == 0) {
	const path = "http://127.0.0.1:5000/tasks/dashboard";
	var response = await axios
		.get(path, {
			headers: {
				Authorization: `Bearer ${store.state.accessToken}`,
			},
		})
		.then((response) => response)
		.catch((response) => response.response);

	console.log(response);
	if (response.status == 200) stats = reactive(response.data);
	else stats = reactive({ data: "No Data Collected" });
}
</script>
<template>
	<div
		class="container text-white"
		v-if="store.getters.isLoggedIn && store.state.user.type == 0">
		<div class="row align-items-center main-body">
			<div class="d-flex justify-content-center" style="height: 336px">
				<button
					:disabled="pageNumber <= 0"
					@click="pageNumber--"
					class="btn mx-5">
					<i class="bi fs-4 bi-chevron-left text-white"></i>
				</button>
				<NichexIndustry v-if="pageNumber == 0" :data="stats.NichexIndustry" />
				<ActiveUsers v-if="pageNumber == 1" :data="stats.ActiveUsers" />
				<ContractxPlatform
					v-if="pageNumber == 2"
					:data="stats.ContractxPlatform" />
				<BudgetxIndustry v-if="pageNumber == 3" :data="stats.BudgetxIndustry" />
				<button
					:disabled="pageNumber >= 3"
					@click="pageNumber++"
					class="btn mx-5">
					<i class="bi fs-4 bi-chevron-right text-white"></i>
				</button>
			</div>
		</div>
	</div>
	<div class="container text-white" v-else>
		<div class="row align-items-center main-body">
			<div class="col-md" v-if="!store.getters.isLoggedIn">
				<h1>Welcome to</h1>
				<h1 class="text-green">Connekt!</h1>
				<p>
					THE place to partner up and
					<span class="text-green">connekt</span> with the wider world!
				</p>
				<router-link to="/login" custom v-slot="{ href, navigate, isActive }">
					<button
						:class="{ active: !isActive }"
						:href="href"
						@click="navigate"
						class="btn text-white">
						Join the World!
					</button>
				</router-link>
			</div>
			<div class="col-md" v-else>
				<h2>
					Hi
					<span class="text-green"
						>{{ store.state.user.first_name }}
						{{ store.state.user.last_name }},</span
					>
				</h2>
				<p>Welcome to the world of grand possibilities!</p>
			</div>
			<div class="col-md">
				<div
					id="carousel"
					class="carousel slide carousel-fade"
					data-bs-ride="carousel">
					<div class="carousel-inner">
						<div class="carousel-item active">
							<img
								src="../assets/homepage-image-1.png"
								class="d-block w-100"
								alt="Visit www.framesters.com" />
						</div>
						<div class="carousel-item">
							<img
								src="../assets/homepage-image-2.png"
								class="d-block w-100"
								alt="Visit www.framesters.com" />
						</div>
						<div class="carousel-item">
							<img
								src="../assets/homepage-image-3.png"
								class="d-block w-100"
								alt="Visit www.framesters.com" />
						</div>
						<div class="carousel-item">
							<img
								src="../assets/homepage-image-4.png"
								class="d-block w-100"
								alt="Visit www.framesters.com" />
						</div>
						<div class="carousel-item">
							<img
								src="../assets/homepage-image-5.png"
								class="d-block w-100"
								alt="Visit www.framesters.com" />
						</div>
					</div>
					<button
						class="carousel-control-prev"
						type="button"
						data-bs-target="#carousel"
						data-bs-slide="prev">
						<span class="carousel-control-prev-icon" aria-hidden="true"></span>
						<span class="visually-hidden">Previous</span>
					</button>
					<button
						class="carousel-control-next"
						type="button"
						data-bs-target="#carousel"
						data-bs-slide="next">
						<span class="carousel-control-next-icon" aria-hidden="true"></span>
						<span class="visually-hidden">Next</span>
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<style lang="scss" scoped>
.main-body {
	min-height: 70vh;
}

.active {
	background-color: #468585;
}

.text-green {
	color: #9cdba6;
}

.btn:hover {
	background-color: rgba(255, 255, 255, 0.1);
}
</style>
