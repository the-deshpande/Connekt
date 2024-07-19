<script setup>
import { RouterLink } from "vue-router";
import store from "@/store";
import { ref } from "vue";
import ModalWindow from "./modal/ProfileModal.vue";

let modalActive = ref(false);
</script>

<template>
	<header
		class="d-flex text-white flex-wrap justify-content-center py-3 mb-4 border-bottom">
		<router-link to="/" custom v-slot="{ href, navigate }">
			<button
				:href="href"
				@click="navigate"
				class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none px-3 nav-link">
				<img alt="Connekt Logo" class="filter-green" src="../assets/logo.svg" />
				<span class="fs-3 px-3 text-green">Connekt</span>
			</button>
		</router-link>

		<ul class="nav nav-pills">
			<li
				class="nav-item mx-1"
				v-if="
					store.getters.isLoggedIn &&
					store.state.user &&
					(store.state.user.type == 0 || store.state.user.type == 2)
				">
				<router-link to="/users" custom v-slot="{ href, navigate, isActive }">
					<button
						:class="{ active: isActive }"
						:href="href"
						@click="navigate"
						class="nav-link text-white">
						Users
					</button>
				</router-link>
			</li>
			<li class="nav-item mx-1" v-if="store.getters.isLoggedIn">
				<router-link
					to="/campaigns"
					custom
					v-slot="{ href, navigate, isActive }">
					<button
						:class="{ active: isActive }"
						:href="href"
						@click="navigate"
						class="nav-link text-white">
						Campaigns
					</button>
				</router-link>
			</li>
			<li class="nav-item mx-1" v-if="store.getters.isLoggedIn">
				<router-link
					to="/contracts"
					custom
					v-slot="{ href, navigate, isActive }">
					<button
						:class="{ active: isActive }"
						:href="href"
						@click="navigate"
						class="nav-link text-white">
						Contracts
					</button>
				</router-link>
			</li>
			<li class="nav-item mx-1 me-3" v-if="!store.getters.isLoggedIn">
				<router-link to="/login" custom v-slot="{ href, navigate, isActive }">
					<button
						:class="{ active: isActive }"
						:href="href"
						@click="navigate"
						class="nav-link text-white">
						Login
					</button>
				</router-link>
			</li>

			<li class="nav-item mx-1 me-3" v-else>
				<button @click="modalActive = true" class="nav-link text-white active">
					Profile
				</button>
			</li>
		</ul>
	</header>

	<ModalWindow
		v-if="modalActive"
		@closePopup="modalActive = false"></ModalWindow>
</template>

<style lang="scss" scoped>
.nav-link.active {
	background-color: #468585;
}

.text-green {
	color: #9cdba6;
}

.filter-green {
	filter: invert(92%) sepia(11%) saturate(1094%) hue-rotate(68deg)
		brightness(90%) contrast(90%);
}
</style>
