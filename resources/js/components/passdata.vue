<template>
    <div>
       <h1 class="text-white">{{prod}}</h1>
       <h5 class="text-white" v-for="(product,index) in prod" :key="index">{{product.name}}</h5>
    </div>
</template>
<script>
export default {
    // delimiters: ["[[", "]]"],
    props:{
        product:Array,
    },
    data(){
        return{
            prod:this.product,
        }
    },
}
</script>