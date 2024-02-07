<template>
  <div class="content1">
    <h1>Главная</h1>
    <img :src="avatarPath" alt="Мой интернет аватар" class="avatar">
    <div class="lab-info">
      <p>Лабораторная работа №{{ labNumber }}</p>
      <p class="labTitle">{{ labTitle }}</p>
    </div>
    <button @click="incrementLabNumber">Мутация</button>
  </div>
</template>

<script>
  import { mapGetters, mapMutations } from 'vuex';

  export default {
    computed: {
      ...mapGetters(['getLabNumber']),
      avatarPath() {
        return this.$store.state.avatarPath;
      },
      labTitle() {
        return this.$store.state.labTitle;
      },
      labNumber() {
        return this.getLabNumber;
      },
    },
    methods: {
      ...mapMutations(['incrementLabNumber']),
    }
    
  };
</script>

<style>
  .content1 {
    padding-left: 20%;
    padding-right: 20%;
    justify-content: center;
    align-items: center;
    text-align: center;
    color: rgb(16, 16, 16);
    margin-bottom: 20px;
  }

  .lab-info {
    margin-bottom: 20px;
  }

  .content1 h1 {
    font-weight: 700;
    font-size: 24px;
    margin-bottom: 80px;
  }

  .content1 img {
    width: 150px;
    height: 150px;
    margin-bottom: 20px;
    border-radius: 5px;
  }

  .lab-info p {
    color: rgb(0, 0, 0);
    padding: 16px;
    font-size: 20px;
    font-weight: 700;
  }

  .labTitle {
    color: black;
  }

  .content1 button {
    padding-top: 40px;
    font-size: 20px;
    font-weight: 700;
    padding: 8px 32px;
    border-style: none;
    border-radius: 5px;
    outline: none;
    background-color: rgb(0, 0, 0);
    color: white;
    cursor: pointer;
    display: inline-block;
  }

  .content1 button:hover {
    background-color: rgb(75, 210, 255);
  }
</style>
