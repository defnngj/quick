<template>
  <div class="module">
    <div style="height: 30px;">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>模块管理</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <el-card class="box-card">
      <!-- 模块树 -->
      <div class="module-tree">
        <el-select v-model="projectId" filterable placeholder="选择项目" @change="selectProject">
          <el-option
            v-for="item in projectOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        <div class="node-create">
          <span style="float: right">
            <el-button type="text" plain size="mini" icon="el-icon-circle-plus-outline" @click="showCreate()">根节点</el-button>
          </span>
        </div>
        <el-tree
          :data="moduleData"
          show-checkbox
          node-key="id"
          :default-expand-all="switchTree"
          :expand-on-click-node="false"
          @node-click="handleNodeClick">
          <span class="custom-tree-node" slot-scope="{ node, data }">
            <span>{{ node.label }}</span>
            <span>
              <el-button
                type="text"
                size="mini"
                @click="() => append(data)"
                icon="el-icon-circle-plus-outline">
              </el-button>
              <el-button
                type="text"
                size="mini"
                @click="() => remove(node, data)"
                icon="el-icon-delete">
              </el-button>
            </span>
          </span>
        </el-tree>
      </div>
    </el-card>
    <ModuleDialog v-if="showDailog" :mid=moduleId :pid=projectId @cancel="cancelModule"></ModuleDialog>
  </div>
</template>

<script>
import ProjectApi from '../../request/project'
import ModuleApi from '../../request/module'
import ModuleDialog from './ModuleDialog.vue'
  let id = 1000;

  export default {
    components: {
      ModuleDialog
    },
    data(){
      return {
        loading: false,
        moduleId: 0,
        tableData: [],
        showDailog: false,
        total: 0,
        query: {
          page: 1,
          size: 5,
        },
        projectId: 1,
        projectOptions: [],
        moduleData: [],
        switchTree: false,
        

      }
    },
    created() {
    },
    mounted() {
      this.initProject()
    },
    methods: {
      // 初始化项目列表
      async initProject() {
        this.loading = true
        const pQuery = {
          page: 1,
          size: 1000,
        }
        const resp = await ProjectApi.getProjects(pQuery)
        if (resp.success == true) {
          const projectData = resp.data.projectList
          this.projectOptions = []
          for (let i = 0; i < projectData.length; i++) {
            this.projectOptions.push({
              value: projectData[i].id,
              label: projectData[i].name
            })
          }
          this.projectId = this.projectOptions[0].value
          this.initModuleTree()
        } else {
          this.$message.error(resp.error.message);
        }
        this.loading = false
      },

      // 选择一个项目
      async selectProject(val) {
        this.projectId = val
        await this.initModuleTree()
      },

      // 初始化模块树
      async initModuleTree() {
        this.loading = true
        const resp = await ModuleApi.getModuleTree(this.projectId)
        if (resp.success == true) {
          this.moduleData = JSON.parse(JSON.stringify(resp.data))
        } else {
          this.$message.error(resp.error.message);
        }
        this.loading = false
      },

      // 添加根节点
      showCreate() {
        this.showDailog = true
      },

      // 展开收起节点
      switchNode() {
        console.log("switchNode", this.switchTree)
        if (this.switchTree === false) {
          this.switchTree = true
        } else {
          this.switchTree = false
        }
      },

      // 显示编辑窗口
      showEdit(row) {
        this.moduleId = row.id
        this.showDailog = true
      },

      // 删除一条项目信息
      async deleteModule(row) {
        this.$confirm('是否要删除模块?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          ModuleApi.deleteModule(row.id).then(resp =>{
            if (resp.success == true) {
              this.$message.success("删除成功！")
              this.initModuleTree()
            } else {
              this.$message.error("删除失败");
            }
          })
          
        })        
      },

      // 子组件的回调
      cancelModule() {
        this.showDailog = false
        this.moduleId = 0
        this.initModuleTree()
      },

      // 添加子节点
      append(data) {
        const newChild = { id: id++, label: 'testtest', children: [] };
        if (!data.children) {
          this.$set(data, 'children', []);
        }
        data.children.push(newChild);
      },

      // 删除子节点
      remove(node, data) {
        const parent = node.parent;
        const children = parent.data.children || parent.data;
        const index = children.findIndex(d => d.id === data.id);
        children.splice(index, 1);
      },

      //点击节点
      handleNodeClick(data) {
        console.log("click node", data)
      }

    }

  }
</script>

<style scoped>
.filter-line {
  height: 50px;
  text-align: left;
}
.foot-page {
  margin-top: 20px;
  float: right;
  margin-bottom: 20px;
  
}
.module-tree {
  /* width: 200px; */
  height: 600px;
  float: left;
  overflow: auto;
}
.node-create {
  margin-top: 5px;
  margin-bottom: 5px;
  text-align: left;
  height: 28px;
}
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}
.module-tree /deep/ .el-tree-node.is-expanded > .el-tree-node__children {
  display: inline;
}
</style>