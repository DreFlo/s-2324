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
                <div class="accordion" id="accordionExample">
                    <div class="accordion-item pt-2 pb-2" style="background-color: lightgray;">
                        <div class="row ps-4">
                            <div class="col-3 text-start">
                                <span style="font-weight: bold;">
                                    Company Name
                                </span>
                            </div>
                            <div class="col-2 text-start">
                                <span style="font-weight: bold;">
                                    Recommendation
                                </span>
                            </div>
                            <div class="col-3 text-start">
                                <span style="font-weight: bold;">
                                    Probability of price increase
                                </span>
                            </div>
                            <div class="col-2 text-start">
                                <span style="font-weight: bold;">
                                    Prediction Date
                                </span>
                            </div>
                        </div>
                    </div>
                    <div v-for="ranking in this.rankings" class="accordion-item" style="background-color: whitesmoke;">
                        <div class="row p-2">
                            <div class="col-3 text-start ms-3">
                                <span>
                                    {{ ranking['name'] }} ({{ ranking['symbol'] }})
                                </span>
                            </div>
                            <div class="col-2 text-start">
                                <span v-if="ranking['recommendation'] == 'buy'" style="color: #1C7330; font-weight: bold;">
                                    Buy
                                </span>
                                <span v-else-if="ranking['recommendation'] == 'sell'" style="color: #9c0900; font-weight: bold;">
                                    Sell
                                </span>
                            </div>
                            <div class="col-3 text-start">
                                <span v-if="ranking['recommendation'] == 'buy'" style="color: #1C7330;">
                                    {{ (Number(ranking['probability']) * 100).toFixed(2) }}%
                                </span>
                                <span v-else-if="ranking['recommendation'] == 'sell'" style="color: #9c0900;">
                                    {{ (Number(ranking['probability']) * 100).toFixed(2) }}%
                                </span>
                            </div>
                            <div class="col-2 text-start">
                                <span>
                                    {{ ranking['date'].split(' ')[0] }}
                                </span>
                            </div>
                            <div class="col-1 text-end" :id="'heading'+ ranking['symbol']">
                                <button :id="'button'+ranking['symbol']" class="accordion-button p-0 m-0 collapsed" type="button" data-bs-toggle="collapse" aria-expanded="false" :data-bs-target="'#collapse'+ ranking['symbol']" :aria-controls="'collapse'+ ranking['symbol']" style="width: fit-content !important;">
                                </button>
                            </div>

                        </div>
                        <div :id="'collapse'+ ranking['symbol']" class="accordion-collapse collapse"  data-bs-parent="#accordionExample">
                            <div v-html="ranking['explanation'].replaceAll('\n', '<br>')" class="accordion-body ms-1" style="text-align: justify !important;">
                            </div>
                        </div>
                    </div>
                    <div v-if="this.numRankings != -1" class="accordion-item p-2" style="background: whitesmoke">
                        <a @click="goToRankings" style="color: #1C7330; cursor:pointer">
                            Click to See More
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { Ranking } from '../types/Ranking.ts';
import axios from 'axios';

export default defineComponent({
    name: 'RankingTable',
    props: {
        numRankings: {
            type: Number,
            required: false,
            default: -1
        },
    },
    data() {
        return {
            rankings: [] as Ranking[],
        };
    },
    async mounted() {
        await this.getRankings();
    },
    methods: {
        async getRankings() {
            await axios.get('http://localhost:8000/rankings', {
                params: {
                    num: this.numRankings,
                }
            }).then((response) => {
                this.rankings = response.data;
            }).catch((error) => {
                console.log(error);
            });
        },
        goToRankings() {
            this.$router.push({ name: 'rankings'});
        }
    }
});
</script>