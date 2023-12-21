<template>
    <div class="container-fluid ms-0" style="padding: 5%;padding-bottom: 5%;padding-top: 5%; background: url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'); background-position: center center;">
        <div class="row">
            <div class="col-2"></div>
            <div class="col-6 text-center align-self-center">
                <input class="form-control-lg" type="search" v-model="searchString" placeholder="Search for a Company..." style="width: 100%;border-radius: 15px;border: 2px solid #1C7330 ;">
            </div>
            <div class="col-2 col-xl-2 text-center align-self-center">
                <button class="btn btn-primary btn-lg" type="submit" v-on:click="searchCompany" style="background: #1C7330;">
                    Search
                </button>
            </div>
            <div class="col-2"></div>
        </div>
    </div>
  </template>
  
  <script lang="ts">
    import { defineComponent } from 'vue';
    import axios from 'axios';
  
    export default defineComponent({
      name: 'Search',
      data() {
        return {
            searchString: '' as string,
        };
      },
      methods: {
        async searchCompany() {
            console.log(this.searchString);
            await axios.get('http://localhost:8000/predict', {
                params: {
                    company_name: this.searchString,
                }
            }).then((response) => {
                console.log(response.data);
                this.$router.push({ name: 'prediction', params: { prediction: JSON.stringify(response.data) } });
            }).catch((error) => {
                console.log(error);
            });

        }
      },
    });
  </script>
  