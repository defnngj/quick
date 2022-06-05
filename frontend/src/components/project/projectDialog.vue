<template>
  <div class="project-dialog">
    <el-dialog :title=showTitle :visible.sync="showStatus" @close="cancelProject()"  width="600px">
      <el-form v-if="inResize === true" :rules="rules" ref="form" :model="form" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input cy-data="project-name" v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input cy-data="project-desc" type="textarea" v-model="form.describe"></el-input>
        </el-form-item>
        <el-form-item label="图片" prop="image">
          <div id="image">
            <el-upload
              action="#"
              :before-upload="beforeUpload"
              list-type="picture-card"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              :file-list="fileList"
            >
              <i class="el-icon-plus"></i>
            </el-upload>
            <el-dialog :visible.sync="imageVisible">
              <img width="100%" :src="imageUrl" alt="" />
            </el-dialog>
          </div>
        </el-form-item>
        <el-form-item label="状态">
          <span style="float: left;">
            <el-switch cy-data="project-status" v-model="form.status"></el-switch>
          </span>
        </el-form-item>
        <el-form-item>
          <div class="dialog-footer">
            <el-button cy-data="cancel-project" @click="cancelProject()">取消</el-button>
            <el-button cy-data="save-project" type="primary" @click="onSubmit('form')">保存</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
  import ProjectApi from '../../request/project_v2'

  export default {
    props: ['pid'],
    data() {
      return {
        showStatus: true,
        showTitle: '',
        form: {
          name: '',
          describe: '',
          image: "",
          status: true
        },
         rules: {
          name: [
            { required: true, message: '请输入项目名称', trigger: 'blur' }
          ]
        },
        inResize: true,
        fileList: [],
        imageUrl: "",
        imageVisible: false
      }
    },
    created() {
      if (this.pid === 0) {
        this.showTitle = "创建项目"
      } else {
        this.showTitle = "编辑项目"
        this.getProject()
      }
      // 强制刷新
      this.inResize = false;
      this.$nextTick(() => {
        this.inResize = true;
      });
    },
    mounted() {
    //   this.initProject()
    },
    methods: {

      // 获取一条项目信息
      async getProject() {
        const resp = await ProjectApi.getProject(this.pid)
        if (resp.success == true) {
          
          this.form = resp.data
          var file_name = ""
          var file_path = ""
          if (resp.data.image === null) {
            file_name = "default.jpeg"
            file_path =  "static/images/default.jpeg"
          } else {
            file_name = resp.data.image
            file_path = "static/images/" + resp.data.image
          }

          this.fileList.push({
            name: file_name,
            url: file_path,
          })
        } else {
          this.$message.error(resp.error.message);
        }
      },

      // 关闭dialog
      cancelProject() {
        this.$emit('cancel', {})
      },

      // 创建项目按钮
      onSubmit(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            if(this.pid === 0) {
              ProjectApi.createProject(this.form).then(resp => {
                if (resp.success == true) {
                  this.$message.success("创建成功！")
                  this.cancelProject()
                } else {
                  this.$message.error("创建失败！");
                } 
              })
            } else {
              ProjectApi.updateProject(this.pid, this.form).then(resp => {
                if (resp.success == true) {
                  this.$message.success("更新成功！")
                  this.cancelProject()
                } else {
                  this.$message.error("更新失败！");
                }
              })
            }
            
          } else {
            return false;
          }
        });
        
      },

      // 删除图片
      handleRemove(file) {
        console.log("删除", file)
        this.fileList = []
      },

      // 预览图片
      handlePreview(file, fileList) {
        console.log("上传成功", file, fileList)
        this.imageUrl = file.url
        this.imageVisible = true
      },

      beforeUpload(file) {
        let fd = new FormData()
        fd.append("file", file)

        ProjectApi.updateProjectImage(fd).then((resp) => {
          if (resp.data.success === true) {
            this.form.image = resp.data.data.name
            const imagePath = "/static/images/" + resp.data.data.name
            this.fileList.push({
              name: file.name,
              url: imagePath,
            })
            this.$message.success("上传成功！")
          } else {
            console.log("上传失败", resp)
            this.$message.error(resp.error.message)
          }
        })
        return true
      }

    }

  }
</script>

<style scoped>
.dialog-footer {
  float: right;
}
</style>