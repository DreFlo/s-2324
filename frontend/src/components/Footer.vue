<template>
    <body class="d-flex flex-column h-100" style="width: 100vw;">
        <footer class="footer mt-auto py-3 bg-light">
            <div class="container">
                <div class="row">
                    <div class="col-lg-6 text-center text-lg-start my-auto h-100">
                        <ul class="list-inline mb-2">
                            <li class="list-inline-item"><a href="#">About</a></li>
                            <li class="list-inline-item"><span style="color: var(--bs-black);font-size: 16;font-weight: bold;">⋅ </span></li>
                            <li class="list-inline-item"><a href="#">Contact</a></li>
                            <li class="list-inline-item"><span style="font-size: 16px;font-weight: bold;">⋅</span></li>
                            <li class="list-inline-item"><a href="#">Terms of &nbsp;Use</a></li>
                            <li class="list-inline-item"><span style="font-weight: bold;">⋅</span></li>
                            <li class="list-inline-item"><a href="#">Privacy Policy</a></li>
                        </ul>
                        <p class="text-muted small mb-4 mb-lg-0">© Money Talks 2023. All Rights Reserved.</p>
                    </div>
                    <div class="col-lg-6 text-center text-lg-end my-auto h-100"></div>
                </div>
            </div>
        </footer>
    </body>
</template>

<script lang="ts">
  import { defineComponent } from 'vue';

  export default defineComponent({
    name: 'Footer',
  });
</script>