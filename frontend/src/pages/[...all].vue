<script>
import { get } from '@/utils/api.js'
import Stadium from '../assets/images/back.jpg'
import Quaid from "../assets/images/quaid-logo.png"

export default {
  data() {
    return {
      logo: null,
      sponsor1: null,
      sponsor2: null,
      backgroundUrl: `url(${Stadium}) `,
      Quaid: Quaid
    }
  },
  mounted() {
    let projectId = localStorage.getItem('projectId')
    if (projectId) {
      this.getProject(projectId)
    }
  },
  methods: {
    async getProject(id) {
      const response = await get(`/project/${id}/`)
      let obj = response.data.data
      this.logo = obj['logo']
      this.sponsor1 = obj['sponsor1']
      this.sponsor2 = obj['sponsor2']
    },
  },

}
</script>

<template>
  <div class="divStyle" :style="{ backgroundImage: backgroundUrl }">
    <div class="image-row">
      <img v-if="sponsor1" :src="sponsor1" class="custom-logo mr-7 " alt="Description of the image">
      <img v-if="logo" :src="logo" class="custom-logo mr-7" alt="Description of the image">
      <img v-if="sponsor2" :src="sponsor2" class="custom-logo mr-7" alt="Description of the image">
    </div>

    <h1 class="welcomeHeading text-white">
      Welcome To Auction Pro
    </h1>

    <div class="buttonContainer">
      <RouterLink to="/settings">
        <button type="button" class="btn mt-3 btn-lg buttonStyle1 text-white">
          Admin Panel
        </button>
      </RouterLink>

      <RouterLink to="/auction1">
        <button type="button" class="btn mt-3 btn-lg buttonStyle2 text-white">
          Start Auction
        </button>
      </RouterLink>

      <RouterLink to="/login">
        <button type="button" class="btn mt-3 btn-lg buttonStyle3 text-white">
          Team Login
        </button>
      </RouterLink>
    </div>
    <div class="contact-div">
      <img :src="Quaid" class="image">
      <h1 class="contact text-white">
        Managed By:<br>
        QuaidJohar <br> +971 556086529
      </h1>
    </div>
  </div>
</template>

<style scoped>
.divStyle {
  background-size: cover;
  height: 95vh;
  align-items: center;
  padding-top: 1rem;
}

.image-row {
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-logo {
  width: 6%;
  height: auto;
  object-fit: cover;
}

.welcomeHeading {
  font-size: 2rem;
  text-align: center;
  font-weight: 700;
}

.contact {
  font-size: 1rem;
  text-align: start;
}

.contact-div {
  position: absolute;
  bottom: 26px;
  right: 6px;
}

.buttonContainer {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3;
}

.buttonStyle1 {
  color: white;
  background-color: blue;

}

.buttonStyle2 {
  color: white;
  background-color: orange;

}

.buttonStyle3 {
  color: white;
  background-color: red;

}

.buttonStyle1,
.buttonStyle2,
.buttonStyle3 {
  width: 100%;
  margin-top: 1rem;
}

.image {
  width: 65px;
  height: 65px;
  object-fit: cover;
}

@media (min-width: 576px) {

  .image {
    width: 200px;
    height: 200px;
  }

  .contact {
    font-size: 2rem;
  }

  .welcomeHeading {
    font-size: 4rem;
    margin-top: 80px;
  }

  .buttonContainer {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 3;
  }

  .buttonStyle1,
  .buttonStyle2,
  .buttonStyle3 {
    width: auto;
    margin-left: 5px;
    margin-right: 5px;
  }


}
</style>

<route lang="yaml">
meta:
  layout: blank
</route>
