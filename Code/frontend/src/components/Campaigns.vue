<script setup>
import store from "@/store";
import { ref, reactive } from "vue";
import ModalWindow from "./modal/CampaignModal.vue";
import AddItemModal from "./modal/AddItemModal.vue";
import axios from "axios";

let modalActive = ref(false);
let detail = reactive({});
function openModal(details) {
	this.detail = details;
	this.modalActive = true;
}
let addItem = ref(false);
let item = reactive({});
function createCampaign() {
	this.item.item = 0;
	this.addItem = true;
}

const response = await store.dispatch(
	"getCampaignsList",
	store.state.accessToken
);

async function exportToCSV() {
	const path = "http://127.0.0.1:5000/tasks/export";
	var response = await axios
		.get(path, {
			headers: {
				Authorization: `Bearer ${store.state.accessToken}`,
			},
		})
		.then((response) => response)
		.catch((response) => response.response);

	if (response.status == 200) {
		alert("The file will be shared on your mail");
	}
	console.log(response);
}

const campaigns = response.data.campaigns;
</script>

<template>
	<div class="container">
		<div class="text-center">
			<button
				class="btn btn-green btn-block text-white mx-3 mb-3"
				v-if="store.state.user.type == 2"
				@click="createCampaign()">
				Add Campaign
			</button>
			<button
				class="btn btn-green btn-block text-white mx-3 mb-3"
				@click="exportToCSV()">
				Export to CSV
			</button>
		</div>
		<div v-if="campaigns.length == 0" class="text-white fs-1 text-center">
			Uh Oh! Seems like there are no campaigns.
		</div>
		<div class="list-group py-1 text-white" v-for="campaign in campaigns">
			<button
				class="list-group-item text-white list-group-item-action bg-gray"
				@click="openModal(campaign)">
				<div class="d-flex w-100 justify-content-between">
					<h5 class="mb-1 text-green">{{ campaign.name }}</h5>
					<small v-if="campaign.approved">
						<i
							class="bi bi-flag-fill fs-3"
							:class="{ 'text-danger': campaign.flagged }"></i
					></small>
					<small v-else> <i class="bi bi-clock text-info fs-3"></i></small>
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
	<AddItemModal
		v-if="addItem"
		@closePopup="addItem = false"
		:item="item"></AddItemModal>
</template>

<style lang="scss" scoped>
.container {
	min-height: 70vh;
}
div button.bg-gray {
	background-color: #758694;
}
div button.bg-gray:hover {
	background-color: #468585;
}
.btn-green {
	background-color: rgba(70, 133, 133, 1);
}
.btn-green:hover {
	background-color: rgba(70, 133, 133, 0.8);
}
.text-green {
	color: #9cdba6;
}
</style>
