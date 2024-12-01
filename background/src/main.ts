import { createApp } from "vue"
import App from "./App.vue"
import "normalize.css"
import "./assets/css/index.less"
// import "element-plus/dist/index.css"
import "element-plus/theme-chalk/el-message.css"

import router from "./router/index"
import pinia from "./store/index"
import registerIcon from "./global/register-icon"

createApp(App).use(pinia).use(router).use(registerIcon).mount("#app")
