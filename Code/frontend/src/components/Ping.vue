<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";

let msg = ref("Hello");

function getMessage() {
	const path = "http://127.0.0.1:5000/ping";
	axios
		.get(path)
		.then((response) => {
			msg.value = response.data;
			console.log(response.data);
		})
		.catch((error) => {
			console.error(error);
		});
}

onMounted(() => {
	// getMessage();
});
</script>

<template>
	<div class="container">
		<p class="text-white">{{ msg }}</p>
	</div>
</template>
