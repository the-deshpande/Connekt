<script setup>
import store from "@/store";
import router from "@/router";
import UserModalWindow from "./UserModal.vue";
import CampaignModalWindow from "./CampaignModal.vue";
import { ref, reactive } from "vue";
import axios from "axios";

let userModalActive = ref(false);
let campaignModalActive = ref(false);
let detail = reactive({});

function openUserModal(details) {
	this.detail = details;
	this.userModalActive = true;
}
function openCampaignModal(details) {
	this.detail = details;
	this.campaignModalActive = true;
}

async function deleteContract(contract_id) {
	if (confirm("Are you sure?")) {
		const path = "http://127.0.0.1:5000/contract";
		var response = await axios
			.delete(path, {
				headers: {
					Authorization: `Bearer ${store.state.accessToken}`,
				},
				data: {
					contract_id: contract_id,
				},
			})
			.then((response) => response)
			.catch((response) => response.response);

		if (response.status == 202) {
			router.go();
		} else {
			alert(response.data.message);
		}
		console.log(response);
	}
}

var editMode = ref(false);
async function updateContract() {
	if (this.contract.requirements == "" || this.contract.payment_amount == 0) {
		alert("Please enter all details correctly!");
		return;
	}
	const path = "http://127.0.0.1:5000/contract";
	var response = await axios
		.put(path, this.contract, {
			headers: {
				Authorization: `Bearer ${store.state.accessToken}`,
			},
		})
		.then((response) => {
			store.dispatch("getUserData", store.state.accessToken);
			if (store.state.user.influencer) this.contract.status = 1;
			else this.contract.status = 2;
			return response;
		})
		.catch((response) => {
			return response.response;
		});

	console.log(response);
	this.editMode = false;
}

async function updateStatus(approved) {
	if (approved) this.contract.status = 3;
	else this.contract.status = 0;

	const path = "http://127.0.0.1:5000/contract";
	var response = await axios
		.put(path, this.contract, {
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

defineEmits(["closePopup"]);
var contract = defineProps(["contract"]);
contract = ref(contract.contract);
</script>

<template>
	<div class="modal-wrapper" aria-modal="true" role="dialog" tabindex="-1">
		<div class="inner text-white" v-if="!editMode">
			<h2 class="text-green">Contract Details</h2>
			<button class="close-btn" @click="$emit('closePopup')">
				<i class="bi bi-x-lg text-white"></i>
			</button>
			<div class="row">
				<div>
					<span class="fw-bold">Requirements: </span>
					{{ contract.requirements }}
				</div>
				<div @click="openUserModal(contract.influencer)" class="link">
					<span class="fw-bold">Influencer:</span>
					{{ contract.influencer.first_name }}
					{{ contract.influencer.last_name }}
				</div>
				<div @click="openCampaignModal(contract.campaign)" class="link">
					<span class="fw-bold">Campaign:</span>
					{{ contract.campaign.name }}
				</div>
				<div>
					<span class="fw-bold">Payment Amount: </span>
					{{ contract.payment_amount }}
				</div>
				<div class="row">
					<button
						@click="updateStatus(false)"
						class="btn col"
						v-if="
							(contract.influencer.id == store.state.user.id &&
								contract.status == 2) ||
							(contract.campaign.sponsor.id == store.state.user.id &&
								contract.status == 1)
						">
						<i class="bi fs-4 bi-ban text-danger"></i>
					</button>
					<button
						@click="updateStatus(true)"
						class="btn col"
						v-if="
							(contract.influencer.id == store.state.user.id &&
								contract.status == 2) ||
							(contract.campaign.sponsor.id == store.state.user.id &&
								contract.status == 1)
						">
						<i class="fs-4 bi bi-check2-circle text-success"></i>
					</button>
					<button
						@click="editMode = true"
						class="btn col"
						v-if="
							store.state.user.type == 0 ||
							(contract.influencer.id == store.state.user.id &&
								contract.status == 2) ||
							(contract.campaign.sponsor.id == store.state.user.id &&
								contract.status == 1)
						">
						<i class="bi fs-4 bi-pencil text-warning"></i>
					</button>
					<button
						@click="deleteContract(contract.id)"
						class="btn col"
						v-if="
							store.state.user.type == 0 ||
							contract.influencer.id == store.state.user.id ||
							contract.campaign.sponsor.id == store.state.user.id
						">
						<i class="bi fs-4 bi-trash-fill text-danger"></i>
					</button>
				</div>
			</div>
		</div>
		<div class="inner text-white" v-else>
			<button class="close-btn" @click="$emit('closePopup')">
				<i class="bi bi-x-lg text-white"></i>
			</button>
			<div class="row my-2">
				<label for="requirements" class="col-3 form-label"
					>Requirements:
				</label>
				<input
					type="text"
					id="requirements"
					class="col form-control"
					v-model="contract.requirements" />
			</div>

			<div class="row my-2">
				<label for="payment-amount" class="col-3 form-label"
					>Payment Amount:
				</label>
				<input
					type="number"
					id="payment-amount"
					class="col form-control"
					v-model="contract.payment_amount" />
			</div>

			<div class="row">
				<div class="col"></div>
				<button @click="updateContract()" class="btn col btn-green text-white">
					Make Changes
				</button>
				<div class="col"></div>
			</div>
		</div>
	</div>
	<CampaignModalWindow
		v-if="campaignModalActive"
		@closePopup="campaignModalActive = false"
		:campaign="detail"></CampaignModalWindow>
	<UserModalWindow
		v-if="userModalActive"
		@closePopup="userModalActive = false"
		:user="detail"></UserModalWindow>
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

		.link:hover {
			color: #9cdba6;
			cursor: pointer;
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
