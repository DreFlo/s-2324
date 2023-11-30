<template>
    <div class="container-fluid ms-0" style="padding: 5%;padding-bottom: 10%;padding-top: 10%; background: url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');">
        <div class="row">
            <div class="col-md-12 text-center align-self-center">
                <p class="fs-5 fw-bolder" style="margin-bottom: 1%;margin-top: 1%;color: #1C7330;">
                    [WHAT WE DO]
                </p>
            </div>
        </div>
        <div class="row">
            <div class="col-2"></div>
            <div class="col-6 text-center align-self-center">
                <input class="form-control-lg" type="search" placeholder="Search for a Company..." style="width: 100%;border-radius: 15px;border: 2px solid #1C7330 ;">
            </div>
            <div class="col-2 col-xl-2 text-center align-self-center">
                <button class="btn btn-primary btn-lg" type="submit" style="background: #1C7330;">
                    Search
                </button>
            </div>
            <div class="col-2"></div>
        </div>
    </div>
    <RankingTable :numRankings=3 />
  </template>

<script lang="ts">
    import { defineComponent } from 'vue';
    import RankingTable from '../components/RankingTable.vue';

    export default defineComponent({
    name: 'HomePage',
    components: {
        RankingTable,
    },
    methods: {
        searchCompany() {
            //Add axios call
        }
    },
    });
</script>