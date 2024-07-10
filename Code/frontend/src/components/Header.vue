<script setup>
import { RouterLink } from "vue-router";
import store from "@/store";
</script>

<template>
	<header
		class="d-flex text-white flex-wrap justify-content-center py-3 mb-4 border-bottom">
		<a
			href="/"
			class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none px-3">
			<img alt="Connekt Logo" class="filter-green" src="../assets/logo.svg" />
			<span class="fs-3 px-3 text-green">Connekt</span>
		</a>

		<ul class="nav nav-pills">
			<li class="nav-item mx-1">
				<router-link to="/" custom v-slot="{ href, navigate, isActive }">
					<button
						:class="{ active: isActive }"
						:href="href"
						@click="navigate"
						class="nav-link text-white">
						Home
					</button>
				</router-link>
			</li>
			<li class="nav-item mx-1">
				<router-link to="/ping" custom v-slot="{ href, navigate, isActive }">
					<button
						:class="{ active: isActive }"
						:href="href"
						@click="navigate"
						class="nav-link text-white">
						Ping
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
				<button
					@click="store.commit('logout')"
					class="nav-link text-white active">
					Logout
				</button>
			</li>
		</ul>
	</header>
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
