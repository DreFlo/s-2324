<template>
    <div class="container p-5">
        <div class="row">
            <div class="col-md-12">
                <p class="fs-5 fw-bolder text-center" style="margin-bottom: 1%;color: #1C7330;">
                    Top Recommendations
                </p>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <ul class="list-group">
                    <li v-for="ranking in this.rankings" class="list-group-item" style="--bs-body-bg: #959595;background: rgb(241,241,241);">
                        <div class="row">
                            <div class="col-1 text-center align-self-center">
                                <i v-if="ranking['newRanking'] > ranking['oldRanking']" class="bi bi-caret-up-fill" style="color: #1C7330; font-size:x-large;"></i>
                                <i v-else-if="ranking['oldRanking'] > ranking['newRanking']" class="bi bi-caret-down-fill" style="color: #9c0900; font-size:x-large;"></i>
                                <i v-else class="bi bi-dash-lg" style=" font-size:x-large;"></i>
                            </div>
                            <div class="col-3 text-center align-self-center">
                                <span>
                                    {{ ranking['companyName'] }}
                                </span>
                            </div>
                            <div class="col-6 text-center align-self-center">
                                <span>
                                    {{ ranking['score'] }}
                                </span>
                            </div>
                            <div class="col-1 text-center align-self-center">
                                <i class="bi bi-chevron-down" style="color: #1C7335;"></i>
                            </div>
                        </div>
                    </li>
                    <li class="list-group-item text-center" style="--bs-body-bg: #959595;background: rgb(241,241,241);">
                        <a href="#" style="color: #1C7330;">
                            Click to See More
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { Ranking } from '../types/Ranking.ts';

export default defineComponent({
    name: 'RankingTable',
    props: {
        numRankings: {
            type: Number,
            required: false,
        },
    },
    data() {
        return {
            rankings: [] as Ranking[],
        };
    },
    mounted() {
        this.getRankings();
    },
    methods: {
        getRankings() {
            //add axios call to get rankings
            
            this.rankings.push({companyId: 1, companyName: 'Company 1', score: 0.9, oldRanking: 1, newRanking: 1});
            this.rankings.push({companyId: 2, companyName: 'Company 2', score: 0.8, oldRanking: 2, newRanking: 2});
            this.rankings.push({companyId: 3, companyName: 'Company 3', score: 0.7, oldRanking: 4, newRanking: 3});
            this.rankings.push({companyId: 4, companyName: 'Company 4', score: 0.6, oldRanking: 3, newRanking: 4});
            this.rankings.push({companyId: 4, companyName: 'Company 4', score: 0.5, oldRanking: 5, newRanking: 5});
            
        }
    }
});
</script>