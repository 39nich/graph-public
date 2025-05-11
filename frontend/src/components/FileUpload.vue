<template>
	<div class="upload-section" v-if="loading">
		<p>Uploading and analyzing the graph... please wait.</p>
	</div>

	<div class="upload-section" v-else>
			<input id="file" class="file" type="file" accept=".pdf,.png,.jpg,.jpeg" @change="handleFileChange" aria-label="Select a file to upload"/>
            <label for="file">Select a file</label>
            <button class="button" id="upload-button" @click="uploadFile" :disabled="!selectedFile" aria-label="Upload selected file">Upload</button>
	</div>
</template>

<script setup lang="ts">
    import {ref} from 'vue'
    import axios from 'axios'

    const selectedFile = ref<File | null>(null)
    const emit = defineEmits(['graph-ready'])
    const loading = ref(false)

    function handleFileChange(event: Event) {
        const target = event.target as HTMLInputElement
        const file = target.files?.[0] || null
        selectedFile.value = file
    }

    async function uploadFile() {
        if(!selectedFile.value) return
        loading.value = true

        const formData = new FormData()
        formData.append('file', selectedFile.value)

        try {
            const response = await axios.post('https://graph-backend-hlqx.onrender.com/api/convert/', formData)
            console.log('response:', response.data.graph_data) 
            emit('graph-ready', response.data.graph_data)
        } catch (error) {
            console.error('Upload failed:', error)
            if (axios.isAxiosError(error) && error.response) {
                console.error('Backend response:', error.response.data)
                alert("Error: " + JSON.stringify(error.response.data, null, 2))
            }
        } finally {
            loading.value = false
        }
    }
</script>

<style scoped>
.file {
    opacity: 0;
    width: 0.1px;
    height: 0.1px;
    position: absolute;
}

.upload-section {
    display: flex;
    flex-flow: column nowrap;
	justify-content: center;
	align-items: center;
	align-content: stretch;
	font-weight: normal;
	text-align: center;
	width: 100%;
	margin: 0 auto;
}

.upload-section label {
	font-size: 2rem;
    font-family: Arial;
	width: 100%;
	background-color: #0d8815;
	color: white;
	margin: 0.5rem auto;
	padding: 1rem 0;
	border: none;
	border-radius: 8px;
	cursor: pointer;
	font-weight: 600;
    text-align: center;
    transition: background-color 0.3s ease;
}

.upload-section label:hover,
.upload-section label:focus {
    background-color: #185f1d;
}

.button {
	font-size: 2rem;
    font-family: Arial;
	width: 100%;
	background-color: #b11525;
	color: white;
	margin: 0.5rem auto;
	padding: 1rem 0;
	border: none;
	border-radius: 8px;
	cursor: pointer;
	font-weight: 600;
    transition: background-color 0.3s ease;
}

.button:hover,
.button:focus {
    background-color: #7c2b33;
}

.button:disabled {
    background-color: gray;
    cursor: not-allowed;
}
</style>