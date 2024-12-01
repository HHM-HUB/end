class Storage {
  storage: any
  constructor(isFlag = true) {
    this.storage = isFlag ? localStorage : sessionStorage
  }

  setLocalStorage(key: string, value: any) {
    if (value) {
      this.storage.setItem(key, JSON.stringify(value))
    }
  }
  getLocalStorage(key: string) {
    let res
    if (key) {
      res = JSON.parse(this.storage.getItem(key))
    }
    return res
  }
  removeLocalStorage(key: string) {
    this.storage.removeItem(key)
  }

  cleanLocalStorage() {
    this.storage.clear()
  }
}

const MYLocalStorage = new Storage()
const MYSessionStorage = new Storage(false)

export { MYLocalStorage, MYSessionStorage }
