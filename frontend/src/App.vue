<script setup>
import Footer from '@/layouts/components/Footer.vue'
</script>
 
<template>
  <VApp>
    <VLayout class="layout-wrapper layout-nav-type-vertical">
      <RouterView />
    </VLayout>
    <Footer />
  </VApp>
</template>
