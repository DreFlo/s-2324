import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

import "bootstrap/dist/css/bootstrap.css";
import 'bootstrap-icons/font/bootstrap-icons';
import 'bootstrap-icons/font/bootstrap-icons.css';

createApp(App).use(router).mount('#app')

import "bootstrap/dist/js/bootstrap.js";
