<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const showModal = ref(false)
const configs = ref([])
const modelPath = ref('')
const datasetPath = ref('')
const selectedProject = ref('')
const projects = ref([])

// 获取项目列表
axios.get('http://localhost:5000/api/projects')
  .then(response => {
    projects.value = response.data.projects
  })

// 获取配置列表
const getConfigs = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/configs')
    configs.value = response.data.configs
  } catch (error) {
    console.error('获取配置列表失败:', error)
  }
}

// 提交表单
const submitForm = async () => {
  try {
    await axios.post('http://localhost:5000/api/submit', {
      model_path: modelPath.value,
      dataset_path: datasetPath.value,
      project: selectedProject.value
    })
    showModal.value = false
    getConfigs()
  } catch (error) {
    alert('提交失败：' + error.response.data.error)
  }
}

// 删除配置
const deleteConfig = async (id) => {
  try {
    await axios.delete(`http://localhost:5000/api/configs/${id}`)
    getConfigs()
  } catch (error) {
    alert('删除失败：' + error.response.data.error)
  }
}

// 运行配置
const runConfig = async (id) => {
  try {
    await axios.post(`http://localhost:5000/api/configs/${id}/run`)
    alert('运行配置成功')
  } catch (error) {
    alert('运行失败：' + error.response.data.error)
  }
}

// 组件挂载时获取配置
onMounted(() => {
  getConfigs()
})
</script>

<template>
  <div>
    <div class="config-table">
      <div class="table-header">
        <button class="create-btn" @click="showModal = true">创建模型测试配置</button>
        <button class="refresh-btn" @click="getConfigs">
          <span class="icon">⟳</span> 刷新
        </button>
      </div>
      <table>
        <thead>
          <tr>
            <th>项目名称</th>
            <th>模型路径</th>
            <th>测试集路径</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(config, index) in configs" :key="config.id" :class="{ even: index % 2 === 0 }">
            <td>{{ config.project }}</td>
            <td>{{ config.model_path }}</td>
            <td>{{ config.dataset_path }}</td>
            <td>{{ config.created_at }}</td>
            <td>
              <button class="run-btn" @click="runConfig(config.id)">运行</button>
              <button class="delete-btn" @click="deleteConfig(config.id)">删除</button>
            </td>
          </tr>
          <tr v-if="configs.length === 0">
            <td colspan="5" class="empty">暂无数据</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div v-if="showModal" class="modal-overlay">
      <div class="form-container">
        <h2>测试配置</h2>
        <div class="form-item">
          <label>模型路径：</label>
          <input v-model="modelPath" type="text" />
        </div>
        <div class="form-item">
          <label>测试集路径：</label>
          <input v-model="datasetPath" type="text" />
        </div>
        <div class="form-item">
          <label>选择项目：</label>
          <select v-model="selectedProject">
            <option v-for="project in projects" :key="project">{{ project }}</option>
          </select>
        </div>
        <button @click="submitForm">提交配置</button>
        <button class="cancel-btn" @click="showModal = false">取消</button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.create-btn {
  background-color: #42b983;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 200px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.2s;

  &:hover {
    background-color: #3aa876;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  }
}

.config-table {
  margin: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;

  .table-header {
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .refresh-btn {
    background-color: #42b983;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;

    .icon {
      margin-right: 5px;
    }

    &:hover {
      background-color: #3aa876;
    }
  }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
      table-layout: fixed;

      th {
        background-color: #f8f9fa;
        color: #495057;
        font-weight: 600;
        padding: 12px 16px;
        text-align: left;
        border-bottom: 2px solid #e9ecef;
      }

      th:nth-child(1) { width: 20%; }
      th:nth-child(2) { width: 25%; }
      th:nth-child(3) { width: 25%; }
      th:nth-child(4) { width: 20%; }
      th:nth-child(5) { width: 10%; }

      td {
        padding: 12px 16px;
        border-bottom: 1px solid #e9ecef;
        text-align: left;
        word-wrap: break-word;
      }

    tr {
      transition: background-color 0.2s;

      &:hover {
        background-color: #f8f9fa;
      }

      &.even {
        background-color: #f8f9fa;
      }
    }

    .empty {
      text-align: center;
      color: #6c757d;
      padding: 20px;
    }

    .run-btn {
      background-color: #4287f5;
      color: white;
      padding: 6px 12px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      margin-right: 5px;
      transition: all 0.2s;

      &:hover {
        background-color: #3a76d4;
      }
    }

    .delete-btn {
      background-color: #ff4444;
      color: white;
      padding: 6px 12px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.2s;

      &:hover {
        background-color: #cc0000;
      }
    }
  }
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-container {
  position: relative;
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;

  h2 {
    color: #2c3e50;
    margin-bottom: 20px;
  }

  .form-item {
    margin-bottom: 15px;

    label {
      display: inline-block;
      width: 120px;
      margin-right: 10px;
    }

    input, select {
      width: 300px;
      padding: 8px;
      border: 1px solid #ddd;
      border-radius: 4px;
    }
  }

  .cancel-btn {
    background-color: #ff4444;
    margin-left: 10px;
    
    &:hover {
      background-color: #cc0000;
    }
  }

  button {
    background-color: #42b983;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 15px;

    &:hover {
      background-color: #3aa876;
    }
  }
}
</style>
