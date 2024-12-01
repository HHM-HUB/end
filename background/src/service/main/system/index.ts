import { requestLogin } from "@/service/request"

function getUserListData(info: any) {
  return requestLogin.post({
    url: "/users/list",
    data: info
  })
}

function deleteUser(id: number) {
  return requestLogin.delete({
    url: "/users/" + id
  })
}

function createUser(form: any) {
  return requestLogin.post({
    url: "/users",
    data: form
  })
}

function updateUser(form: any, id: number) {
  return requestLogin.patch({
    url: "/users/" + id,
    data: form
  })
}

//获取页面数据的增删改查（通过页面）
function getPageListData(pageName: string, form: any) {
  return requestLogin.post({
    url: `/${pageName}/list`,
    data: form
  })
}

function deletePageListData(pageName: string, id: number) {
  return requestLogin.delete({
    url: `/${pageName}/${id}`
  })
}

function createPageListData(pageName: string, form: any) {
  return requestLogin.post({
    url: `/${pageName}`,
    data: form
  })
}

function editPageListData(pageName: string, form: any, id: number) {
  return requestLogin.patch({
    url: `/${pageName}/${id}`,
    data: form
  })
}

export {
  getUserListData,
  deleteUser,
  createUser,
  updateUser,
  getPageListData,
  deletePageListData,
  createPageListData,
  editPageListData
}
