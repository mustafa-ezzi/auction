<template>
    <VOverlay
      :model-value="isVisible"
      class="align-center justify-center"
      style="backdrop-filter: blur(3px); background-color: rgba(0, 0, 0, 0.3);"
    >
      <div class="cricket-loader">
        <p class="loading-text"></p>
      </div>
    </VOverlay>
  </template>

  <script>
  export default {
    props: {
      isVisible: {
        type: Boolean,
        default: false,
      },
    },
  }
  </script>

<style scoped>
.cricket-loader {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.loading-text {
  margin-top: 20px;
  font-size: 18px;
  color: white;
  font-weight: bold;
}

/* Cricket Bat Styles */
.cricket-bat {
  position: relative;
  width: 60px;
  height: 150px;
  animation: bat-swing 1.5s infinite ease-in-out;
}

.bat-handle {
  position: absolute;
  width: 10px;
  height: 80px;
  background-color: #8b4513; /* Brown color for handle */
  top: 70px;
  left: 25px;
  border-radius: 5px;
}

.bat-blade {
  position: absolute;
  width: 40px;
  height: 70px;
  background-color: #c3b091; /* Light wood color for blade */
  top: 0;
  left: 10px;
  border-radius: 5px 5px 0 0;
}

/* Cricket Ball Styles */
.cricket-ball {
  width: 30px;
  height: 30px;
  background-color: #ff0000; /* Red color for the ball */
  border-radius: 50%;
  position: relative;
  margin-top: 20px;
  animation: ball-bounce 1.5s infinite ease-in-out;
}

/* Bat swinging animation */
@keyframes bat-swing {
  0% {
    transform: rotate(0deg);
  }
  50% {
    transform: rotate(-20deg);
  }
  100% {
    transform: rotate(0deg);
  }
}

/* Ball bouncing animation */
@keyframes ball-bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-15px);
  }
}
</style>