<script setup>
import { onMounted, computed } from "vue";
import store from "@/store";
import router from "@/router";

function getData() {
	if (store.getters.isLoggedIn) {
		store.dispatch("getUserData", store.state.accessToken);
	} else {
		router.push("/login");
	}
}

onMounted(() => {
	getData();
});
</script>
<template>
	<div class="container text-white">Hi {{ store.state.user.first_name }}</div>
</template>
