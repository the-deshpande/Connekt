<script setup>
import store from "@/store";
</script>

<template>
	<div class="modal-wrapper" aria-modal="true" role="dialog" tabindex="-1">
		<div class="inner">
			<button class="close-btn" @click="$emit('closePopup')">
				<i class="bi bi-x-lg"></i>
			</button>

			<div class="row">
				<div>
					<span class="fw-bold">Name:</span>
					{{ store.state.user.first_name }} {{ store.state.user.last_name }}
				</div>
				<div>
					<span class="fw-bold">Email:</span> {{ store.state.user.email }}
				</div>
				<div v-if="store.state.user.influencer">
					<div>
						<span class="fw-bold">Type:</span>
						Influencer
					</div>
					<div>
						<span class="fw-bold">Niche:</span>
						{{ store.state.user.influencer.niche }}
					</div>
					<div>
						<span class="fw-bold">Platform:</span>
						{{ store.state.user.influencer.platform }}
					</div>
					<div>
						<span class="fw-bold">Reach:</span>
						{{ store.state.user.influencer.reach }}
					</div>
				</div>
				<div v-else-if="store.state.user.sponsor">
					<div>
						<span class="fw-bold">Type:</span>
						Sponsor
					</div>
					<div>
						<span class="fw-bold">Company:</span>
						{{ store.state.user.sponsor.company }}
					</div>
					<div>
						<span class="fw-bold">Industry:</span>
						{{ store.state.user.sponsor.industry }}
					</div>
					<div>
						<span class="fw-bold">Budget:</span>
						{{ store.state.user.sponsor.budget }}
					</div>
				</div>
			</div>
			<div class="row">
				<button class="btn col" @click="store.commit('logout')">
					<i class="bi bi-box-arrow-left text-success"></i>
				</button>
				<button class="btn col">
					<i class="bi bi-pencil text-warning"></i>
				</button>
				<button class="btn col">
					<i class="bi bi-trash text-danger"></i>
				</button>
			</div>
		</div>
	</div>
</template>

<style lang="scss" scoped>
.modal-wrapper {
	position: fixed;
	left: 0;
	top: 0;
	z-index: 500;
	width: 100vw;
	height: 100vh;
	background: rgba(0, 0, 0, 0.2);
	display: grid;
	place-items: center;
	color: var(--black-color);

	.inner {
		background-color: white;
		padding: 30px;
		border-radius: 12px;
		display: flex;
		flex-direction: column;
		position: relative;
		max-width: 600px;
		width: 90%;

		h3 {
			font-size: 16px;
			font-weight: 700;
			line-height: 21px;
			margin-bottom: 20px;
		}

		.close-btn {
			position: absolute;
			top: 15px;
			right: 15px;
			cursor: pointer;
			background-color: var(--white-color);
			border-width: 0;
		}
	}
}
</style>
