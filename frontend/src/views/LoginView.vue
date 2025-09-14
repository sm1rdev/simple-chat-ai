<script setup>
    import { reactive } from 'vue'
    import { useRouter } from 'vue-router'
    import api from '../app/api'

    const router = useRouter()

    const formData = reactive({
        email: "",
        password: ""
    })

    async function submitForm() {
        try {
            const data = new URLSearchParams()
            data.append("username", formData.email)
            data.append("password", formData.password)
            const response = await api.post("/users/token", data, {
                headers: { "Content-Type": "application/x-www-form-urlencoded" }
            })
            if(response.status == 200) {
                console.log("Login succesful!")
                router.push("/chat")
            }
        } catch(e) {
            console.error(e)
        }
    }
    
</script>

<template>
    <div class="content">
        <div class="register-container">
            <h1>LOGIN</h1>
            <form class="register-form" @submit.prevent="submitForm">
                <label>Email:</label>
                <input type="email" v-model="formData.email"/>

                <label>Password:</label>
                <input type="password" v-model="formData.password"/>

                <button type="submit">Register</button>
            </form>
            <router-link to="/register">Don't have account? Register</router-link>
        </div>
    </div>
</template>

<style scoped>
    .content {
        display: flex;
        flex-direction: column;
        width: 100%;
        height: 100%;
        align-items: center;
        justify-content: center;
    }

    .register-container {
        display: flex;
        flex-direction: column;
        width: 400px;
        text-align: center;
        gap: 10px;
    }

    .register-form {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
</style>
