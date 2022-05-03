<template>
  <div class="task-dialog">
    <el-dialog :title=showTitle :visible.sync="showStatus" @close="cancelTask()">
      <el-form v-if="inResize === true" :rules="rules" ref="form" :model="form" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input type="textarea" v-model="form.describe"></el-input>
        </el-form-item>
        <el-form-item label="选择用例">
          <el-card class="div-tree">
          <div>
            <el-tree :data="moduleData" :props="defaultProps"
              @node-click="handleNodeClick"
              @check-change="handleCheckChange"
              node-key="id"
              :default-checked-keys="checkId">
            </el-tree>
          </div>
          </el-card>
          <div class="div-table">
            <el-table
              ref="multipleTable"
              :data="caseData"
              tooltip-effect="dark"
              style="width: 100%"
              @select="selectionOneCase"
              @select-all="selectionAllCases"
              >
              <el-table-column type="selection" width="55"> </el-table-column>
              <el-table-column prop="id" label="ID" width="80"> </el-table-column>
              <el-table-column prop="name" label="名称" show-overflow-tooltip> </el-table-column>
            </el-table>
          </div>
           
        </el-form-item>
        <el-form-item>
          <div class="dialog-footer">
            已选择【{{this.caseNum}}】条用例
            <el-button @click="cancelTask()">取消</el-button>
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
  import TaskApi from '../../request/task'
  // import CaseApi from '../../request/case'

  export default {
    props: ['tid', 'pid'],
    data() {
      return {
        showStatus: true,
        showTitle: '',
        moduleData: [],
        form: {
          id: 0,
          name: '',
          describe: '',
          cases: []
        },
         rules: {
          name: [
            { required: true, message: '请输入任务名称', trigger: 'blur' }
          ]
        },
        inResize: true,
        data:[],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        checkId: [],
        caseData: [],
        currentModuleId: 0,
        caseNum: 0
      }
    },
    created() {
      if (this.tid === 0) {
        this.showTitle = "创建任务"
      } else {
        this.showTitle = "编辑任务"
        this.getTask()
      }
      // 强制刷新
      this.inResize = false;
      this.$nextTick(() => {
        this.inResize = true;
      });
    },
    mounted() {
      this.initModuleTree()
    },
    methods: {
      handleCheckChange(data, checked) {
        if(data.id != undefined) {
          if(checked == true) {
            this.form.cases.push(data.id)
          } else {
            // this.form.cases.remove(data.id)
            // arr2.splice(1,2,'ttt'); 
            for (var i = 0; i < this.form.cases.length; i++) {
              if(this.form.cases[i] == data.id) {
                this.form.cases.splice(i, 1);
              }
            }
          }
        }
      },

      // 点击模块节点
      handleNodeClick(data) {
        console.log("click node", data)
        this.currentModuleId = data.id
        if (this.form.cases[data.id] == undefined) {
          this.form.cases[data.id] = []
        }
        this.getModuleCaseList(data.id)
      },

      async initModuleTree() {
        this.loading = true
        const resp = await ProjectApi.getModuleTree(this.pid)
        if (resp.success == true) {
          this.moduleData = JSON.parse(JSON.stringify(resp.data))
        } else {
          this.$message.error(resp.error.message)
        }
        this.loading = false
      },

      // 初始化用例数据
      async getModuleCaseList(mid) {
        
        this.caseLoading = true
        const query = { page: 1, size: 5}
        const resp = await ModuleApi.getModuleCases(mid, query)
        if (resp.success == true) {
          this.caseData = resp.data.caseList
          this.total = resp.data.total
          
          // 已经选中的用例
          this.$nextTick(() => {
            let rows = []
            for (let i = 0; i < this.form.cases[mid].length; i++) {
              for (let j = 0; j < this.caseData.length; j++) {
                if (this.form.cases[mid][i] == this.caseData[j].id) {
                  rows.push(this.caseData[j])
                }
              }
            }
            rows.forEach(row => {
              this.$refs.multipleTable.toggleRowSelection(row);
            });
          })

        } else {
          this.$message.error(resp.error.message);
        }
        this.caseLoading = false
      },

      // 选择所有用例
      selectionAllCases(val) {
        this.multipleSelection = val
        const moduleCases = []
        for (let i = 0; i < this.multipleSelection.length; i++) {
          moduleCases.push(this.multipleSelection[i].id)
        }
        this.form.cases[this.currentModuleId] =  moduleCases

        this.calculationCase()
      },

      // 选择一条用例
      selectionOneCase(val, row) {
        console.log("selection-one-change", val)
        console.log("selection-one-change", row)
        this.multipleSelection = val
        const moduleCases = []
        for (let i = 0; i < this.multipleSelection.length; i++) {
          moduleCases.push(this.multipleSelection[i].id)
        }
        this.form.cases[this.currentModuleId] =  moduleCases

        this.calculationCase()
      },

      // 计算用例数量
      calculationCase() {
        this.caseNum = 0
        for (let i = 0; i < this.form.cases.length; i++) {
          if (this.form.cases[i] != undefined) {
            this.caseNum += this.form.cases[i].length
          }
          // this.caseNum += this.form.cases[i].length
        }
      },

      // 获取一条任务信息
      async getTask() {
        const resp = await TaskApi.getTask(this.tid)
        if (resp.success == true) {
          this.form = resp.data
          this.checkId = resp.data.cases
        } else {
          this.$message.error(resp.error.message);
        }
      },

      // 关闭dialog
      cancelTask() {
        this.$emit('cancel', {})
      },

      // 创建任务按钮
      onSubmit(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            if(this.tid === 0) {
              console.log("adfasd", this.form)
              // TaskApi.createTask(this.form).then(resp => {
              //   if (resp.success == true) {
              //     this.$message.success("创建成功！")
              //     this.cancelTask()
              //   } else {
              //     this.$message.error("创建失败！");
              //   }
              // })
            } else {
              this.form.id = this.tid
              // TaskApi.updateTask(this.form).then(resp => {
              //   if (resp.success == true) {
              //     this.$message.success("更新成功！")
              //     this.cancelTask()
              //   } else {
              //     this.$message.error("更新失败！");
              //   }
              // })
            }
            
          } else {
            return false;
          }
        });
        
      },

    }

  }
</script>

<style>

</style>
<style scoped>
.dialog-footer {
  float: right;
}
.div-tree {
  height: 300px;
  overflow: auto;
  width: 30%;
  float: left;
}
.div-table {
  height: 300px;
  overflow: auto;
  width: 65%;
  float: right;
}
</style>