<template>
    <div class="container-fluid ms-0" style="padding: 5%;padding-bottom: 5%;padding-top: 5%; background: url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'); background-position: center center;">
        <div class="row">
            <div class="col-2"></div>
            <div class="col-6 text-center align-self-center">
                <input class="form-control-lg" type="search" v-model="searchString" placeholder="Search for a Company..." style="width: 100%;border-radius: 15px;border: 2px solid #1C7330 ;">
            </div>
            <div class="col-2 col-xl-2 text-center align-self-center">
                <button class="btn btn-primary btn-lg" type="submit" v-on:click="searchCompany" data-bs-toggle="modal" data-bs-target="#staticBackdrop" style="background: #1C7330;">
                    Search
                </button>
            </div>
            <div class="col-2"></div>
        </div>
    </div>

    
    <div class="modal fade" ref="modal" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header" id="ModalHeader" style="display: none;">
                    <h5 class="modal-title ms-2" id="staticBackdropLabel">Error</h5>
                    <button type="button" id="closeModalBttn" class="btn-close me-2" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body" id="loadingModalBody">
                    <h5 class="modal-title mb-3" id="staticBackdropLabel">Searching...</h5>
                    <div class="spinner-border" role="status" style="color: #1C7330;">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
                <div class="modal-body" id="errorModalBody" style="display: none;">
                    <span id="errorMessage"></span>
                </div>
                <!-- <div class="modal-footer" id="ModalFooter" style="display: none;" >
                    <button type="button" id="closeModalBttn" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div> -->
            </div>
            
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
            (document.getElementById('ModalHeader') as HTMLDivElement).style.display = 'none';
            (document.getElementById('errorModalBody') as HTMLDivElement).style.display = 'none';
            (document.getElementById('loadingModalBody') as HTMLDivElement).style.display = 'initial';

            console.log(this.searchString);
            await axios.get('http://localhost:8000/predict', {
                params: {
                    company_name: this.searchString,
                }
            }).then((response) => {
                console.log(response.data);
                (document.getElementById('closeModalBttn') as HTMLButtonElement).click();
                this.$router.push({ name: 'prediction', params: { prediction: JSON.stringify(response.data) } });
            }).catch((error) => {
                console.log(error.response.data.detail);
                (document.getElementById('ModalHeader') as HTMLDivElement).style.display = 'flex';
                (document.getElementById('errorModalBody') as HTMLDivElement).style.display = 'initial';
                (document.getElementById('loadingModalBody') as HTMLDivElement).style.display = 'none';
                (document.getElementById('errorMessage') as HTMLDivElement).innerHTML = error.response.data.detail;
            });

        }
      },
    });
  </script>
  