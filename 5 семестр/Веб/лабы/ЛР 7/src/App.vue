<script setup>
  import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/home" class="page">Главная</RouterLink>
      <RouterLink to="/form" class="page">Форма</RouterLink>
    </nav>
  </header>

  <RouterView/>
</template>

<style scoped>
  header {
    align-items: center;
    text-align: center;
    vertical-align: middle;
  }

  .page {
    margin-right: 40px;
    text-decoration: none;
    font-size: 16px;
    color: black;
  }

  .page:last-child {
    margin-right: 0px;
  }

  .page:hover {
    color: rgb(75, 210, 255);
    border-radius: 10px;
    font-weight: bold;
  }
</style>