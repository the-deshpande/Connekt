<script setup>
import store from "@/store";
import axios from "axios";
import { ref } from "vue";
import ModalWindow from "./modal/ContractModal.vue";

let modalActive = ref(false);
let detail = ref({});
function openModal(details) {
	this.detail = details;
	this.modalActive = true;
}

async function getContractList() {
	const path = "http://127.0.0.1:5000/contract";
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

const response = await getContractList();
const contracts = response.data.contracts;
</script>

<template>
	<div class="container">
		<div v-if="contracts.length == 0" class="text-white fs-1 text-center">
			Uh Oh! Seems like there are no contracts.
		</div>
		<div class="list-group py-1 text-white" v-for="contract in contracts">
			<button
				class="list-group-item text-white list-group-item-action bg-gray"
				@click="openModal(contract)">
				<div class="d-flex w-100 justify-content-between">
					<h5 class="mb-1">{{ contract.requirements }}</h5>
					<small>
						<i class="bi bi-ban text-danger" v-if="contract.status == 0"></i>
						<i
							class="bi bi-check-lg text-success"
							v-else-if="contract.status == 3"></i>
						<i class="bi bi-clock text-info" v-else></i>
					</small>
				</div>
				<p class="mb-1">
					{{ contract.campaign.name }}
				</p>
				<p class="mb-1">
					{{ contract.influencer.first_name }}
					{{ contract.influencer.last_name }}
				</p>
			</button>
		</div>
	</div>
	<ModalWindow
		v-if="modalActive"
		@closePopup="modalActive = false"
		:contract="detail"></ModalWindow>
</template>
