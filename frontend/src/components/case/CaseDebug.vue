<template>
  <div>
    <!-- 调试表单 -->
    <div class="div-line" style="height: 50px;">
      <span style="width: 10%; float: left;">
        <el-select v-model="api.method" placeholder="请求方法"  style="width: 100%">
          <el-option v-for="item in methods" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
      </span>
      <span style="width: 80%; float: left;">
        <el-input v-model="api.url" placeholder="请输入接口"></el-input>
      </span>
      <span style="width: 10%; float: left;">
        <el-button type="primary" @click="clickSend()">发送</el-button>
      </span>
    </div>

    <div class="div-line">
      <el-radio v-model="api.params_type" label="params">params</el-radio>
      <el-radio v-model="api.params_type" label="data">form-data</el-radio>
      <el-radio v-model="api.params_type" label="json">JSON</el-radio>
    </div>
    
    <div class="div-line">
      <el-tabs v-model="activeJSON">
        <el-tab-pane label="Headers" name="first">
          <vueJsonEditor v-model="api.header" :mode="'code'"></vueJsonEditor>
        </el-tab-pane>
        <el-tab-pane label="Params/Body" name="second">
          <vueJsonEditor v-model="api.params_body" :mode="'code'"></vueJsonEditor>
        </el-tab-pane>
      </el-tabs>
    </div>
    <div class="div-line">
      <el-input type="textarea"
        :rows="5"
        placeholder="Response"
        v-model="api.result">
      </el-input>
    </div>

    <div class="div-line">
      <el-collapse v-model="otherNames">
        <!-- 断言 -->
        <el-collapse-item title="断言" name="1">
          <span style="float: left;">
            <div class="div-line">
              <el-radio v-model="api.assert_type" label="include">include</el-radio>
              <el-radio v-model="api.assert_type" label="equal">equal</el-radio>
            </div>
          </span>
          <span style="float: right; margin-bottom: 5px;">
            <el-button type="success" plain size="small" @click="clickAssert()">断言</el-button>
          </span>
          <el-input type="textarea"
            :rows="5"
            placeholder="Assert"
            v-model="api.assert_text">
          </el-input>
        </el-collapse-item>

        <el-collapse-item title="保存用例" name="2">
          <div class="dev-line" style="margin-bottom: 10px;">
            <el-select v-model="api.project_id" placeholder="请选择项目" @change="chanageProject()">
              <el-option
                v-for="(item, index) in projectOptions"
                :key="index"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
            <el-select v-model="api.module_id" placeholder="请选择模块">
              <el-option
                v-for="item in moduleOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </div>
          <div class="dev-line">
            <span style="width: 80%; float: left; margin-right: 10px;">
              <el-input v-model="api.name" placeholder="请输入名称"></el-input>
            </span>
            <span style="width: 15%; float: left;">
              <el-button type="danger" @click="saveCase()">保存</el-button>
            </span>
          </div>
        </el-collapse-item>       
      </el-collapse>
    </div>
  </div>
</template>

<script>
import CaseApi from '../../request/case'
import ProjectApi from '../../request/project'
import vueJsonEditor from 'vue-json-editor'

  export default {
    components: {
      vueJsonEditor
    },
    props: ['cid'],
    data(){
      return {
        methods:[
          {value: 'GET', label: 'GET'}, 
          {value: 'POST', label: 'POST'},
          {value: 'PUT', label: 'PUT'},
          {value: 'DELETE', label: 'DELETE'}
        ],
        api: {
          method: 'GET',
          url: 'http://httpbin.org/get',
          header: {},
          params_type: 'params',
          params_body: {},
          result: '',
          assert_type: 'include',
          assert_text: '',
          module_id: '',
          name: ''
        },
        activeJSON: 'first',
        otherNames: [''],
        projectOptions: [],
        projectId: '',
        moduleOptions: [],
      }
    },
    created() {
      if (this.cid !== 0) {
        this.initCaseInfo()
      } else {
        this.api = {
          method: 'GET',
          url: 'http://httpbin.org/get',
          header: {},
          params_type: 'params',
          params_body: {},
          result: '',
          assert_type: 'include',
          assert_text: '',
          project_id: '',
          module_id: '',
          name: ''
        }
      }
    },
    mounted() {},
    methods: {
      handleChange(val) {
        console.log("val", val)
        this.getProjectList()
      },

      // 初始化用例信息
      async initCaseInfo() {
        let resp = await CaseApi.getCase(this.cid)
        this.api = resp.data
        this.api.result = JSON.parse(this.api.result)
        this.chanageProject()
        this.api.module_id = this.api.module_id.toString()
      },
      // 点击发送
      async clickSend() {
        if(this.api.url == '') {
          this.$message.error('url不能为空')
          return
        }
        // data to JSON
        const req = {
          method: this.api.method,
          url: this.api.url,
          header: JSON.stringify(this.api.header),
          params_type: this.api.params_type,
          params_body: JSON.stringify(this.api.params_body),
        }
        const resp = await CaseApi.debugCase(req)
        if (resp.success == true) {
          this.api.result = resp.data
        } else {
          this.$message.error(resp.error.message)
        }       
      },

      // 断言
      async clickAssert() {
        var assertText = this.api.assert_text
        if (this.api.assert_type == 'equal') {
          assertText = JSON.stringify(this.api.assert_text)
        }
        const req = {
          result: JSON.stringify(this.api.result),
          assert_type: this.api.assert_type,
          assert_text: assertText
        }
        const resp = await CaseApi.assertCase(req)
        if (resp.success == true) {
          this.$message.success('断言成功')
        } else {
          this.$message.error(resp.error.message)
        }
      },

      // 获取项目列表
      async getProjectList() {
        const query = {page: 1, size: 1000}
        const resp = await ProjectApi.getProjects(query)
        if (resp.success == true) {
          const ProjectList = resp.data.projectList
          for(let i=0; i < ProjectList.length; i++) {
            this.projectOptions.push({
              value: ProjectList[i].id.toString(),
              label: ProjectList[i].name,
            })
          }
        } else {
          this.$message.error(resp.error.message);
        }
        this.loading = false
      },

      async chanageProject() {
        this.moduleOptions = []
        const query = {page: 1, size: 1000}
        const resp = await ProjectApi.getModules(this.api.project_id, query)
        if (resp.success == true) {
          const ModuleList = resp.data.moduleList
          for(let i=0; i < ModuleList.length; i++) {
            this.moduleOptions.push({
              value: ModuleList[i].id.toString(),
              label: ModuleList[i].name,
            })
          }
        }
      },

      async saveCase() {
        if(this.api.url == '') {
          this.$message.error('url不能为空')
          return
        }
        if (this.api.name == '') {
          this.$message.error('名称不能为空')
          return
        }

        // data to JSON
        this.api.header = JSON.stringify(this.api.header)
        this.api.params_body = JSON.stringify(this.api.params_body)
        this.api.result = JSON.stringify(this.api.result)
        const resp = await CaseApi.createCase(this.api)
        if(resp.success == true) {
           // JSON to data
          this.api.header = JSON.parse(this.api.header)
          this.api.params_body = JSON.parse(this.api.params_body)
          this.api.result = JSON.parse(this.api.result)
          this.$message.success('创建用例成功')
        } else {
          this.$message.error(resp.error.message)
        }

      }

    }
  }
</script>

<style>
div.jsoneditor {
  border: thin solid #ced4da;
}

div.jsoneditor-menu {
  display: none;
}

.ace-jsoneditor .ace_gutter {
  background: white;
}

div.jsoneditor-outer.has-main-menu-bar {
  margin-top: 0px;
  padding-top: 0px;
}

.per-label {
  margin-right: 10px;
  margin-bottom: 4px;
  font-size: 1rem;
}
</style>
<style scoped>
.debug-button {
  height: 50px;
  text-align: right;
}

.div-line {
  height: auto;
  width: 100%;
  text-align: left;
  margin-bottom: 10px;
}

</style>
