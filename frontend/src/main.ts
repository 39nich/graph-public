import './assets/main.css'          // Loads CSS file to apply styles

import { createApp } from 'vue'     // Bring createApp from the Vue framework
import { createPinia } from 'pinia'

import App from './App.vue'         //Import the root Vue component called App
import router from './router'

// Create, set up and mount the Vue App
const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
