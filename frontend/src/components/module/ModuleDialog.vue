<template>
  <div class="project-dialog">
    <el-dialog :title=showTitle :visible.sync="showStatus" @close="cancelModule()" width="600px">
      <el-form :rules="rules" ref="form" :model="form" label-width="80px">
        <el-form-item label="项目" prop="name">
          <el-select v-model="form.project_id" placeholder="请选择项目" style="width: 100%" :disabled="true">
            <el-option v-for="item in projectOptions" :key="item.value" :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <div v-if="parentid !== 0">
        <el-form-item label="父节点">
          <el-input v-model="parentnode.label" :disabled="true"></el-input>
        </el-form-item>
        </div>
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input type="textarea" v-model="form.describe"></el-input>
        </el-form-item>
        <el-form-item>
          <div class="dialog-footer">
            <el-button @click="cancelModule()">取消</el-button>
            <el-button type="primary" @click="onSubmit('form')">保存</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
  import ProjectApi from '../../request/project'
  import ModuleApi from '../../request/module'

  export default {
    props: ['moduleid', 'projectid', 'parentid', 'parentnode'],
    data(){
      return {
        showStatus: true,
        showTitle: '',
        projectOptions: [],
        form: {
          project_id: '',
          name: '',
          describe: '',
          parent_id: 0,
        },
         rules: {
          name: [
            { required: true, message: '请输入模块名称', trigger: 'blur' }
          ]
        },
        queryProjectList: {
          page: 1,
          size: 1000,
        },
      }
    },
    created() {
      console.log("this.parentid", this.parentid)
      if (this.moduleid === 0 && this.parentid === 0) {
        this.form.project_id = this.projectid
        this.showTitle = "创建根节点"
      } else if (this.moduleid === 0 && this.parentid !== 0) {
        this.form.project_id = this.projectid
        this.form.parent_id = this.parentid
        this.showTitle = "创建子节点"
      } else {
        this.showTitle = "编辑模块"
        this.getModule()
      }
      this.getAllProject()
    },
    mounted() {
      // this.initProject()
    },
    methods: {
      // 获取所有项目-select
      async getAllProject() {
        this.loading = true
        const resp = await ProjectApi.getProjects(this.queryProjectList)
        if (resp.success == true) {
          var ProjectList = resp.data.projectList;
          for(let i=0; i < ProjectList.length; i++) {
            this.projectOptions.push({
              value: ProjectList[i].id,
              label: ProjectList[i].name,
            })
          }
        } else {
          this.$message.error(resp.error.message);
        }
        this.loading = false
      },

      // 获取一条模块信息
      async getModule() {
        const resp = await ModuleApi.getModule(this.mid)
        if (resp.success == true) {
          this.form = resp.data
        } else {
          this.$message.error(resp.error.message);
        }
      },

      // 关闭dialog
      cancelModule() {
        this.$emit('cancel', {})
      },

      // 创建模块按钮
      onSubmit(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            ModuleApi.createModule(this.form).then(resp => {
              if (resp.success == true) {
                this.$message.success("创建成功！")
                this.cancelModule()
              } else {
                this.$message.error("创建失败！");
              }
            })
          } else {
            return false;
          }
        });
        
      },

    }

  }
</script>

<style scoped>
.dialog-footer {
  float: right;
}
</style>