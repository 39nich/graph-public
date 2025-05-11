<template>
	<header id="title" role="banner" aria-labelledby="title">Graph Reading Assistant Tool</header>
	<main id="description" role="main" aria-label="Main Information">
		This is an online tool that uses vibration feedback to help people with visual impairments explore and understand graphs.
		<br>Click the button below to learn how it works or use the buttons after it to start by uploading a graph.
	</main>
	<button id="button" aria-label="Instructions Button" @click="goToHelp">Instructions</button>
    <FileUpload @graph-ready="handleGraphReady"/>
</template>

<script setup lang="ts">
import FileUpload from '@/components/FileUpload.vue'
import { useRouter } from 'vue-router'
import { useGraphStore } from '../stores/graph' 

const router = useRouter()
const store = useGraphStore()

function handleGraphReady(data: any) {
  store.setGraphData(data)
  router.push('/graph')
}

function goToHelp() {
  router.push('/help')
}
</script>

<style scoped>
#title {
	font-weight: bold;
	text-align: center;
	width: 100%;
	margin: 1rem auto;
}

#description {
	font-weight: normal;
	text-align: center;
	width: 100%;
	margin: 1rem auto;
	padding-bottom: 0.5rem;
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
	#title {
		font-size: 2rem;
	}
}

@media (min-width: 768px) {
	#title {
		font-size: 2rem;
	}
}

@media (min-width: 1024px) {
	#title {
		font-size: 3rem;
	}
}
</style>