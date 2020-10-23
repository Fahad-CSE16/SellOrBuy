<template>
    <div>
       <!-- <Navbar/> -->
       <div class="container">
<!-- {{msg}} -->
    <About></About>
    <Detail></Detail>
    <Service/> -->
    <!-- <Contact/>
    
    </div>
    </div>
</template>
<script>
import Navbar from './Navbar.vue'
import About from './About.vue'
import Detail from './Detail.vue'
import Service from './Service.vue'
import Contact from './Contact.vue'

// Vue.component('pass_compo',require('./components/passdata.vue').default);


export default {
    data(){
        return{
                msg:"Hossain"
                // product: [{{product}}]
        }
    },
    props:['product'],
    components:{
        Navbar,
        About,
        Detail,
        Service,
        Contact,
    }
    
}
</script>