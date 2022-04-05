<template>
  <div style="margin-left: 10px;
    margin-right: 10px;">
    <!-- 调试表单 -->
    <div class="div-line" style="height: 50px;">
      <span style="width: 15%; float: left;">
        <el-select v-model="api.method" placeholder="请求方法"  style="width: 100%">
          <el-option v-for="item in methods" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
      </span>
      <span style="width: 70%; float: left;">
        <el-input v-model="api.url" placeholder="请输入接口"></el-input>
      </span>
      <span style="width: 15%; float: left;">
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
        :rows="8"
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

      </el-collapse>

      <div class="div-line" style="height: 50px; margin-top: 30px;">
        <span style="width: 80%; float: left;">
          <el-input v-model="api.name" placeholder="请输入名称"></el-input>
        </span>
        <span style="float: right;">
          <el-button type="success" @click="saveCase()">保存</el-button>
        </span>
      </div>

    </div>
  </div>
</template>

<script>
import CaseApi from '../../request/case'
import vueJsonEditor from 'vue-json-editor'

  export default {
    components: {
      vueJsonEditor
    },
    props: ['mid', 'cid'],
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
      this.api.module_id = this.mid
      if (this.cid !== 0) {
        this.initCaseInfo()
      } else {
        this.api = {
          method: 'GET',
          url: 'http://httpbin.org/get',
          header: {"token": "123"},
          params_type: 'params',
          params_body: {"hello": "world"},
          result: '',
          assert_type: 'include',
          assert_text: '',
          module_id: '',
          name: ''
        }
      }
    },
    mounted() {},
    methods: {

      // 初始化用例信息
      async initCaseInfo() {
        let resp = await CaseApi.getCase(this.cid)
        this.api = resp.data
        this.api.header = JSON.parse(this.api.header)
        this.api.params_body = JSON.parse(this.api.params_body)
        this.api.result = JSON.parse(this.api.result)
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
          this.$message.success("发送成功")
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

      async saveCase() {
        if(this.api.url == '') {
          this.$message.error('url不能为空')
          return
        }
        if (this.api.name == '') {
          this.$message.error('名称不能为空')
          return
        }

        var assertText = this.api.assert_text
        if (this.api.assert_type == 'equal') {
          assertText = JSON.stringify(this.api.assert_text)
        }

        const req = {
          name: this.api.name,
          module_id: this.mid,
          method: this.api.method,
          url: this.api.url,
          header: JSON.stringify(this.api.header),
          params_type: this.api.params_type,
          params_body: JSON.stringify(this.api.params_body),
          result: JSON.stringify(this.api.result),
          assert_type: this.api.assert_type,
          assert_text: assertText,
        }

        if(this.cid == 0) {
          const resp = await CaseApi.createCase(req)
          if(resp.success == true) {
            this.$message.success('创建用例成功')
            this.saveCaseSuccess()
          } else {
            this.$message.error(resp.error.message)
          }
        } else {
          const resp = await CaseApi.updateCase(this.cid, req)
          if(resp.success == true) {
            this.$message.success('更新用例成功')
            this.saveCaseSuccess()
          } else {
            this.$message.error(resp.error.message)
          }
        }
        
        

      },

      // 保存用例
      saveCaseSuccess() {
        this.$emit('cancel', {})
      },

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
