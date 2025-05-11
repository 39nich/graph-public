<template>
  <h1 aria-label="Instructions" id="title">Instructions for Using the Graph Reader</h1>
	<main id="description" role="main" aria-label="Instructions split by section">
    <section aria-label="About this program">
      <h2>About This Program</h2>
      <p>
        This application assists blind and visually impaired users in exploring graphs through sound and vibration feedback. Upload a graph image and interact with it using a mouse, touchscreen, or assistive technology.
      </p>
    </section>

    <section aria-label="Step by step instructions">
      <h2>How to Use the Program</h2>
      <ol>
        <li>  On the home page, you will find three buttons from top to bottom: "Instructions", "Select File", and "Upload".</li>
        <li>  Select the "Instructions" button to review this guidance.</li>
        <li>  Select the "Select File" button to choose a PNG image of the graph you want to explore.</li>
        <li>  After selecting a file, the "Upload" button will become active. <strong>Note:</strong> The "Upload" button is disabled until a file is selected.</li>
        <li>  Press the "Upload" button to start processing the file.</li>
        <li>  A loading message will appear. Please wait; processing may take up to a minute depending on the image size.</li>
        <li>  After processing, you will automatically be taken to the graph exploration page.</li>
      </ol>
    </section>

    <section aria-label="Graph interaction guide">
      <h2>Exploring the Graph</h2>
      <p>
        On the graph page, information about the graph will be shown at the top, followed by a canvas area where the graph is displayed.
      </p>
      <ul>
        <li>
          <strong>  On a computer:</strong> Move your mouse over the canvas area. When you are on the graph line or over a point, a beeping sound will play. Follow the sound to trace the graph shape.
        </li>
        <li>
          <strong>  On a phone or tablet:</strong> Move your finger across the screen. Your device will vibrate or beep when you touch the graph line.
        </li>
        <li>
            If the sound or vibration stops, you have moved off the graph. Adjust your movement to return to the graph.
        </li>
      </ul>
    </section>

    <section aria-label="Important notes and disclaimers">
      <h2>Important Notes</h2>
      <ul>
        <li>  Vibration feedback is supported on Android phones and Windows devices with built-in vibration motors.</li>
        <li>  iOS devices provide audio feedback only; vibration is not supported by iOS browsers.</li>
        <li>  Desktop and laptop computers will provide only audio beeping feedback.</li>
        <li>  Currently, only PNG image files are supported for upload.</li>
        <li>  This version of the program supports scatter plots and line graphs. Other graph types may not be interpreted correctly.</li>
      </ul>
    </section>

    <section aria-label="Disclaimer">
      <h2>Disclaimer</h2>
      <p>
        This application is experimental. The accuracy of graph interpretation depends on the clarity and quality of the uploaded image. Results may vary.
      </p>
    </section>
	</main>
	<button id="button" @click="goToHome">Return Home</button>

</template>
<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter();
function goToHome() {
  router.push('/')
}
</script>

<style scoped>
#title {
	font-weight: bold;
	text-align: center;
	width: 100%;
	margin: 1rem auto;
}

h2 {
  font-weight: bold;
	text-align: justify;
	width: 100%;
	margin: 1rem auto;
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
		font-size: 2.5rem;
	}
  h2 {
    font-size: 1.75rem;
  }
}

@media (min-width: 768px) {
	#title {
		font-size: 2.5rem;
	}
  h2 {
    font-size: 2rem;
  }
}

@media (min-width: 1024px) {
	#title {
		font-size: 3.5rem;
	}
  h2 {
    font-size: 3rem;
  }
  p, ol, ul {
    font-size: 1.6rem;
  }
}
</style>