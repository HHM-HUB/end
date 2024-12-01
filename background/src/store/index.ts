import { createPinia } from "pinia"
import type { App } from "vue"
import useLoginStore from "./login"

const pinia = createPinia()

function piniaGetInfos(app: App) {
  app.use(pinia)
  const loginStore = useLoginStore()
  loginStore.getInfosRoute()
}

export default piniaGetInfos
