<script setup>
    import { reactive } from 'vue'
    import { useRouter } from 'vue-router'
    import api from '../app/api'

    const router = useRouter()

    const formData = reactive({
        nickname: "",
        email: "",
        password: ""
    })

    async function submitForm() {
        try {
            const response = await api.post("/users", formData)
            if (response.status == 200) {
                console.log("Register succesful!")
                router.push("/login")
            }
        }
        catch(e) {
            console.error(e)
        }
    }
    
</script>

<template>
    <div class="content">
        <div class="register-container">
            <h1>REGISTER</h1>
            <form class="register-form" @submit.prevent="submitForm">
                <label>Username:</label>
                <input type="text" v-model="formData.nickname"/>

                <label>Email:</label>
                <input type="email" v-model="formData.email"/>

                <label>Password:</label>
                <input type="password" v-model="formData.password"/>

                <button type="submit">Register</button>
            </form>
            <router-link to="/login">Have account? Login</router-link>
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
