<script setup>
import store from "@/store";
import router from "@/router";
import { reactive } from "vue";
import axios from "axios";

defineEmits(["closePopup"]);
var item = defineProps(["item"]);
item = item.item;

let entry;
let influencers;
let campaigns;
if (item.item == 0) {
	entry = reactive({
		name: "",
		description: "",
		start_date: "",
		end_date: "",
		goals: 0,
		public: false,
	});
} else if (item.item == 1) {
	entry = reactive({
		requirements: "",
		payment_amount: 0,
		campaign_id: 0,
		influencer_id: 0,
	});
	if (item.campaign_id) {
		entry.campaign_id = item.campaign_id;
	}
	if (item.influencer_id) {
		entry.influencer_id = item.influencer_id;
	}

	if (!store.state.user.influencer) {
		var response = await store.dispatch(
			"getUsersList",
			store.state.accessToken
		);
		influencers = reactive(response.data.users);
	}

	response = await store.dispatch("getCampaignsList", store.state.accessToken);
	campaigns = reactive(
		response.data.campaigns.filter((i) => i.approved && !i.flagged)
	);
}

async function addCampaign() {
	if (
		this.entry.name == "" ||
		this.entry.description == "" ||
		this.entry.start_date == "" ||
		this.entry.end_date == "" ||
		this.entry.goals == 0 ||
		Date.parse(this.entry.start_date) > Date.parse(this.entry.end_date)
	) {
		alert("Please enter the data correctly");
		return;
	}

	const path = "http://127.0.0.1:5000/campaigns/create";
	var response = await axios
		.post(path, this.entry, {
			headers: {
				Authorization: `Bearer ${store.state.accessToken}`,
			},
		})
		.then((response) => response)
		.catch((resposne) => response.response);
	console.log(response);
	if (response.status == 201) {
		router.go();
	}
}

async function addContract() {
	if (store.state.user.influencer)
		this.entry.influencer_id = store.state.user.influencer.id;

	if (
		this.entry.requirements == "" ||
		this.entry.payment_amount == 0 ||
		this.entry.influencer_id == 0 ||
		this.entry.campaign_id == 0
	) {
		alert("Please enter the data correctly");
		return;
	}

	const path = "http://127.0.0.1:5000/contracts/create";
	var response = await axios
		.post(path, this.entry, {
			headers: {
				Authorization: `Bearer ${store.state.accessToken}`,
			},
		})
		.then((response) => response)
		.catch((resposne) => response.response);
	console.log(response);
	if (response.status == 201) {
		router.go();
	}
}
</script>

<template>
	<div class="modal-wrapper" aria-modal="true" role="dialog" tabindex="-1">
		<div class="inner text-white" v-if="item.item == 0">
			<button class="close-btn" @click="$emit('closePopup')">
				<i class="bi bi-x-lg text-white"></i>
			</button>
			<div class="row my-2 mt-4">
				<label for="name" class="col-3 form-label">Name: </label>
				<input
					type="text"
					id="name"
					class="col form-control input-grey text-white"
					v-model="entry.name" />
			</div>

			<div class="row my-2">
				<label for="description" class="col-3 form-label">Description: </label>
				<input
					type="text"
					id="description"
					class="col form-control input-grey text-white"
					v-model="entry.description" />
			</div>

			<div class="row my-2">
				<label for="public" class="col-3 form-label">Visibility: </label>
				<button
					type="checkbox"
					id="public"
					class="col btn text-white"
					:class="[entry.public ? 'btn-outline-success' : 'btn-outline-danger']"
					@click="entry.public = !entry.public">
					{{ entry.public ? "Public" : "Private" }}
				</button>
			</div>

			<div class="row my-2">
				<label for="start-date" class="col-3 form-label">Start Date: </label>
				<input
					type="date"
					id="start-date"
					class="col form-control input-grey text-white"
					v-model="entry.start_date" />
			</div>

			<div class="row my-2">
				<label for="end-date" class="col-3 form-label">End Date: </label>
				<input
					type="date"
					id="end-date"
					class="col form-control input-grey text-white"
					v-model="entry.end_date" />
			</div>

			<div class="row my-2">
				<label for="goals" class="col-3 form-label">Goals: </label>
				<input
					type="number"
					id="goals"
					class="col form-control input-grey text-white"
					v-model="entry.goals" />
			</div>

			<div class="row">
				<div class="col"></div>
				<button @click="addCampaign()" class="btn col btn-green text-white">
					Add Campaign
				</button>
				<div class="col"></div>
			</div>
		</div>
		<div class="inner text-white" v-else-if="item.item == 1">
			<button class="close-btn" @click="$emit('closePopup')">
				<i class="bi bi-x-lg text-white"></i>
			</button>
			<div class="row my-2 mt-4">
				<label for="requirements" class="col-3 form-label"
					>Requirements:
				</label>
				<input
					type="text"
					id="requirements"
					class="col form-control input-grey text-white"
					v-model="entry.requirements" />
			</div>

			<div class="row my-2">
				<label for="payment-amount" class="col-3 form-label"
					>Payment Amount:
				</label>
				<input
					type="number"
					id="payment-amount"
					class="col form-control input-grey text-white"
					v-model="entry.payment_amount" />
			</div>

			<div class="row my-2">
				<label for="campaigns" class="col-3 form-label">Campaign: </label>
				<select
					class="col form-select input-grey text-white"
					id="campaigns"
					v-model="entry.campaign_id">
					<option v-for="campaign in campaigns" :value="campaign.id">
						{{ campaign.name }}
					</option>
				</select>
			</div>

			<div class="row my-2" v-if="!store.state.user.influencer">
				<label for="influencer" class="col-3 form-label">Influencer: </label>
				<select
					class="col form-select input-grey text-white"
					id="influencer"
					v-model="entry.influencer_id">
					<option
						v-for="influencer in influencers"
						:value="influencer.influencer.id">
						{{ influencer.first_name }} {{ influencer.last_name }}
					</option>
				</select>
			</div>

			<div class="row">
				<div class="col"></div>
				<button @click="addContract()" class="btn col btn-green text-white">
					Add Contract
				</button>
				<div class="col"></div>
			</div>
		</div>
	</div>
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

		.btn-green {
			background-color: #468585;
		}

		.text-green {
			color: #9cdba6;
		}

		.input-grey {
			background-color: #758694;
		}
	}
}
</style>
