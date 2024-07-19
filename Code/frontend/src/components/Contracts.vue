<script setup>
import store from "@/store";
import { ref, reactive } from "vue";
import ModalWindow from "./modal/ContractModal.vue";
import AddItemModal from "./modal/AddItemModal.vue";

let modalActive = ref(false);
let detail = reactive({});
function openModal(details) {
	this.detail = details;
	this.modalActive = true;
}
let addItem = ref(false);
let item = reactive({});
function createContract() {
	this.item.item = 1;
	this.addItem = true;
}

const response = await store.dispatch(
	"getContractList",
	store.state.accessToken
);
const contracts = response.data.contracts;
</script>

<template>
	<div class="container mb-5" v-if="store.state.user.type != 0">
		<div class="row">
			<div class="col-5"></div>
			<button class="col btn btn-green text-white" @click="createContract()">
				Add Contract
			</button>
			<div class="col-5"></div>
		</div>
	</div>
	<div class="container">
		<div v-if="contracts.length == 0" class="text-white fs-1 text-center">
			Uh Oh! Seems like there are no contracts.
		</div>
		<div class="list-group py-1 text-white" v-for="contract in contracts">
			<button
				class="list-group-item text-white list-group-item-action bg-gray"
				@click="openModal(contract)">
				<div class="d-flex w-100 justify-content-between">
					<h5 class="mb-1 text-green">{{ contract.requirements }}</h5>
					<small>
						<i
							class="bi bi-ban text-danger fs-3"
							v-if="contract.status == 0"></i>
						<i
							class="bi bi-check-lg text-success fs-3"
							v-else-if="contract.status == 3"></i>
						<i
							class="bi bi-send text-info fs-3"
							v-else-if="
								(store.state.user.influencer && contract.status == 1) ||
								(store.state.user.sponsor && contract.status == 2)
							"></i>
						<i class="bi bi-clock text-info fs-3" v-else></i>
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
	background-color: #468585;
}
.btn-green {
	background-color: #468585;
}
.text-green {
	color: #9cdba6;
}
</style>
