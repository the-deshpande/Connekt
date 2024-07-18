<script setup>
import store from "@/store";
import axios from "axios";
import router from "@/router";
import { ref } from "vue";

defineEmits(["closePopup"]);
var user = defineProps(["user"]);
user = ref(user.user);

async function flagUser(user_id) {
	const path = "http://127.0.0.1:5000/all-users";
	var response = await axios
		.post(
			path,
			{ user_id: user_id },
			{
				headers: {
					Authorization: `Bearer ${store.state.accessToken}`,
				},
			}
		)
		.then((response) => {
			this.user.flagged = !this.user.flagged;
			return response;
		})
		.catch((response) => {
			alert(response.response.data.message);
			return response.response;
		});

	console.log(response);
}

async function deleteUser(user_id) {
	if (confirm("Are you sure?")) {
		const path = "http://127.0.0.1:5000/all-users";
		var response = await axios
			.delete(path, {
				headers: {
					Authorization: `Bearer ${store.state.accessToken}`,
				},
				data: { user_id: user_id },
			})
			.then((response) => {
				return response;
			})
			.catch((response) => {
				alert(response.response.data.message);
				return response.response;
			});
		console.log(response);
		if (response.status == 200) {
			router.go();
		}
	}
}
</script>

<template>
	<div class="modal-wrapper" aria-modal="true" role="dialog" tabindex="-1">
		<div class="inner">
			<h2>User Details</h2>
			<button class="close-btn" @click="$emit('closePopup')">
				<i class="bi bi-x-lg"></i>
			</button>
			<div class="row">
				<div>
					<span class="fw-bold">Name:</span>
					{{ user.first_name }} {{ user.last_name }}
				</div>
				<div><span class="fw-bold">Email:</span> {{ user.email }}</div>
				<div v-if="user.influencer">
					<div>
						<span class="fw-bold">Type:</span>
						Influencer
					</div>
					<div>
						<span class="fw-bold">Niche:</span>
						{{ user.influencer.niche }}
					</div>
					<div>
						<span class="fw-bold">Platform:</span>
						{{ user.influencer.platform }}
					</div>
					<div>
						<span class="fw-bold">Reach:</span>
						{{ user.influencer.reach }}
					</div>
				</div>
				<div v-else-if="user.sponsor">
					<div>
						<span class="fw-bold">Type:</span>
						Sponsor
					</div>
					<div>
						<span class="fw-bold">Company:</span>
						{{ user.sponsor.company }}
					</div>
					<div>
						<span class="fw-bold">Industry:</span>
						{{ user.sponsor.industry }}
					</div>
					<div>
						<span class="fw-bold">Budget:</span>
						{{ user.sponsor.budget }}
					</div>
				</div>
			</div>

			<div class="row" v-if="store.state.user.type == 0">
				<button class="btn col" @click="flagUser(user.id)">
					<i
						class="bi bi-flag-fill"
						:class="{ 'text-danger': user.flagged }"></i>
				</button>
				<button class="btn col" @click="deleteUser(user.id)">
					<i class="bi bi-trash text-danger"></i>
				</button>
			</div>
			<div class="row" v-if="store.state.user.type == 2">
				<div class="col"></div>
				<button class="btn btn-green text-white col">Create Contract</button>
				<div class="col"></div>
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
		.btn-green {
			background-color: #468585;
		}
	}
}
</style>
