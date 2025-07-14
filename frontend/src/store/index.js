// frontend/src/store/index.js
import { createStore } from 'vuex'
import { chatService } from '@/services/api'

export default createStore({
    state: {
        messages: []
    },
    mutations: {
        SET_MESSAGES(state, messages) {
            state.messages = messages
        },
        ADD_MESSAGE(state, message) {
            state.messages.push(message)
        }
    },
    actions: {
        async sendMessage({ commit }, message) {
            const response = await chatService.sendMessage(message)
            commit('ADD_MESSAGE', response.data)
        }
    }
})
