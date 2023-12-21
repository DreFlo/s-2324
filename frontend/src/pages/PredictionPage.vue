<template>
    <Search />
    <div class="container mt-4 mb-4">
        <div class="row">
            <div class="col-md-12 p-2" style="background-color: #1C7330; border-radius: 5px;">
                <span class="display-6 text-center" style="color: white;">
                    We recommend you <b>{{ prediction['recommendation'] }}</b>
                </span>
            </div>
        </div>
        <div class="row text-start">
            <div v-html="prediction['explanation'].replaceAll('\n', '<br>')" class="col-md-12 p-2" style="background-color: whitesmoke; border-radius: 5px; text-align: justify;">
            </div>
        </div>
        <div class="row text-start">
            <div class="col-md-12 p-2" style="background-color: whitesmoke; border-radius: 5px; text-align: justify;">
                <span style="font-size: smaller;">
                    <b>Disclaimer:</b> This is not financial advice. We are not financial advisors. This is a prediction based on our machine learning model. Please do your own research before making any financial decisions.
                </span>
            </div> 
        </div>
    </div>
    <div class="p-3"></div>
  </template>

<script lang="ts">
    import { defineComponent } from 'vue';
    import Search from '../components/Search.vue';

    export default defineComponent({
    name: 'PredictionPage',
    components: {
        Search,
    },
    data() {
        return {
            prediction: JSON.parse(this.$route.params.prediction as string),
        };
    },
    methods: {},
    });
</script>