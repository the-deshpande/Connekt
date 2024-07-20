<script setup>
import Chart from "chart.js/auto";
import { onMounted, ref } from "vue";

var data = defineProps(["data"]);
data = data.data;

const plugin = {
	id: "canvasBackgroundColor",
	beforeDraw: (chart, args, options) => {
		const { ctx } = chart;
		ctx.save();
		ctx.globalCompositeOperation = "destination-over";
		ctx.fillStyle = "#FFF";
		ctx.fillRect(0, 0, chart.width, chart.height);
		ctx.restore();
	},
};

const values = {
	labels: ["Influencers", "Sponsors"],
	datasets: [
		{
			label: "Total",
			data: data.total,
			borderWidth: 1,
		},
		{
			label: "Active",
			data: data.active,
			borderWidth: 1,
		},
	],
};

const options = {
	aspectRatio: 2,
	plugins: {
		title: {
			display: true,
			text: "Total and Active Users of each Type",
			padding: {
				top: 10,
				bottom: 20,
			},
		},
	},
};

const ctx = ref(null);
onMounted(
	() =>
		new Chart(ctx.value, {
			type: "doughnut",
			data: values,
			options: options,
			plugins: [plugin],
		})
);
</script>
<template>
	<canvas ref="ctx"></canvas>
</template>
