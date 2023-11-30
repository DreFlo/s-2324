<template>
    <Header />
    <div class="container ms-0" style="padding: 5%;padding-bottom: 10%;padding-top: 10%; background: url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')">
        <div class="row">
            <div class="col-md-12 text-center align-self-center">
                <p class="fs-5 fw-bolder" style="margin-bottom: 1%;margin-top: 1%;color: #1C7330;">
                    [WHAT WE DO]
                </p>
            </div>
        </div>
        <div class="row">
            <div class="col-xl-1"></div>
            <div class="col-md-6 col-xl-7 text-center align-self-center">
                <input class="form-control-lg" type="search" placeholder="Search for a Company..." style="width: 100%;border-radius: 15px;border: 2px solid #1C7330 ;">
            </div>
            <div class="col-md-6 col-xl-2 text-center align-self-center">
                <button class="btn btn-primary btn-lg" type="submit" style="background: #1C7330;">
                    Search
                </button>
            </div>
            <div class="col"></div>
        </div>
    </div>
    <div class="container p-5">
        <div class="row">
            <div class="col-md-12">
                <p class="fs-5 fw-bolder text-center" style="margin-bottom: 1%;margin-top: 1%;color: #1C7330;">
                    Top Predictions
                </p>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <ul class="list-group">
                    <li class="list-group-item" style="--bs-body-bg: #959595;background: rgb(241,241,241);">
                        <div class="row">
                            <div class="col-1 text-center align-self-center">
                                <i class="bi bi-caret-up-fill" style="color: #1C7330; font-size:x-large;"></i>
                            </div>
                            <div class="col-3 text-center align-self-center">
                                <span>
                                    Company Name
                                </span>
                            </div>
                            <div class="col-6 text-center align-self-center">
                                <span>
                                    Prediction Info
                                </span>
                            </div>
                            <div class="col-1 text-center align-self-center">
                                <i class="bi bi-chevron-down" style="color: #1C7335;"></i>
                            </div>
                        </div>
                    </li>
                    <li class="list-group-item" style="--bs-body-bg: #959595;background: rgb(241,241,241);">
                        <div class="row">
                            <div class="col-1 text-center align-self-center">
                                <i class="bi bi-caret-down-fill" style="color: #9c0900; font-size:x-large;"></i>
                            </div>
                            <div class="col-3 text-center align-self-center">
                                <span>
                                    Company Name
                                </span>
                            </div>
                            <div class="col-6 text-center align-self-center">
                                <span>
                                    Prediction Info
                                </span>
                            </div>
                            <div class="col-1 text-center align-self-center">
                                <i class="bi bi-chevron-down" style="color: #1C7335;"></i>
                            </div>
                        </div>
                    </li>
                    <li class="list-group-item" style="--bs-body-bg: #959595;background: rgb(241,241,241);">
                        <div class="row">
                            <div class="col-1 text-center align-self-center">
                            </div>
                            <div class="col-3 text-center align-self-center">
                                <span>
                                    Company Name
                                </span>
                            </div>
                            <div class="col-6 text-center align-self-center">
                                <span>
                                    Prediction Info
                                </span>
                            </div>
                            <div class="col-1 text-center align-self-center">
                                <i class="bi bi-chevron-down" style="color: #1C7335;"></i>
                            </div>
                        </div>
                    </li>
                    <li class="list-group-item" style="--bs-body-bg: #959595;background: rgb(241,241,241);">
                        <div class="row">
                            <div class="col-1 text-center align-self-center">
                                <i class="bi bi-caret-up-fill" style="color: #1C7330; font-size:x-large;"></i>
                            </div>
                            <div class="col-3 text-center align-self-center">
                                <span>
                                    Company Name
                                </span>
                            </div>
                            <div class="col-6 text-center align-self-center">
                                <span>
                                    Prediction Info
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
    <Footer />
  </template>

<script lang="ts">
    import { defineComponent } from 'vue';
    import Header from '../components/Header.vue';
    import Footer from '../components/Footer.vue';

    export default defineComponent({
    name: 'HomePage',
    components: {
        Header,
        Footer
    },
    });
</script>