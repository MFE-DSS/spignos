<!-- components/Chat/ChatWindow.vue -->
<template>
  <div class="chat-container">
    <message-list :messages="messages" />
    <message-input @send="sendMessage" />
  </div>
</template>

<script>
import { ref } from 'vue'
import api from '@/services/api'

export default {
  setup() {
    const messages = ref([])

    const sendMessage = async (text) => {
      try {
        const response = await api.post('/chat/', { text })
        messages.value.push(response.data)
      } catch (error) {
        console.error('Erreur:', error)
      }
    }

    return {
      messages,
      sendMessage
    }
  }
}
</script>
