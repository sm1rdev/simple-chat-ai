<template>
  <main class="chat-main">
    <header class="chat-header">
      <h3>{{ chatName }}</h3>
    </header>

    <section class="chat-messages">
      <ChatMessage 
        v-for="msg in messages" 
        :key="msg.key"
        :message="msg"
      />
    </section>

    <footer class="chat-input">
      <input 
        v-model="localMessage" 
        type="text" 
        placeholder="Type a message..." 
        @keyup.enter="handleSend" 
      />
      <button @click="handleSend">➤</button>
    </footer>
  </main>
</template>

<script setup>
import api from '../app/api'
import { ref, watch, onMounted } from "vue";
import ChatMessage from "./ChatMessage.vue";

const props = defineProps({
  chatName: {
    type: String,
    default: "New Chat"
  },
  chatId: {
      type: Number,
      required: true
  }
});

const emit = defineEmits(["update:chatId"]);

const messages = ref([]);
let messageId = 10000000000;

const localMessage = ref("");

let eventSource = null;

const loadMessages = async (id) => {
  if (id <= 0) {
    messages.value = []
    return
  }

  console.log("Loading messages for chat:", id);

  try {
    const response = await api.get(`/chats/${id}/messages/`);
    messages.value = response.data.map(msg => ({
          key: msg.id,
          data: msg.data,
          from: msg.from_user
    }));
  } catch(e) {
    console.error(e);
  }
};

onMounted(() => {
  loadMessages(props.chatId);
});

watch(
  () => props.chatId,
  (newId) => {
    loadMessages(newId);
  }
);

const handleSend = async () => {
  messageId += 1

  const text = localMessage.value.trim();
  if (!text) return;

  messages.value.push({ key: messageId, data: text, from: "me" });

  let currentChatId = props.chatId;

  if(currentChatId == -1) {
    try {
      const response = await api.post(`/chats/`, {"name": text})
      currentChatId = response.data["id"]
      emit("update:chatId", currentChatId)
    } catch(e) {
      console.log(e)
    }
  }

  try {
    const response = await api.post(`/chats/${currentChatId}/messages/`, {"data": text, "from_user": "me"})
  } catch(e) {
    console.error(e)
  }

  messageId += 1

  messages.value.push({ key: messageId, data: "", from: "other" });

  initSSE(currentChatId);

  console.log(messages.value)

  localMessage.value = "";
};

const initSSE = (chatId) => {
  if (eventSource) eventSource.close();

  eventSource = new EventSource(
    `http://127.0.0.1:8000/events/openai?chat_id=${encodeURIComponent(chatId)}`
  );

  let sseContent = "";

  eventSource.onopen = () => console.log("SSE connected.");

  eventSource.onmessage = (event) => {
    messages.value[messages.value.length - 1].data += event.data;
    sseContent += event.data;
  };

  eventSource.onerror = async (err) => {
    eventSource.close();
    console.log("SSE disconnected. Save data.");
    try {
      const response = await api.post(`/chats/${props.chatId}/messages/`, {"data": sseContent, "from_user": "other"})
    } catch(e) {
      console.error(e)
    }
  };
};
</script>

<style scoped>
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chat-header {
  padding: 1rem;
  border-bottom: 1px solid #333;
  background: #1a1a1a;
}

.chat-messages {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
}
.chat-input {
  display: flex;
  border-top: 1px solid #333;
  padding: 0.5rem;
  background: #1a1a1a;
}

.chat-input input {
  flex: 1;
  padding: 0.5rem;
  border: none;
  border-radius: 8px;
  outline: none;
  background: #2a2a2a;
  color: #eee;
}

.chat-input button {
  margin-left: 0.5rem;
  padding: 0 1rem;
  background: #a855f7;
  border: none;
  border-radius: 8px;
  color: #fff;
  cursor: pointer;
}

.chat-input button:hover {
  background: #9333ea;
}
</style>
