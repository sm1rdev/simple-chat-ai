import { createRouter, createWebHistory } from 'vue-router'

import RegisterView from "../views/RegisterView.vue"
import LoginView from '../views/LoginView.vue'
import ChatView from '../views/ChatView.vue'


const router = createRouter(
    {
        history: createWebHistory(),
        routes: [
            {path: "", redirect: "/chat"},
            {path: "/register", name: "Register", component: RegisterView},
            {path: "/login", name: "Login", component: LoginView},
            {path: "/chat", name: "Chat", component: ChatView}
        ]
    }
)

export default router
