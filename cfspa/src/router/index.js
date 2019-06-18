import Vue from "vue";
import Router from "vue-router";
import MainContent from "../components/MainContent";
import SignIn from "../components/user/SignIn";
//import SignUp from "../components/user/SignUp";
// import W2pLogin from '@/components/W2pLogin'

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "Home",
      component: MainContent
    },
    {
      path: "/signin",
      name: "SignIn",
      component: SignIn
    }
  ],
  mode: "history"
});
