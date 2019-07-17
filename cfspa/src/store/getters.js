export default {
  menuItems(state, getters) {
    let menuItems = [
      //{ icon: 'face', title: 'Sign up', link: {name: 'SignUp'} },
      { icon: "lock_open", title: "Sign in", link: { name: "SignIn" } }
    ];
    if (getters.userIsAuthenticated) {
      menuItems = [
        //{ icon: "supervisor_account", title: "View Meetups", link: "/meetups" },
        //{ icon: "supervisor_account", title: "View Meetups", link: "/meetups" },
        { icon: "queue", title: "Broadcasts", link: "/broadcasts" },
        { icon: "subject", title: "Templates", link: "/templates" },
        { icon: "contacts", title: "Contacts", link: "/contacts" },
        { icon: "attach_file", title: "Attachments", link: "/attachments" },
        { icon: "style", title: "Tag", link: "/tags" },
        { icon: "business", title: "Company", link: "/company" },
        { icon: "person", title: "Profile", link: "/profile" }
      ];
    }
    return menuItems;
  },
  user(state) {
    return state.user;
  },
  userIsAuthenticated(state) {
    return state.user !== null && state.user !== undefined;
  },
  sideNav(state) {
    return state.sideNav;
  },
  loading(state) {
    return state.loading;
  },
  progress(state) {
    return state.progress;
  },
  alert(state) {
    return state.alert;
  },

  getAuthHeader() {
    return {
      Authorization: "Bearer " + localStorage.getItem("token")
    };
  }
};
