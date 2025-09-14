<template>
  <div class="chat-container">
    <ChatSidebar 
      :chats="chatList" 
      :active-chat="activeChat" 
      @select="setActiveChat" 
      @create-chat="createNewChat"
    />

    <ChatMain 
      :chatId="chatList[activeChat].id"
      :chatName="chatList[activeChat].name"
      v-model:chatId="chatList[activeChat].id"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from '../app/api'

import ChatSidebar from "../components/ChatSidebar.vue";
import ChatMain from "../components/ChatMain.vue";

const router = useRouter();

const chatList = ref([{name: "", id: 0}]);

const activeChat = ref(0);

const setActiveChat = (index) => {
  activeChat.value = index;
};

const createNewChat = () => {
  chatList.value.push({ id: -1, name: "New chat"});
  activeChat.value = chatList.value.length - 1;
};

onMounted(async () => {
  try {
    const response = await api.get(`/chats/me`)
    chatList.value = response.data
  } catch(e) {
    if(e.status == 401) {
      router.push("/login");
    } else {
      console.error(e)
    }
  }
})
</script>

<style scoped>
.chat-container {
  display: flex;
  height: 100vh;
  background: #111;
  color: #eee;
}
@media (max-width: 768px) {
  .chat-container {
    flex-direction: column;
  }
}
</style>
