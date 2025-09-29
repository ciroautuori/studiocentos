import './assets/styles/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Import Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faFacebookF, faInstagram, faYoutube } from '@fortawesome/free-brands-svg-icons'
import { faPhone, faEnvelope, faLocationDot } from '@fortawesome/free-solid-svg-icons'

// Add icons to library
library.add(
  // Brand icons
  faFacebookF,
  faInstagram,
  faYoutube,
  // Solid icons
  faPhone,
  faEnvelope,
  faLocationDot
)

const app = createApp(App)

// Register Font Awesome component
app.component('font-awesome-icon', FontAwesomeIcon)

app.use(router)

app.mount('#app')
