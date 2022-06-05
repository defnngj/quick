import axios from "axios"
import request from '@/HttpCommon.js'


class ProjectApi {

  getProjects(data) {
    return request.get('/v2/project/list/', data)
  }

  getProject(pid) {
    return request.get('/v2/project/' + pid + '/info/')
  }

  deleteProject(pid) {
    return request.delete('/v2/project/' + pid + '/delete/')
  }

  createProject(data) {
    return request.post('/v2/project/create/', data)
  }

  updateProject(pid, data) {
    return request.put('/v2/project/' + pid + '/update/', data)
  }
  
  getModuleTree(pid){
    return request.get('/v2/project/' + pid + '/moduleTree/')
  }

  updateProjectImage(data) {
    return axios({
      method: "post",
      url: "/v2/project/upload/",
      timeout: 20000,
      data: data,
    })
  }

}

export default new ProjectApi()