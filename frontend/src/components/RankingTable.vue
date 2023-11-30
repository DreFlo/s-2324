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
                            <div id="bttn{{ ranking['newRanking'] }}" class="col-1 text-center align-self-center">
                                <i class="bi bi-chevron-down" data-bs-toggle="collapse" :href="'#collapse'+ ranking['newRanking'] " role="button" aria-expanded="false" :aria-controls="'collapse'+ ranking['newRanking']" style="color: #1C7335;"></i>
                            </div>
                        </div>
                        <div class="collapse" :id="'collapse'+ ranking['newRanking']">
                            <div class="card card-body">
                                Prediction Info
                            </div>
                        </div>
                    </li>
                    
                    <li v-if="this.numRankings != null" class="list-group-item text-center" style="--bs-body-bg: #959595;background: rgb(241,241,241);">
                        <a @click="goToRankings" style="color: #1C7330; cursor:pointer">
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
            default: null
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
            
            this.rankings.push({companyId: 1, companyName: 'Company 1', score: 0.90, oldRanking: 1, newRanking: 1});
            this.rankings.push({companyId: 2, companyName: 'Company 2', score: 0.88, oldRanking: 2, newRanking: 2});
            this.rankings.push({companyId: 3, companyName: 'Company 3', score: 0.86, oldRanking: 4, newRanking: 3});
            this.rankings.push({companyId: 4, companyName: 'Company 4', score: 0.84, oldRanking: 3, newRanking: 4});
            this.rankings.push({companyId: 5, companyName: 'Company 4', score: 0.83, oldRanking: 5, newRanking: 5});
            
            if (this.numRankings == null) {
                this.rankings.push({companyId: 6, companyName: 'Company 6', score: 0.80, oldRanking: 8, newRanking: 6});
                this.rankings.push({companyId: 7, companyName: 'Company 7', score: 0.78, oldRanking: 7, newRanking: 7});
                this.rankings.push({companyId: 8, companyName: 'Company 8', score: 0.77, oldRanking: 6, newRanking: 8});
                this.rankings.push({companyId: 9, companyName: 'Company 9', score: 0.75, oldRanking: 9, newRanking: 9});
                this.rankings.push({companyId: 10, companyName: 'Company 10', score: 0.74, oldRanking: 10, newRanking: 10});

            }
        },
        goToRankings() {
            this.$router.push({ name: 'rankings'});
        }
    }
});
</script>