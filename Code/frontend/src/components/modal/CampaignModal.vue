<script setup>
import store from "@/store";
import ModalWindow from "./UserModal.vue";
import { ref } from "vue";

let modalActive = ref(false);
let detail = ref({});

function openModal(details) {
	this.detail = details;
	this.modalActive = true;
}

var campaign = defineProps(["campaign"]);
campaign = campaign.campaign;
</script>

<template>
	<div class="modal-wrapper" aria-modal="true" role="dialog" tabindex="-1">
		<div class="inner">
			<h2>Campaign Modal</h2>
			<button class="close-btn" @click="$emit('closePopup')">
				<i class="bi bi-x-lg"></i>
			</button>
			<div class="row">
				<div>
					<span class="fw-bold">Name:</span>
					{{ campaign.name }}
				</div>
				<div @click="openModal(campaign.sponsor)" class="user">
					<span class="fw-bold">Sponsor:</span>
					{{ campaign.sponsor.first_name }} {{ campaign.sponsor.last_name }}
				</div>
				<div>
					<span class="fw-bold">Description:</span>
					{{ campaign.description }}
				</div>
				<div class="row">
					<div class="col">
						<span class="fw-bold">Start Date:</span>
						{{ campaign.start_date }}
					</div>
					<div class="col">
						<span class="fw-bold">End Date:</span>
						{{ campaign.end_date }}
					</div>
				</div>
				<div class="row">
					<button
						class="btn col"
						v-if="store.state.user.type == 0 && !campaign.approved">
						<h2><i class="bi bi-check-lg text-success"></i></h2>
					</button>
					<button
						class="btn col"
						v-if="store.state.user.type == 0 && campaign.approved">
						<i
							class="bi bi-flag-fill"
							:class="{ 'text-danger': campaign.flagged }"></i>
					</button>
					<button class="btn col">
						<i class="bi bi-trash-fill text-danger"></i>
					</button>
				</div>
			</div>
		</div>
	</div>
	<ModalWindow
		v-if="modalActive"
		@closePopup="modalActive = false"
		:user="detail"></ModalWindow>
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

		.user:hover {
			color: darkcyan;
		}
	}
}
</style>
