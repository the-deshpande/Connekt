<script setup>
import store from "@/store";
</script>
<template>
	<div
		class="container text-white"
		v-if="store.getters.isLoggedIn && store.state.user.type == 0">
		Hi {{ store.state.user.first_name }}
	</div>
	<div class="container text-white" v-else>
		<div class="row align-items-center" style="min-height: 70vh">
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
				<p>Welcome to the grand possibilities!</p>
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
.active {
	background-color: #468585;
}

.text-green {
	color: #9cdba6;
}
</style>
