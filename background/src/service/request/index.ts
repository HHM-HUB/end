import axios from "axios"
import type { AxiosInstance, AxiosRequestConfig } from "axios"
import { TIMEOUT, BASEURL } from "../config"
import { TOKEN } from "@/global/constants"
import { MYLocalStorage } from "@/utils/storage"

class HYRequest {
  instance: AxiosInstance
  constructor(config: AxiosRequestConfig) {
    this.instance = axios.create(config)

    //请求拦截器
    this.instance.interceptors.request.use((config: any) => {
      // 在拦截器上，加上必须要携带的token
      const token = MYLocalStorage.getLocalStorage(TOKEN)
      if (config.headers && token) {
        config.headers.Authorization = token
      }
      return config
    })
    //响应拦截器
    this.instance.interceptors.response.use((config) => {
      return config
    })
  }

  request(config: AxiosRequestConfig) {
    return new Promise((resolve, rejcet) => {
      this.instance
        .request(config)
        .then((res) => {
          resolve(res)
        })
        .catch((err) => {
          rejcet(err)
        })
    })
  }
  get(config: AxiosRequestConfig) {
    return this.request({ ...config, method: "get" })
  }
  post(config: AxiosRequestConfig) {
    return this.request({ ...config, method: "post" })
  }
  delete(config: AxiosRequestConfig) {
    return this.request({ ...config, method: "delete" })
  }
  patch(config: AxiosRequestConfig) {
    return this.request({ ...config, method: "patch" })
  }
}

const requestLogin: any = new HYRequest({
  baseURL: BASEURL,
  timeout: TIMEOUT
})

export { requestLogin }
