<script setup>
import store from "@/store";
import axios from "axios";
import ModalWindow from "./modal/UserModal.vue";
import { ref, reactive } from "vue";

let modalActive = ref(false);
let detail = reactive({});

function openModal(details) {
	this.detail = details;
	this.detail.category = "user";
	this.modalActive = true;
}

const response = await store.dispatch("getUsersList", store.state.accessToken);
const users = response.data.users;
</script>

<template>
	<div class="container">
		<div v-if="users.length == 0" class="text-white fs-1 text-center">
			Uh Oh! Seems like there are no users.
		</div>
		<div class="list-group py-1" v-for="user in users">
			<button
				class="list-group-item text-white list-group-item-action bg-gray"
				@click="openModal(user)">
				<div class="d-flex w-100 justify-content-between">
					<h5 class="mb-1 text-green">
						{{ user.first_name }} {{ user.last_name }}
					</h5>
					<small
						><i
							class="bi bi-flag-fill fs-3"
							:class="{ 'text-danger': user.flagged }"></i
					></small>
				</div>
				<p class="mb-1" v-if="user.type == 0">Admin</p>
				<p class="mb-1" v-else-if="user.type == 1">
					Influencer - {{ user.influencer.niche }}
				</p>
				<p class="mb-1" v-else>Sponsor - {{ user.sponsor.company }}</p>
			</button>
		</div>
	</div>

	<ModalWindow
		v-if="modalActive"
		@closePopup="modalActive = false"
		:user="detail"></ModalWindow>
</template>

<style lang="scss" scoped>
div button.bg-gray {
	background-color: #758694;
}
div button.bg-gray:hover {
	background-color: #468585;
}
.text-green {
	color: #9cdba6;
}
</style>
