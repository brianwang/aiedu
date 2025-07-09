<template>
  <div class="ai-learning-page">
    <div class="page-header">
      <h1>🤖 AI智能学习助手</h1>
      <p>让AI成为您的专属学习伙伴，提供个性化学习体验</p>
    </div>

    <!-- AI服务状态 -->
    <div class="ai-status-card">
      <div
        class="status-indicator"
        :class="{
          online: aiStatus.ai_available,
          offline: !aiStatus.ai_available,
        }"
      >
        <span class="status-dot"></span>
        {{ aiStatus.ai_available ? "AI服务在线" : "AI服务离线" }}
      </div>
      <div class="status-details">
        <span>客户端数量: {{ aiStatus.clients_count }}</span>
        <span>缓存状态: {{ aiStatus.cache_enabled ? "启用" : "禁用" }}</span>
      </div>
    </div>

    <!-- 功能导航 -->
    <div class="feature-grid">
      <div class="feature-card" @click="activeTab = 'qa'">
        <div class="feature-icon">💬</div>
        <h3>智能问答</h3>
        <p>实时AI问答，解答学习疑惑</p>
      </div>

      <div class="feature-card" @click="activeTab = 'voice'">
        <div class="feature-icon">🎤</div>
        <h3>语音交互</h3>
        <p>语音识别与合成，解放双手</p>
      </div>

      <div class="feature-card" @click="activeTab = 'analysis'">
        <div class="feature-icon">📊</div>
        <h3>学习分析</h3>
        <p>深度分析学习数据，提供建议</p>
      </div>

      <div class="feature-card" @click="activeTab = 'grading'">
        <div class="feature-icon">✍️</div>
        <h3>智能评分</h3>
        <p>AI智能评分，详细反馈</p>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="content-area">
      <!-- 智能问答 -->
      <div v-if="activeTab === 'qa'" class="qa-section">
        <div class="chat-container">
          <div class="chat-messages" ref="chatMessages">
            <div
              v-for="(message, index) in chatMessages"
              :key="index"
              class="message"
              :class="message.type"
            >
              <div class="message-content">
                <div class="message-text">{{ message.content }}</div>
                <div class="message-time">
                  {{ formatTime(message.timestamp) }}
                </div>
              </div>
            </div>
          </div>

          <div class="chat-input">
            <textarea
              v-model="questionInput"
              placeholder="请输入您的问题..."
              @keydown.enter.prevent="sendQuestion"
              rows="3"
            ></textarea>
            <button @click="sendQuestion" :disabled="!questionInput.trim()">
              发送
            </button>
          </div>
        </div>
      </div>

      <!-- 语音交互 -->
      <div v-if="activeTab === 'voice'" class="voice-section">
        <div class="voice-controls">
          <div class="voice-card">
            <h3>语音转文字</h3>
            <div class="voice-input">
              <button @click="startRecording" :disabled="isRecording">
                {{ isRecording ? "录音中..." : "开始录音" }}
              </button>
              <button @click="stopRecording" :disabled="!isRecording">
                停止录音
              </button>
            </div>
            <div v-if="transcribedText" class="transcription">
              <h4>识别结果:</h4>
              <p>{{ transcribedText }}</p>
            </div>
          </div>

          <div class="voice-card">
            <h3>文字转语音</h3>
            <div class="tts-input">
              <textarea
                v-model="ttsText"
                placeholder="输入要转换的文字..."
                rows="4"
              ></textarea>
              <button @click="textToSpeech" :disabled="!ttsText.trim()">
                转换为语音
              </button>
            </div>
            <div v-if="audioUrl" class="audio-player">
              <audio controls :src="audioUrl"></audio>
            </div>
          </div>
        </div>
      </div>

      <!-- 学习分析 -->
      <div v-if="activeTab === 'analysis'" class="analysis-section">
        <div class="analysis-grid">
          <div class="analysis-card">
            <h3>学习报告</h3>
            <div v-if="learningReport" class="report-content">
              <div class="report-item">
                <span class="label">学习时长:</span>
                <span class="value"
                  >{{ learningReport.total_study_time }}分钟</span
                >
              </div>
              <div class="report-item">
                <span class="label">答题数量:</span>
                <span class="value">{{ learningReport.total_questions }}</span>
              </div>
              <div class="report-item">
                <span class="label">正确率:</span>
                <span class="value">{{ learningReport.accuracy }}%</span>
              </div>
              <div class="report-item">
                <span class="label">学习建议:</span>
                <span class="value">{{ learningReport.suggestions }}</span>
              </div>
            </div>
            <button @click="generateLearningReport">生成报告</button>
          </div>

          <div class="analysis-card">
            <h3>学习风格</h3>
            <div v-if="learningStyle" class="style-content">
              <div class="style-item">
                <span class="label">学习类型:</span>
                <span class="value">{{ learningStyle.style_type }}</span>
              </div>
              <div class="style-item">
                <span class="label">特点:</span>
                <ul class="characteristics">
                  <li v-for="char in learningStyle.characteristics" :key="char">
                    {{ char }}
                  </li>
                </ul>
              </div>
            </div>
            <button @click="analyzeLearningStyle">分析风格</button>
          </div>

          <div class="analysis-card">
            <h3>学习激励</h3>
            <div v-if="learningMotivation" class="motivation-content">
              <div class="motivation-message">
                {{ learningMotivation.encouragement_message }}
              </div>
              <div class="motivation-tips">
                <h4>学习建议:</h4>
                <ul>
                  <li
                    v-for="tip in learningMotivation.learning_tips"
                    :key="tip"
                  >
                    {{ tip }}
                  </li>
                </ul>
              </div>
            </div>
            <button @click="getLearningMotivation">获取激励</button>
          </div>
        </div>
      </div>

      <!-- 智能评分 -->
      <div v-if="activeTab === 'grading'" class="grading-section">
        <div class="grading-form">
          <h3>智能评分测试</h3>
          <div class="form-group">
            <label>题目内容:</label>
            <textarea
              v-model="gradingData.question_content"
              rows="3"
            ></textarea>
          </div>
          <div class="form-group">
            <label>标准答案:</label>
            <textarea v-model="gradingData.standard_answer" rows="2"></textarea>
          </div>
          <div class="form-group">
            <label>学生答案:</label>
            <textarea v-model="gradingData.student_answer" rows="2"></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>题目类型:</label>
              <select v-model="gradingData.question_type">
                <option value="single_choice">单选题</option>
                <option value="multiple_choice">多选题</option>
                <option value="fill_blank">填空题</option>
                <option value="short_answer">简答题</option>
              </select>
            </div>
            <div class="form-group">
              <label>满分:</label>
              <input
                type="number"
                v-model="gradingData.max_score"
                min="1"
                max="100"
              />
            </div>
          </div>
          <button @click="performGrading">开始评分</button>
        </div>

        <div v-if="gradingResult" class="grading-result">
          <h3>评分结果</h3>
          <div class="score-breakdown">
            <div class="score-item">
              <span class="score-label">总分:</span>
              <span class="score-value"
                >{{ gradingResult.score }}/{{ gradingData.max_score }}</span
              >
            </div>
            <div class="score-item">
              <span class="score-label">内容准确性:</span>
              <span class="score-value"
                >{{ gradingResult.accuracy_score }}%</span
              >
            </div>
            <div class="score-item">
              <span class="score-label">逻辑完整性:</span>
              <span class="score-value">{{ gradingResult.logic_score }}%</span>
            </div>
            <div class="score-item">
              <span class="score-label">表达规范性:</span>
              <span class="score-value"
                >{{ gradingResult.expression_score }}%</span
              >
            </div>
          </div>

          <div class="feedback-section">
            <h4>详细反馈</h4>
            <div class="feedback-item">
              <h5>优点:</h5>
              <ul>
                <li
                  v-for="strength in gradingResult.detailed_feedback.strengths"
                  :key="strength"
                >
                  {{ strength }}
                </li>
              </ul>
            </div>
            <div class="feedback-item">
              <h5>不足:</h5>
              <ul>
                <li
                  v-for="weakness in gradingResult.detailed_feedback.weaknesses"
                  :key="weakness"
                >
                  {{ weakness }}
                </li>
              </ul>
            </div>
            <div class="feedback-item">
              <h5>改进建议:</h5>
              <ul>
                <li
                  v-for="suggestion in gradingResult.detailed_feedback
                    .improvement_suggestions"
                  :key="suggestion"
                >
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </div>

          <div class="encouragement">
            <p>{{ gradingResult.encouragement }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import aiApi from "@/api/ai";

// 响应式数据
const activeTab = ref("qa");
const aiStatus = ref({
  ai_available: false,
  clients_count: 0,
  cache_enabled: false,
  cache_size: 0,
});

// 聊天相关
const chatMessages = ref([]);
const questionInput = ref("");

// 语音相关
const isRecording = ref(false);
const transcribedText = ref("");
const ttsText = ref("");
const audioUrl = ref("");

// 分析相关
const learningReport = ref(null);
const learningStyle = ref(null);
const learningMotivation = ref(null);

// 评分相关
const gradingData = ref({
  question_content: "",
  standard_answer: "",
  student_answer: "",
  question_type: "single_choice",
  max_score: 10,
});
const gradingResult = ref(null);

// 方法
const checkAIStatus = async () => {
  try {
    const response = await aiApi.getStatus();
    aiStatus.value = response;
  } catch (error) {
    console.error("检查AI状态失败:", error);
  }
};

const sendQuestion = async () => {
  if (!questionInput.value.trim()) return;

  const question = questionInput.value;
  questionInput.value = "";

  // 添加用户消息
  chatMessages.value.push({
    type: "user",
    content: question,
    timestamp: new Date(),
  });

  try {
    const response = await aiApi.realTimeQA({
      question: question,
      context: "",
      user_level: "intermediate",
    });

    // 添加AI回复
    chatMessages.value.push({
      type: "ai",
      content: response.answer,
      timestamp: new Date(),
    });
  } catch (error) {
    chatMessages.value.push({
      type: "ai",
      content: "抱歉，AI服务暂时不可用，请稍后重试。",
      timestamp: new Date(),
    });
  }

  // 滚动到底部
  await nextTick();
  const chatContainer = document.querySelector(".chat-messages");
  if (chatContainer) {
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }
};

const startRecording = () => {
  isRecording.value = true;
  // 这里应该实现实际的录音功能
  setTimeout(() => {
    stopRecording();
  }, 5000); // 5秒后自动停止
};

const stopRecording = async () => {
  isRecording.value = false;
  // 模拟语音识别结果
  transcribedText.value = "这是语音识别的示例文本";
};

const textToSpeech = async () => {
  try {
    const response = await aiApi.textToSpeech({
      text: ttsText.value,
      voice: "zh-CN-XiaoxiaoNeural",
    });

    // 这里应该处理音频数据
    audioUrl.value = "data:audio/wav;base64," + response.audio_data;
  } catch (error) {
    console.error("文字转语音失败:", error);
  }
};

const generateLearningReport = async () => {
  try {
    const response = await aiApi.generateLearningReport();
    learningReport.value = response;
  } catch (error) {
    console.error("生成学习报告失败:", error);
  }
};

const analyzeLearningStyle = async () => {
  try {
    const response = await aiApi.analyzeLearningStyle();
    learningStyle.value = response;
  } catch (error) {
    console.error("分析学习风格失败:", error);
  }
};

const getLearningMotivation = async () => {
  try {
    const response = await aiApi.getLearningMotivation();
    learningMotivation.value = response;
  } catch (error) {
    console.error("获取学习激励失败:", error);
  }
};

const performGrading = async () => {
  try {
    const response = await aiApi.smartGrading(gradingData.value);
    gradingResult.value = response;
  } catch (error) {
    console.error("智能评分失败:", error);
  }
};

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString();
};

// 生命周期
onMounted(() => {
  checkAIStatus();
});
</script>

<style scoped>
.ai-learning-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.page-header p {
  font-size: 1.1rem;
  color: #7f8c8d;
}

.ai-status-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  border-radius: 15px;
  margin-bottom: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #2ecc71;
}

.status-dot.offline {
  background: #e74c3c;
}

.status-details {
  display: flex;
  gap: 20px;
  font-size: 0.9rem;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.feature-card {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.feature-card h3 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.feature-card p {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.content-area {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* 聊天界面样式 */
.qa-section {
  padding: 20px;
}

.chat-container {
  height: 500px;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
  margin-bottom: 20px;
}

.message {
  margin-bottom: 15px;
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message.ai {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 15px;
  position: relative;
}

.message.user .message-content {
  background: #007bff;
  color: white;
}

.message.ai .message-content {
  background: white;
  border: 1px solid #e9ecef;
}

.message-time {
  font-size: 0.8rem;
  opacity: 0.7;
  margin-top: 5px;
}

.chat-input {
  display: flex;
  gap: 10px;
}

.chat-input textarea {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: none;
}

.chat-input button {
  padding: 12px 24px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.chat-input button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

/* 语音界面样式 */
.voice-section {
  padding: 20px;
}

.voice-controls {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.voice-card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
}

.voice-input,
.tts-input {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 15px;
}

.voice-input button,
.tts-input button {
  padding: 10px 20px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.voice-input button:disabled,
.tts-input button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.tts-input textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  resize: none;
}

.transcription,
.audio-player {
  margin-top: 15px;
  padding: 15px;
  background: white;
  border-radius: 5px;
}

/* 分析界面样式 */
.analysis-section {
  padding: 20px;
}

.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.analysis-card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
}

.analysis-card h3 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.report-item,
.style-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  padding: 8px 0;
  border-bottom: 1px solid #e9ecef;
}

.characteristics {
  list-style: none;
  padding: 0;
}

.characteristics li {
  padding: 5px 0;
  color: #495057;
}

.motivation-message {
  background: #e3f2fd;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
  font-style: italic;
}

.motivation-tips ul {
  list-style: none;
  padding: 0;
}

.motivation-tips li {
  padding: 5px 0;
  color: #495057;
}

.analysis-card button {
  width: 100%;
  padding: 10px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 15px;
}

/* 评分界面样式 */
.grading-section {
  padding: 20px;
}

.grading-form {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #2c3e50;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.grading-form button {
  width: 100%;
  padding: 12px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.grading-result {
  background: white;
  padding: 20px;
  border-radius: 10px;
  border: 2px solid #28a745;
}

.score-breakdown {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.score-item {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 5px;
}

.score-value {
  font-weight: 600;
  color: #28a745;
}

.feedback-section {
  margin-bottom: 20px;
}

.feedback-item {
  margin-bottom: 15px;
}

.feedback-item h5 {
  color: #2c3e50;
  margin-bottom: 8px;
}

.feedback-item ul {
  list-style: none;
  padding: 0;
}

.feedback-item li {
  padding: 5px 0;
  color: #495057;
}

.encouragement {
  background: #e8f5e8;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  font-style: italic;
  color: #28a745;
}

@media (max-width: 768px) {
  .voice-controls {
    grid-template-columns: 1fr;
  }

  .analysis-grid {
    grid-template-columns: 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .score-breakdown {
    grid-template-columns: 1fr;
  }
}
</style>
