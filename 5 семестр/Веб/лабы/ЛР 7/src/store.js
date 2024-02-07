import { createStore } from 'vuex'

const store = createStore({
  state() {
    return {
      title: 'Главная',
      avatarPath: './src/assets/img/photo.jpg',
      labNumber: 7,
      labTitle: 'VUE.JS · Маршрутизация и управление состоянием'
    };
  },
  mutations: {
    incrementLabNumber(state) {
      state.labNumber++;
    },
  },
  getters: {
    getLabNumber(state) {
      return state.labNumber;
    }
  }
})

export default store