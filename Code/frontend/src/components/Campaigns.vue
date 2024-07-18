<script setup>
import store from "@/store";
import axios from "axios";
import { ref } from "vue";
import ModalWindow from "./modal/CampaignModal.vue";

let modalActive = ref(false);
let detail = ref({});
function openModal(details) {
	this.detail = details;
	this.modalActive = true;
}

async function getCampaignsList() {
	const path = "http://127.0.0.1:5000/campaigns";
	return axios
		.get(path, {
			headers: {
				Authorization: `Bearer ${store.state.accessToken}`,
			},
		})
		.then((response) => {
			return response;
		})
		.catch((response) => {
			return response.response;
		});
}

const response = await getCampaignsList();
const campaigns = response.data.campaigns;
</script>

<template>
	<div class="container">
		<div v-if="campaigns.length == 0" class="text-white fs-1 text-center">
			Uh Oh! Seems like there are no campaigns.
		</div>
		<div class="list-group py-1 text-white" v-for="campaign in campaigns">
			<button
				class="list-group-item text-white list-group-item-action bg-gray"
				@click="openModal(campaign)">
				<div class="d-flex w-100 justify-content-between">
					<h5 class="mb-1">{{ campaign.name }}</h5>
					<small v-if="campaign.approved">
						<i
							class="bi bi-flag-fill"
							:class="{ 'text-danger': campaign.flagged }"></i
					></small>
					<small v-else> <i class="bi bi-clock text-info"></i></small>
				</div>
				<p class="mb-1">
					{{ campaign.sponsor.sponsor.company }}
				</p>
				<small>{{ campaign.description }}</small>
			</button>
		</div>
	</div>
	<ModalWindow
		v-if="modalActive"
		@closePopup="modalActive = false"
		:campaign="detail"></ModalWindow>
</template>

<style lang="scss" scoped>
div button.bg-gray {
	background-color: #758694;
}
div button.bg-gray:hover {
	background-color: #405d72;
}
</style>
