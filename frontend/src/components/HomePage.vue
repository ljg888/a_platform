<template>
  <div class="home-container">
    <div class="banner">
      <div class="banner-content">
        <span>欢迎使用模型测试平台！</span>
        <span>今日推荐：尝试新的卷积神经网络模型</span>
        <span>当前用户：测试工程师</span>
      </div>
    </div>
    
    <div class="main-content">
      <div class="sidebar">
        <div class="menu">
          <div class="menu-item" :class="{active: activeMenu === 'test'}" @click="activeMenu = 'test'">
            测试配置
          </div>
          <div class="menu-item" :class="{active: activeMenu === 'results'}" @click="activeMenu = 'results'">
            测试结果
          </div>
        </div>
      </div>

      <div class="content">
        <div v-if="activeMenu === 'test'">
          <TestConfigForm />
        </div>
        <div v-if="activeMenu === 'results'">
          <TestResults />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TestConfigForm from './TestConfigForm.vue';
import TestResults from './TestResults.vue';

export default {
  name: 'HomePage',
  components: {
    TestConfigForm,
    TestResults
  },
  data() {
    return {
      showForm: false,
      configs: [],
      activeMenu: 'test'
    }
  },
  methods: {
    async getConfigs() {
      try {
        const response = await fetch('http://localhost:5000/api/configs');
        const data = await response.json();
        this.configs = data.configs;
      } catch (error) {
        console.error('获取配置列表失败:', error);
      }
    },
    async getResults() {
      try {
        const response = await fetch('http://localhost:5000/api/results');
        const data = await response.json();
        this.results = data.results;
      } catch (error) {
        console.error('获取测试结果失败:', error);
      }
    }
  },
  watch: {
    activeMenu(newVal) {
      if (newVal === 'results') {
        this.getResults();
      }
    }
  }
}
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  display: flex;
  flex: 1;
}

.banner {
  width: 100%;
  background-color: #42b983;
  color: white;
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.banner-content {
  display: flex;
  gap: 30px;
  font-size: 14px;
}

.sidebar {
  width: 200px;
  background-color: #f5f5f5;
  padding: 20px;
  border-right: 1px solid #ddd;
}

.menu {
  display: flex;
  flex-direction: column;
}

.menu-item {
  padding: 12px;
  margin: 4px 0;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.menu-item:hover {
  background-color: #e9e9e9;
}

.menu-item.active {
  background-color: #42b983;
  color: white;
}

.content {
  flex: 1;
  padding: 20px;
}

.config-container {
  margin-top: 20px;
  position: relative;
}

.create-btn {
  position: absolute;
  top: 0;
  left: 0;
  margin-bottom: 20px;
  background-color: #42b983;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.create-btn:hover {
  background-color: #3aa876;
}

.config-table {
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f5f5f5;
}

tr:hover {
  background-color: #f9f9f9;
}
</style>
