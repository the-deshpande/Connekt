<script setup>
import store from "@/store";
import axios from "axios";
import router from "@/router";
import { ref, reactive } from "vue";
import AddItemModal from "./AddItemModal.vue";

defineEmits(["closePopup"]);
var user = defineProps(["user"]);
user = reactive(user.user);

let addItem = ref(false);
let item = reactive({});
function createContract() {
	this.item.item = 1;
	this.item.influencer_id = this.user.influencer.id;
	this.addItem = true;
}

async function flagUser(user_id) {
	const path = "http://127.0.0.1:5000/users/flag";
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
		const path = "http://127.0.0.1:5000/users/delete";
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
		<div class="inner text-white">
			<h2 class="text-green">User Details</h2>
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

			<div class="row" v-if="store.state.user.type == 0">
				<button class="btn col" @click="flagUser(user.id)">
					<i
						class="bi fs-4 bi-flag-fill"
						:class="{ 'text-danger': user.flagged }"></i>
				</button>
				<button class="btn col" @click="deleteUser(user.id)">
					<i class="bi fs-4 bi-trash text-danger"></i>
				</button>
			</div>
			<div class="row" v-if="store.state.user.type == 2">
				<div class="col"></div>
				<button @click="createContract()" class="btn btn-green text-white col">
					Create Contract
				</button>
				<div class="col"></div>
			</div>
		</div>
	</div>

	<AddItemModal
		v-if="addItem"
		@closePopup="addItem = false"
		:item="item"></AddItemModal>
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
