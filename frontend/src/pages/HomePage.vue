<template>
    <Search />
    <RankingTable :numRankings=5 />
  </template>

<script lang="ts">
    import { defineComponent } from 'vue';
    import RankingTable from '../components/RankingTable.vue';
    import Search from '../components/Search.vue';


    export default defineComponent({
    name: 'HomePage',
    components: {
        RankingTable,
        Search,
    },
    methods: {},
    });
</script>