<template>
	<div class="results" role="main" v-if="store.graphData && store.graphData.coord_data">
		<header id="graph-title" aria-labelledby="graph-title">{{ store.graphData.title }}</header>
		<section id="graph-metadata">
			<p class="graph-info"><b>Description:</b> {{ store.graphData.graph_description }} <br></p>
			<p class="graph-info"><b>Graph Type:</b> {{ store.graphData.graph_type }}</p>
			<p class="graph-info"><b>X-axis:</b> {{ store.graphData.x_label }}</p>
			<p class="graph-info"><b>Y-axis:</b> {{ store.graphData.y_label }}</p>
		</section>
		<GraphCanvas :pixelData="store.graphData.coord_data"/>
		<button id="button" @click="uploadNewGraph">Upload Another Graph</button>
	</div>
	<div class="results" v-else>
		<p>Graph data is missing. Try uploading again.</p>
	</div>
</template>

<script setup lang=ts>
import { useGraphStore } from '../stores/graph'
import GraphCanvas from '@/components/GraphCanvas.vue'
import { useRouter } from 'vue-router' 

const store = useGraphStore()

const router = useRouter()

function uploadNewGraph() {
  store.clearGraphData()
  router.push('/')
}
</script>

<style scoped>
#graph-title {
	font-weight: bold;
	text-align: center;
	width: 100%;
	margin: 0.5rem auto;
	padding-bottom: 0.5rem;
}

.results {
  	font-weight: normal;
	text-align: center;
	width: 100%;
	margin: 0.5rem auto;
	padding-bottom: 0.5rem;
}

#graph-metadata {
	display: flex;
	flex-flow: row wrap;
	justify-content: center;
	align-items: center;
	align-content: stretch;
	width: 100%;
	height: 100%;
	margin: 0.3rem auto;
	border-bottom: 2px solid gray;
}

.graph-info {
	padding: 1rem auto;
	margin: 0.3rem auto;
}

#button {
	font-size: 2rem;
	font-family: Arial;
	width: 100%;
	background-color: #1d5cdf;
	color: white;
	margin: 0.5rem auto;
	padding: 1rem 0;
	border: none;
	border-radius: 8px;
	cursor: pointer;
	transition: background-color 0.3s ease;
	font-weight: 600;
}

#button:hover,
#button:focus {
	background-color: #2f4f92;
}

@media (max-width: 767px) {
	#graph-title {
		font-size: 2rem;
	}
}

@media (min-width: 768px) {
	#graph-title {
		font-size: 2rem;
	}
}

@media (min-width: 1024px) {
	#graph-title {
		font-size: 2rem;
	}
	p {
		font-size: 1rem;
	}
}
</style>
