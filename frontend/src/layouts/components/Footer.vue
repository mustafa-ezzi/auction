<template>
  <hr/>
  <footer class=" py-4 text-gray-500 " style="background-color: none;">
    <span class="flex justify-center">
      &copy; {{ currentYear }} Made By <a
        :href="websiteLink"
        target="_blank"
        style="color: red;"
        class="ml-1 "
      > 5Cube</a>
    </span>
  </footer>
</template>
<div class="h-4 w-px bg-gray-300 mx-2"></div>
<script>
export default {
  data() {
    return {
      websiteLink: 'https://5cube.io/',
    }
  },
  computed: {
    currentYear() {
      return new Date().getFullYear()
    },
  },  
}
</script>

<style>


.footer {
  width: 100%;
  text-align: center;
  bottom: 0;
  /* background-color: lavender !important; */
}

@media (min-width: 768px) {
  .footer {
    position: relative;
  }
}
</style>