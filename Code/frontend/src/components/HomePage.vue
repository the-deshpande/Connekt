<script setup>
import { onMounted } from "vue";
import store from "@/store";

onMounted(async () => {
	const abc = await store.dispatch("getUserData", store.state.accessToken);
	console.log(abc);
});
</script>
<template>
	<div class="container text-white">Hi {{ store.getters.userData }}</div>
</template>
