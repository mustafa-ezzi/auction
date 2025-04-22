<template>
    <div style="background-color: white;border-radius: 30px;">

  <VRow>
    <VCol md="9" sm="9">
      <h1 class="ml-5 mt-2 heading">
        Unsold - Players
      </h1>
    </VCol>
    <VCol md="3" sm="" class="mb-3">
      <VSelect class="mr-4"  v-model="selectedCategory" label="Category" :items="category" item-value="id" item-title="name" />
    </VCol>
  </VRow>
  <!-- table for showing data -->
  <VTable style="border-radius: 30px;">
    <thead>
      <tr>
        <th>
          Name
        </th>
        <th>
          Profile Picture
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in players" :key="item.name">
        <td>{{ item.name }} </td>
        <td>
          <img v-if="item.profile_pic" class="image" :src="item.profile_pic">
        </td>
      </tr>
    </tbody>
  </VTable>
</div>
  <VDialog v-model="deleteDialog" max-width="400" persistent width="500">
    <VCard>
      <VCardTitle class="headline red--text">
        Confirm Reverse
      </VCardTitle>
      <VDivider />
      <VCardText>
        Are you sure you want to remove this Player?
      </VCardText>
      <VCardActions>
        <VCol cols="12">
          <VBtn class="mr-2" color="error" dark @click="reversePlayer">
            Remove
          </VBtn>
          <VBtn color="secondary" @click="deleteDialog = false">
            Cancel
          </VBtn>
        </VCol>
      </VCardActions>
    </VCard>
  </VDialog>

  <VSnackbar v-model="snack">
    Your player reversed Successfully
  </VSnackbar>

  <LoadingOverlay :isVisible="overlay" />

</template>


<script>
import { get, _delete } from '@/utils/api.js'
import LoadingOverlay from '@/shared/LoadingOverlay.vue';
export default {

  components: {
    LoadingOverlay
  },

  data() {
    return {
      overlay: false,
      projectId: null,
      players: [],
      deleteId: null,
      category: [],
      selectedCategory: null,
      deleteDialog: false,
      snack: false,
    }
  },
  watch: {
    selectedCategory: function () {
      this.getPlayersByTeam()
    },
  },
  mounted() {
    this.projectId = localStorage.getItem('projectId')
    this.getAllCategories()

  },
  methods: {
    async getPlayersByTeam() {
      let obj = this.projectId
      this.overlay = true
      try {
        const response = await get(`/players/unsold/${obj}/${this.selectedCategory}/`)
        this.players = response.data.data
        this.overlay = false

      } catch (error) {
        console.error('Error fetching product options:', error)
        this.overlay = false

      }
    },
    async reversePlayer() {
      this.overlay = true
      try {

        const response = await get(`/auction/reverse-player/${this.deleteId}/`)
        this.snack = true
        this.players = response.data.data
        this.deleteDialog = false
        this.getPlaygiersByTeam()
        this.overlay = false

      } catch (error) {
        console.error('Error fetching product options:', error)
        this.overlay = false

      }
    },
    async getAllCategories() {
      this.overlay = true
      try {

        const response = await get(`/all/category/${this.projectId}/`)
        this.category = response.data.data

        if (this.category.length > 0) {
          this.selectedCategory = this.category[0].id
        }
        this.overlay = false

      } catch (error) {
        console.error('Error fetching product options:', error)
        this.overlay = false

      }
    },

  },
}
</script>

<style>
.image {
  height: 80px;
  width: 80px;
  border-radius: 50%;
}

.center {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.deleteBtn {
  background-color: red;
}

.margin {
  margin-bottom: 30px;
}

.bg {
  background-color: ghostwhite;
}

.heading {
  color: blueviolet;
  font-size: 25px;
}

.text-center {
  text-align: center;
}
</style>