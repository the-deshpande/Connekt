<script setup>
import store from "@/store";
import axios from "axios";
import { ref, reactive } from "vue";

let editMode = ref(false);

let user = reactive(store.state.user);

async function updateProfile() {
	const path = "http://127.0.0.1:5000/get-user-data";
	var response = await axios
		.put(path, this.user, {
			headers: {
				Authorization: `Bearer ${store.state.accessToken}`,
			},
		})
		.then((response) => {
			store.dispatch("getUserData", store.state.accessToken);
			return response;
		})
		.catch((response) => {
			return response.response;
		});

	console.log(response);
	this.editMode = false;
}

async function deleteUser() {
	if (confirm("Are you sure?")) {
		const path = "http://127.0.0.1:5000/get-user-data";
		var response = await axios
			.delete(path, {
				headers: {
					Authorization: `Bearer ${store.state.accessToken}`,
				},
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
			store.commit("logout");
		}
	}
}
</script>

<template>
	<div class="modal-wrapper" aria-modal="true" role="dialog" tabindex="-1">
		<div class="inner text-white" v-if="!editMode">
			<h2 class="text-green">Profile</h2>
			<button class="close-btn" @click="$emit('closePopup')">
				<i class="bi bi-x-lg text-white"></i>
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
			<div class="row">
				<button class="btn col" @click="store.commit('logout')">
					<i class="bi fs-4 bi-box-arrow-left text-success"></i>
				</button>
				<button class="btn col" @click="editMode = true">
					<i class="bi fs-4 bi-pencil text-warning"></i>
				</button>
				<button class="btn col" @click="deleteUser()">
					<i class="bi fs-4 bi-trash text-danger"></i>
				</button>
			</div>
		</div>
		<div class="inner text-white" v-else>
			<button class="close-btn" @click="$emit('closePopup')">
				<i class="bi bi-x-lg text-white"></i>
			</button>
			<div class="row my-2">
				<label for="first-name" class="col-3 form-label">First Name: </label>
				<input
					type="text"
					id="first-name"
					class="col form-control"
					v-model="user.first_name" />
			</div>

			<div class="row my-2">
				<label for="last-name" class="col-3 form-label">Last Name: </label>
				<input
					type="text"
					id="last-name"
					class="col form-control"
					v-model="user.last_name" />
			</div>

			<div class="row my-2" v-if="user.sponsor">
				<label for="industry" class="col-3 form-label">Industry: </label>
				<select
					class="col form-select"
					id="industry"
					v-model="user.sponsor.industry">
					<option>Healthcare</option>
					<option>Gaming</option>
					<option>Tech</option>
					<option>Vlog</option>
				</select>
			</div>

			<div class="row my-2" v-if="user.sponsor">
				<label for="company" class="col-3 form-label">Company: </label>
				<input
					type="text"
					id="company"
					class="col form-control"
					v-model="user.sponsor.company" />
			</div>

			<div class="row my-2" v-if="user.sponsor">
				<label for="budget" class="col-3 form-label">Budget: </label>
				<input
					type="number"
					id="budget"
					class="col form-control"
					v-model="user.sponsor.budget" />
			</div>

			<div class="row my-2" v-if="user.influencer">
				<label for="platform" class="col-3 form-label">Platform: </label>
				<input
					type="text"
					id="platform"
					class="col form-control"
					v-model="user.influencer.platform" />
			</div>

			<div class="row my-2" v-if="user.influencer">
				<label for="niche" class="col-3 form-label">Niche: </label>
				<select
					class="col form-select"
					id="niche"
					v-model="user.influencer.niche">
					<option>Healthcare</option>
					<option>Gaming</option>
					<option>Tech</option>
					<option>Vlog</option>
				</select>
			</div>

			<div class="row my-2" v-if="user.influencer">
				<label for="reach" class="col-3 form-label">Reach: </label>
				<input
					type="number"
					id="reach"
					class="col form-control"
					v-model="user.influencer.reach" />
			</div>

			<div class="row">
				<div class="col"></div>
				<button @click="updateProfile()" class="btn col btn-green text-white">
					Make Changes
				</button>
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
		background-color: #758694;
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

		.text-green {
			color: #9cdba6;
		}
	}
}
</style>
