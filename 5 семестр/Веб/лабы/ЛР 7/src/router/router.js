import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/home',
      name: 'home',
      meta: {
        title: "Главная страница"
        },
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/form',
      name: 'form',
      meta: {
        title: "Форма контактов"
        },
      component: () => import('../views/ContactView.vue')
    }
  ]
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title;
  console.log(document.title);
  next();
});

export default router
