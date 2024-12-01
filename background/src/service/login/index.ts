import { requestLogin } from "../request"

interface IInfo {
  account: string | number
  password: string | number
}

//1.通过用户名个密码获取token
function loginInterface(info: IInfo): any {
  return requestLogin.post({
    url: "/login",
    data: {
      name: info.account,
      password: info.password
    }
  })
}

// 2.获取登录角色的相关信息
function getuserInfo(id: number) {
  return requestLogin.get({
    url: "/users/" + id
    // headers: {
    //   Authorization: "Bearer" + localStorage.getItem(TOKEN)
    // }
  })
}

// 3.根据id，获取角色的权限菜单信息
function getMenuInfo(id: number) {
  return requestLogin.get({
    url: `/role/${id}/menu`
  })
}

export { loginInterface, getuserInfo, getMenuInfo }
