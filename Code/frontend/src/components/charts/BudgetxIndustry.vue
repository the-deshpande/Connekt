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
	labels: ["Healthcare", "Gaming", "Tech", "Vlog"],
	datasets: [
		{
			label: "Budget of Campaign",
			data: data.budget,
			borderWidth: 1,
		},
		{
			label: "Spent on Contracts",
			data: data.actual_spent,
			borderWidth: 1,
		},
	],
};

const options = {
	plugins: {
		title: {
			display: true,
			text: "Budget vs Actual Spent by Industry",
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
			type: "bar",
			data: values,
			options: options,
			plugins: [plugin],
		})
);
</script>
<template>
	<canvas ref="ctx"></canvas>
</template>
