<template>
  <aside class="chat-sidebar">
    <h2 class="chat-title">
      Chats
    </h2>
    <button class="add-chat" @click="emit('create-chat')">Create new chat</button>
    <ul>
      <li 
        v-for="(chat, index) in chats" 
        :key="index" 
        :class="{ active: activeChat === index }"
        @click="$emit('select', index)"
      >
        {{ chat.name }}
      </li>
    </ul>
  </aside>
</template>

<script setup>
defineProps({
  chats: Array,
  activeChat: Number
});

const emit = defineEmits(["create-chat"]);

</script>

<style scoped>
.chat-sidebar {
  width: 260px;
  background: #1a1a1a;
  border-right: 1px solid #333;
  padding: 1rem;
}

.chat-title {
  margin-bottom: 1rem;
  font-size: 1.2rem;
  color: #a855f7;
}

.chat-sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
  overflow-y: auto;
}

.chat-sidebar li {
  background: #333;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.chat-sidebar li:hover {
  background: #2a2a2a;
}

.chat-sidebar li.active {
  background: #a855f7;
  color: #fff;
}

.add-chat {
  font-size: 0.7rem;
  margin: 5px;
  padding: 5px;
  background-color: #a855f7;
  border: none;
  border-radius: 9px;
  color: #fff;
}

.add-chat:hover {
  cursor: pointer;
  background-color: #8f47d3;
}

@media (max-width: 768px) {
  .chat-sidebar {
    width: 100%;
    display: flex;
    flex-direction: row;
    overflow-x: auto;
  }
  .chat-sidebar ul {
    display: flex;
    gap: 0.5rem;
  }
  .chat-sidebar li {
    flex-shrink: 0;
  }
}
</style>
