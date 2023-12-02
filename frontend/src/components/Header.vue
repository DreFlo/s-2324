<template>
  <nav class="navbar navbar-light navbar-expand bg-light navigation-clean" style="width: 100%;">
    <div class="container">
      <a class="navbar-brand fs-4 fw-bold" href="/" style="--bs-body-color: #1C7330;color: #1C7330;">
        Money Talks
      </a>
      <div class="navbar-text" id="navcol-1">
        <a @click="goToRankings" style="color:#1C7335; text-decoration: none; cursor: pointer;">
            Top Recommendations
        </a>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
  import { defineComponent } from 'vue';

  export default defineComponent({
    name: 'Header',
    methods: {
      goToRankings() {
        this.$router.push({ name: 'rankings'});
      },
      goToHome() {
        this.$router.push({ name: 'home'});
      },
    },
  });
</script>
