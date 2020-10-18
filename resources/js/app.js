import app from './components/header';
const Vue = require('vue')
new Vue({
    el: "#app",
    data:{
        
    },
    components:{
        app,
    },

    template: "<app/>",
});
 Vue.component('passdata',require('./components/passdata.vue').default);
const app2 = new Vue({
    el: '#app2',
});