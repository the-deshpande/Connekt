<script setup>
import store from "@/store";
import UserModalWindow from "./UserModal.vue";
import CampaignModalWindow from "./CampaignModal.vue";
import { ref } from "vue";

let userModalActive = ref(false);
let campaignModalActive = ref(false);
let detail = ref({});

function openUserModal(details) {
	this.detail = details;
	this.userModalActive = true;
}
function openCampaignModal(details) {
	console.log("Hello");
	this.detail = details;
	this.campaignModalActive = true;
}

var contract = defineProps(["contract"]);
contract = contract.contract;
</script>

<template>
	<div class="modal-wrapper" aria-modal="true" role="dialog" tabindex="-1">
		<div class="inner">
			<h2>Contract Details</h2>
			<button class="close-btn" @click="$emit('closePopup')">
				<i class="bi bi-x-lg"></i>
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
						class="btn col"
						v-if="
							store.state.user.type == 0 ||
							contract.influencer.id == store.state.user.id ||
							contract.campaign.sponsor.id == store.state.user.id
						">
						<i class="bi bi-trash-fill text-danger"></i>
					</button>
					<button
						class="btn col"
						v-if="
							store.state.user.type == 0 ||
							(contract.influencer.id == store.state.user.id &&
								contract.status == 2) ||
							(contract.campaign.sponsor.id == store.state.user.id &&
								contract.status == 1)
						">
						<i class="bi bi-pencil text-warning"></i>
					</button>
				</div>
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

		.link:hover {
			color: darkcyan;
		}
	}
}
</style>
