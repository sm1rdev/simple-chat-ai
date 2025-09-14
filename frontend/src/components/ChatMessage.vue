<template>
  <div :class="['chat-message', message.from === 'me' ? 'me' : 'other']">
    {{ message.data }}
  </div>
</template>

<script setup>
defineProps({
  message: Object
});
</script>

<style scoped>
.chat-message {
  max-width: 60%;
  padding: 0.5rem 0.75rem;
  margin-bottom: 0.5rem;
  border-radius: 12px;
  line-height: 1.4;
}
.chat-message.me {
  background: #a855f7;
  color: #fff;
  margin-left: auto;
}
.chat-message.other {
  background: #2a2a2a;
  color: #ddd;
  margin-right: auto;
}
</style>
