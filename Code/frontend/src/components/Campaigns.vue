<script setup>
import store from "@/store";
import axios from "axios";
import { ref, reactive } from "vue";
import ModalWindow from "./modal/CampaignModal.vue";
import AddItemModal from "./modal/AddItemModal.vue";

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
const campaigns = response.data.campaigns;
</script>

<template>
	<div class="container mb-5" v-if="store.state.user.type == 2">
		<div class="row">
			<div class="col-5"></div>
			<button class="col btn btn-green text-white" @click="createCampaign()">
				Add Campaign
			</button>
			<div class="col-5"></div>
		</div>
	</div>
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
div button.bg-gray {
	background-color: #758694;
}
div button.bg-gray:hover {
	background-color: #405d72;
}
.btn-green {
	background-color: #468585;
}
</style>
