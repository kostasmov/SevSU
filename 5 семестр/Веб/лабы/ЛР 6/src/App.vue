<template>
  <form @submit.prevent="submitForm">
    <h1>Форма</h1>

    <div>
      <label for="name">Имя</label>
      <input type="text" id="name" v-model="formData.name" @input="resetSuccessMessage"/>
    </div>

    <div>
      <label for="surname">Фамилия</label>
      <input type="text" id="surname" v-model="formData.surname" @input="resetSuccessMessage"/>
    </div>

    <div>
      <label for="age">Возраст</label>
      <input type="number" id="age" v-model="formData.age" @input="resetSuccessMessage"/>
    </div>

    <div>
      <label>Пол</label>
      <div v-for="option in sexOptions" :key="option">
        <input type="radio" v-model="formData.sex" :value="option" @input="resetSuccessMessage"/>
        <span>{{ option }}</span>
      </div>
    </div>

    <div>
      <label>Фреймворки</label>
      <div v-for="option in frameworkOptions" :key="option">
        <input type="checkbox" v-model="formData.frameworks" :value="option" @input="resetSuccessMessage"/>
        <span>{{ option }}</span>
      </div>
    </div>

    <button type="submit">Отправить</button>

    <div v-if="isFormSubmitted && errors.length === 0" class="msg">{{ successMessage }}</div>

    <div v-if="errors.length > 0">
      <ul>
        <li v-for="error in errors" :key="error.field">{{ error.message }}</li>
      </ul>
    </div>
  </form>
</template>

<script>
import { computed } from '@vue/reactivity';

export default {
  data: () => ({
    formData: {
      name: '',
      surname: '',
      age: null,
      sex: '',
      frameworks: []
    },

    sexOptions: Object.freeze({
      M: 'M',
      F: 'F'
    }),

    frameworkOptions: Object.freeze([
      'Vue', 
      'Angular', 
      'Svelte', 
      'React'
    ]),

    successMessage: 'Форма отправлена успешно!',
    isFormSubmitted: false
  }),

  methods: {
    submitForm() {
      if (this.errors.length === 0) {
        this.successMessage = 'Форма отправлена успешно!';
        this.isFormSubmitted = true;
      }
    },

    resetSuccessMessage() {
      this.successMessage = '';
    },
  },

  computed: {
    errors() {
      const errors = [];

      if (!this.formData.name) {
        errors.push({ field: 'name', message: 'Введите имя!' });
      } else {
        errors.filter((error) => error.field !== 'name');
      }

      if (!this.formData.surname) {
        errors.push({ field: 'surname', message: 'Введите фамилию!' });
      } else {
        errors.filter((error) => error.field !== 'surname');
      }

      if (!this.formData.age && typeof this.formData.age !== 'number') {
        errors.push({ field: 'age', message: 'Укажите возраст!' });
      } else {
        errors.filter((error) => error.field !== 'age');
      }

      if (!this.formData.sex) {
        errors.push({ field: 'sex', message: 'Укажите пол!' });
      } else {
        errors.filter((error) => error.field !== 'sex');
      }

      return errors;
    }
  }
};
</script>

<style>
  body {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    margin: 0;
    background-color: #f0f0f0;
    font-family: Arial, sans-serif;
  }

  form {
    text-align: left;
    width: 300px;
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  }

  label {
    display: block;
    margin-bottom: 5px;
  }

  input[type="text"], input[type="number"] {
    width: 90%;
    padding: 10px;
    margin: 10px 0;
    border-radius: 4px;
    border: 1px solid #ccc;
  }

  button {
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 4px;
    background-color: #007BFF;
    color: #fff;
    cursor: pointer;
  }

  button:hover {
    background-color: #0056b3;
  }
</style>
