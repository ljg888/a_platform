<script setup>
import { ref } from 'vue'
import axios from 'axios'

const results = ref([])
const selectedProject = ref('')
const projects = ref([])
const selectedResult = ref(null)

// 获取项目列表
const fetchProjects = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/configs')
    projects.value = [...new Set(response.data.configs.map(c => c.project))]
    // if (projects.value.length > 0) {
    //   selectedProject.value = projects.value[0]
    //   fetchResults()
    // }
  } catch (error) {
    console.error('获取项目失败:', error)
  }
}

// 获取测试结果
const fetchResults = async () => {
  if (!selectedProject.value) return
  
  try {
    const response = await axios.get('http://localhost:5000/api/results', {
      params: { project: selectedProject.value }
    })
    results.value = response.data.results
    if (results.value.length > 0) {
      selectedResult.value = results.value[0]
    }
  } catch (error) {
    console.error('获取结果失败:', error)
  }
}

// 初始化获取数据
fetchProjects()
</script>

<template>
  <div class="results-container">
    <div class="header">
      <h2>测试结果</h2>
      <div class="project-selector">
        <label>选择项目：</label>
        <select v-model="selectedProject" @change="fetchResults">
          <option v-for="project in projects" :key="project" :value="project">
            {{ project }}
          </option>
        </select>
      </div>
    </div>

    <div class="result-view">
      <div class="result-list">
        <div 
          v-for="(item, index) in results" 
          :key="index" 
          class="result-item"
          :class="{ active: selectedResult === item }"
          @click="selectedResult = item"
        >
          <div class="item-info">
            <div class="filename">{{ item.filename }}</div>
            <div class="timestamp">{{ item.filename.replace('.html', '') }}</div>
          </div>
        </div>
      </div>

      <div class="result-content">
        <iframe 
          v-if="selectedResult"
          :src="`data:text/html;charset=utf-8,${encodeURIComponent(selectedResult.content)}`"
          frameborder="0"
          class="report-frame"
        ></iframe>
        <div v-else class="no-result">
          请从左侧选择测试报告
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.results-container {
  height: calc(100vh - 100px);
  padding: 20px;

  .header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;

    h2 {
      color: #2c3e50;
      margin: 0 20px 0 0;
    }

    .project-selector {
      display: flex;
      align-items: center;

      label {
        margin-right: 10px;
        font-size: 14px;
        color: #666;
      }

      select {
        padding: 6px 12px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 14px;
      }
    }
  }

  .result-view {
    display: flex;
    height: calc(100% - 60px);
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;

    .result-list {
      width: 300px;
      border-right: 1px solid #ddd;
      overflow-y: auto;

      .result-item {
        padding: 12px;
        border-bottom: 1px solid #eee;
        cursor: pointer;
        transition: background-color 0.2s;

        &:hover {
          background-color: #f5f5f5;
        }

        &.active {
          background-color: #e8f0fe;
        }

        .item-info {
          .filename {
            font-size: 14px;
            color: #333;
            margin-bottom: 4px;
          }

          .timestamp {
            font-size: 12px;
            color: #666;
          }
        }
      }
    }

    .result-content {
      flex: 1;
      position: relative;

      .report-frame {
        width: 100%;
        height: 100%;
        border: none;
      }

      .no-result {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #999;
        font-size: 14px;
      }
    }
  }
}
</style>
