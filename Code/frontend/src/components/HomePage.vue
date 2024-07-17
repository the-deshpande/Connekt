<script setup>
import { onMounted } from "vue";
import store from "@/store";
</script>
<template>
	<div class="container text-white">Hi {{ store.state.user.first_name }}</div>
</template>
