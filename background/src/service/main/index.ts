import { requestLogin } from "@/service/request"

// 以下网站请求都是获取下拉菜单的数据
function getRoleData() {
  return requestLogin.post({
    url: "/role/list"
  })
}

function getDepartmentData() {
  return requestLogin.post({
    url: "/department/list"
  })
}
//获取完整的菜单树
function getMenuData() {
  return requestLogin.post({
    url: "/menu/list"
  })
}

export { getRoleData, getDepartmentData, getMenuData }
