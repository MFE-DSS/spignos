<!-- components/Chat/ChatWindow.vue -->
<template>
  <div class="chat-container">
    <message-list :messages="messages" />
    <message-input @send="sendMessage" />
  </div>
</template>

<script>
import { useStore } from 'vuex'
import { computed } from 'vue'

export default {
  setup() {
    const store = useStore()
    const messages = computed(() => store.state.messages)

    const sendMessage = async (text) => {
      try {
        await store.dispatch('sendMessage', text)
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
