import request from '@/HttpCommon.js'


class ModuleApi {
  getModules(data) {
    return request.get('/v1/module/', data)
  }

  getModule(mid) {
    return request.get('/v1/module/'+mid+'/')
  }

  deleteModule(mid) {
    return request.delete('/v1/module/'+mid+'/')
  }

  createModule(data) {
    return request.post('/v1/module/', data)
  }

  updateModule(mid, data) {
    return request.put('/v1/module/'+mid+'/', data)
  }

  getModuleTree(pid){
    return request.get('/v1/'+pid+'/node/tree/')
  }

  getModuleCases(mid, data){
    return request.get('/v1/module/'+mid+'/cases/', data)
  }

}

export default new ModuleApi()