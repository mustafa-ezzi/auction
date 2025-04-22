<template>
    <div style="background-color: white;border-radius: 30px;">

  <VRow>
    <VCol md="9" sm="12">
      <h1 class="ml-5 mt-2 heading">
        Player - Team
      </h1>
    </VCol>
    <VCol md="3" sm="12" class="mb-3 ">
      <VSelect class="mr-4"  v-model="selectedTeam" label="Teams" :items="teams" item-value="id" item-title="name" />
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
        <th>
          Sold Price
        </th>
        <th>Category</th>
        <th />
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in players" :key="item.name">
        <!-- <td >{{ item.id }}</td> -->
        <td>{{ item.name }}</td>
        <td >
          <img v-if="item.profile_pic" class="image mt-1 mb-1" :src="item.profile_pic">
        </td>
        <td>
          <div class="sold-price-wrapper">
            <span>{{ item.sold_price }}</span>
            <!-- <VBtn class="edit-btn" icon color="green"> -->
              <VIcon style="margin-left: 18px;"  @click="openEditSoldDialog(item)">mdi-pencil</VIcon>
            <!-- </VBtn> -->
          </div>
        </td>
        <td>{{ item.category_name }}</td>
        
        <td>
          <VBtn class="mr-2" color="primary" size="small" @click="deleteDialog = true; deleteId = item.id">
            <VIcon>mdi-delete</VIcon>
          </VBtn>
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

  <VSnackbar v-model="Soldsnack">
    Player's sold price UPDATED!
  </VSnackbar>
  <LoadingOverlay :isVisible="overlay" />

   


    <VDialog v-model="editSoldDialog" persistent max-width="400">
    <VCard>
      <VCardTitle class="headline text-center">Edit Sold Price</VCardTitle>
      <VDivider />
      <VCardText>
        <VForm @submit.prevent="UpdateSoldPrice">
          <VTextField v-model="soldPrice" label="Sold Price" type="number" required />
        </VForm>
        <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
      </VCardText>
      <VCardActions class="justify-center">
        <VBtn color="grey" @click="editSoldDialog = false, this.errorMessage = ''">Cancel</VBtn>
        <VBtn color="green" @click="UpdateSoldPrice">Save</VBtn>
      </VCardActions>
    </VCard>
  </VDialog>

</template>


<script>
import { get, patch, _delete } from '@/utils/api.js'
import LoadingOverlay from '@/shared/LoadingOverlay.vue'
export default {
  components: {
    LoadingOverlay,
  },
  data() {
    return {
      projectId: null,
      editSoldDialog:false,
      players: [],
      deleteId: null,
      teams: [],
      // editForm: {
      //   sold_price:''
      // },
      editSoldDialog: false, // Controls the visibility of the edit sold price dialog
      soldPrice: null,       // Holds the sold price value for editing
      currentPlayerId: null,
      selectedTeam: null,
      deleteDialog: false,
      snack: false,
      Soldsnack:false,
      overlay: false,
      errorMessage: '',
    }
  },
  watch: {
    selectedTeam: function () {
      this.getPlayersByTeam()
    },
  },
  mounted() {
    this.projectId = localStorage.getItem('projectId')
    this.getAllTeams()

  },
  methods: {
    
    async getPlayersByTeam() {
      this.overlay = true
      try {
        const response = await get(`/players/team/${this.selectedTeam}/`)
        this.players = response.data.data
        this.overlay = false
      } catch (error) {
        console.error('Error fetching product options:', error)
        this.overlay = false

      }
    },
    async reversePlayer() {
      try {
        const response = await get(`/auction/reverse-player/${this.deleteId}/`)
        this.snack = true
        this.deleteDialog = false
        this.getPlayersByTeam()
      } catch (error) {
        console.error('Error fetching product options:', error)
      }
    },
    async getAllTeams() {
      this.overlay = true

      try {
        const response = await get(`/all/teams/${this.projectId}/`)
        this.teams = response.data.data
        this.overlay = false

        if (this.teams.length > 0) {
          this.selectedTeam = this.teams[0].id
        }

      } catch (error) {
        console.error('Error fetching product options:', error)
      }
    },
    openEditSoldDialog(player) {
      // Prepopulate the soldPrice and playerId for editing
      this.soldPrice = player.sold_price
      this.currentPlayerId = player.id
      this.editSoldDialog = true
    },
    async UpdateSoldPrice() {
  try {
    const formData = { sold_price: this.soldPrice };
    await patch(`/auction/update/sold_price/${this.currentPlayerId}/`, formData);
    this.editSoldDialog = false;
    this.snack = true;
    this.getPlayersByTeam(); // Refresh player list
  } catch (error) {
    console.error('Error updating sold price:', error);
    if (error.response && error.response.data && error.response.data.message) {
      this.errorMessage = error.response.data.message; // Set error message from API response
    } else {
      this.errorMessage = 'An unexpected error occurred.'; // Fallback error message
    }
    
  }
}

  },
}
</script>

<style>
.image {
  height: 80px;
  width: 80px;
  border-radius: 50%;
}



.heading {
  color: blueviolet;
  font-size: 25px;
}

.text-center {
  text-align: center;
}
.error-text {
  color: red;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}
</style>