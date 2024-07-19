<script setup>
import store from "@/store";
import router from "@/router";
import ModalWindow from "./UserModal.vue";
import AddItemModal from "./AddItemModal.vue";
import { ref, reactive } from "vue";
import axios from "axios";

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
	this.item.campaign_id = this.campaign.id;
	this.addItem = true;
}

async function flagCampaign(campaign_id) {
	const path = "http://127.0.0.1:5000/campaigns";
	var response = await axios
		.post(
			path,
			{ campaign_id: campaign_id },
			{
				headers: {
					Authorization: `Bearer ${store.state.accessToken}`,
				},
			}
		)
		.then((response) => {
			if (this.campaign.approved) {
				this.campaign.flagged = !this.campaign.flagged;
			} else {
				this.campaign.approved = true;
			}
			return response;
		})
		.catch((response) => {
			alert(response.response.data.message);
			return response.response;
		});
	console.log(response);
}

async function deleteCampaign(campaign_id) {
	if (confirm("Are you sure?")) {
		const path = "http://127.0.0.1:5000/campaigns";
		var response = await axios
			.delete(path, {
				headers: {
					Authorization: `Bearer ${store.state.accessToken}`,
				},
				data: { campaign_id: campaign_id },
			})
			.then((response) => {
				return response;
			})
			.catch((response) => {
				alert(response.response.data.message);
				return response.response;
			});
		console.log(response);
		if (response.status == 202) {
			router.go();
		}
	}
}

let editMode = ref(false);
async function editCampaign() {
	if (
		this.campaign.name == "" ||
		this.campaign.description == "" ||
		this.campaign.start_date == "" ||
		this.campaign.end_date == "" ||
		this.campaign.goals == 0 ||
		Date.parse(this.campaign.start_date) > Date.parse(this.campaign.end_date)
	) {
		alert("Please enter the data correctly");
		return;
	}
	const path = "http://127.0.0.1:5000/campaigns";
	var response = await axios
		.put(path, this.campaign, {
			headers: {
				Authorization: `Bearer ${store.state.accessToken}`,
			},
		})
		.then((response) => {
			if (store.state.user.type != 0) this.campaign.approved = false;
			return response;
		})
		.catch((response) => {
			router.go();
			return response.response;
		});

	console.log(response);
	this.editMode = false;
}

defineEmits(["closePopup"]);
var campaign = defineProps(["campaign"]);
campaign = ref(campaign.campaign);
</script>

<template>
	<div class="modal-wrapper" aria-modal="true" role="dialog" tabindex="-1">
		<div class="inner" v-if="!editMode">
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
				<div>
					<span class="fw-bold">Visibility:</span>
					{{ campaign.public ? "Public" : "Private" }}
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
						@click="flagCampaign(campaign.id)"
						class="btn col"
						v-if="store.state.user.type == 0 && !campaign.approved">
						<h2><i class="bi bi-check-lg text-success"></i></h2>
					</button>
					<button
						@click="flagCampaign(campaign.id)"
						class="btn col"
						v-else-if="store.state.user.type == 0 && campaign.approved">
						<i
							class="bi bi-flag-fill"
							:class="{ 'text-danger': campaign.flagged }"></i>
					</button>

					<button
						@click="editMode = true"
						class="btn col"
						v-if="
							store.state.user.type == 0 ||
							campaign.sponsor.id == store.state.user.id
						">
						<i class="bi bi-pencil text-warning"></i>
					</button>

					<button
						class="btn col"
						v-if="!store.state.user.influencer"
						@click="deleteCampaign(campaign.id)">
						<i class="bi bi-trash-fill text-danger"></i>
					</button>
				</div>
				<div
					class="row mt-3"
					v-if="store.state.user.type == 2 || store.state.user.type == 1">
					<div class="col"></div>
					<button
						@click="createContract()"
						class="btn btn-green text-white col"
						:disabled="
							!campaign.approved ||
							campaign.flagged ||
							(store.state.user.type == 1 && !campaign.public)
						">
						Create Contract
					</button>
					<div class="col"></div>
				</div>
			</div>
		</div>
		<div class="inner" v-else>
			<button class="close-btn" @click="$emit('closePopup')">
				<i class="bi bi-x-lg"></i>
			</button>
			<div class="row my-2">
				<label for="name" class="col-3 form-label">Name: </label>
				<input
					type="text"
					id="name"
					class="col form-control"
					v-model="campaign.name" />
			</div>

			<div class="row my-2">
				<label for="description" class="col-3 form-label">Description: </label>
				<input
					type="text"
					id="description"
					class="col form-control"
					v-model="campaign.description" />
			</div>

			<div class="row my-2">
				<label for="public" class="col-3 form-label">Visibility: </label>
				<button
					type="checkbox"
					id="public"
					class="col btn"
					:class="[
						campaign.public ? 'btn-outline-success' : 'btn-outline-danger',
					]"
					@click="campaign.public = !campaign.public">
					{{ campaign.public ? "Public" : "Private" }}
				</button>
			</div>

			<div class="row my-2">
				<label for="start-date" class="col-3 form-label">Start Date: </label>
				<input
					type="date"
					id="start-date"
					class="col form-control"
					v-model="campaign.start_date" />
			</div>

			<div class="row my-2">
				<label for="end-date" class="col-3 form-label">End Date: </label>
				<input
					type="date"
					id="end-date"
					class="col form-control"
					v-model="campaign.end_date" />
			</div>

			<div class="row my-2">
				<label for="goals" class="col-3 form-label">Goals: </label>
				<input
					type="number"
					id="goals"
					class="col form-control"
					v-model="campaign.goals" />
			</div>

			<div class="row">
				<div class="col"></div>
				<button @click="editCampaign()" class="btn col btn-green text-white">
					Make Changes
				</button>
				<div class="col"></div>
			</div>
		</div>
	</div>
	<ModalWindow
		v-if="modalActive"
		@closePopup="modalActive = false"
		:user="detail"></ModalWindow>
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
			cursor: pointer;
		}

		.btn-green {
			background-color: #468585;
		}
	}
}
</style>
