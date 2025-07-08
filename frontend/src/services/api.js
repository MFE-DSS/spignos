// frontend/src/services/api.js
import axios from 'axios'

const api = axios.create({
    baseURL: process.env.VUE_APP_API_URL,
    headers: {
        'Content-Type': 'application/json'
    }
})

export const chatService = {
    sendMessage(message) {
        return api.post('/api/chat/', { content: message })
    },
    getMessages() {
        return api.get('/api/chat/')
    }
}

export default api