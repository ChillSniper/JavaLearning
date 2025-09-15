<div id = "app">
    <h1>{{message}}</h1>
</div>

<script type = "module">
import {createApp} from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';
createApp({
    data() {
        return {
            message: 'Hello Vue!'
        }
    }
}).mount('#app');
</script>

<template>

</template>

<style scoped>

</style>