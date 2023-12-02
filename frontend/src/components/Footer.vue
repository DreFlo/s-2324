<template>
    <hr class="m-0">
    <footer class="footer-fluid mt-0 py-3 bg-light" style="width:100%;">
        <div class="container">
            <div class="row">
                <div class="col-lg-6 text-center text-lg-start my-auto h-100">
                    <ul class="list-inline mb-2">
                        <li class="list-inline-item">
                            <a href="#" style="color:#1C7335;">
                                About
                            </a>
                        </li>
                        <li class="list-inline-item">
                            <span style="color: var(--bs-black);font-size: 16;font-weight: bold;">
                                ⋅ 
                            </span>
                        </li>
                        <li class="list-inline-item">
                            <a href="#" style="color:#1C7335;">
                                Contact
                            </a>
                        </li>
                        <li class="list-inline-item">
                            <span style="font-size: 16px;font-weight: bold;">
                                ⋅
                            </span>
                        </li>
                        <li class="list-inline-item">
                            <a href="#" style="color:#1C7335;">
                                Terms of Use
                            </a>
                        </li>
                        <li class="list-inline-item">
                            <span style="font-weight: bold;">
                                ⋅
                            </span>
                        </li>
                        <li class="list-inline-item">
                            <a href="#" style="color:#1C7335;">
                                Privacy Policy
                            </a>
                        </li>
                    </ul>
                    <p class="text-muted small mb-4 mb-lg-0">© Money Talks 2023. All Rights Reserved.</p>
                </div>
                <div class="col-lg-6 text-center text-lg-end my-auto h-100"></div>
            </div>
        </div>
    </footer>
</template>

<script lang="ts">
  import { defineComponent } from 'vue';

  export default defineComponent({
    name: 'Footer',
  });
</script>