<template>
    <div style="background-color: white;border-radius: 30px;">

  <VRow>
    <VCol cols="9">
      <h1 class="ml-5 mt-2 heading mb-3">
        Admin Panel
      </h1>
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
          Logo
        </th>
        
        <th>
          Actions
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in projects" :key="item.name">
        <td>{{ item.name }}</td>
        <td>
          <img v-if="item.logo" class="image" :src="item.logo">
        </td>
        
        <td>
          <VBtn class="m-1" color="primary" size="small" @click="getTeamList(item.id)">
            <VIcon>mdi-download</VIcon>
          </VBtn>
          <VBtn color="error" class="m-1" m-1 size="small" @click="deleteDialog = true; deleteId = item.id">
            <VIcon>mdi-delete</VIcon>
          </VBtn>
        </td>
      </tr>
    </tbody>
  </VTable>
  </div>
  <!-- delete dialog -->
  <VDialog v-model="deleteDialog" persistent width="450">
    <VCard>
      <VCardTitle class="headline red--text">
        Confirm Delete
      </VCardTitle>
      <VDivider />
      <VCardText>
        Are you sure you want to delete this Project?
      </VCardText>
      <VCardActions>
        <VCol cols="12">
          <VBtn class="mr-2" color="error" dark @click="deleteTeam">
            Delete
          </VBtn>
          <VBtn color="secondary" @click="deleteDialog = false">
            Cancel
          </VBtn>
        </VCol>
      </VCardActions>
    </VCard>
  </VDialog>
  <VSnackbar v-model="deleteSnackbar" color="error" rounded="pill">
    Your record deleted successfully
  </VSnackbar>
  <LoadingOverlay :isVisible="overlay" />

</template>


<script>
import { get, _delete } from '@/utils/api.js'
import * as XLSX from 'xlsx'
import LoadingOverlay from '@/shared/LoadingOverlay.vue';
export default {
  components: {
    LoadingOverlay
  },
  data() {
    return {
      overlay: false,
      projectId: null,
      projects: [],
      deleteDialog: false,
      deleteId: null,
      deleteSnackbar: false,
    }
  },

  mounted() {
    this.projectId = localStorage.getItem('projectId')
    this.getAllProjects()

  },

  methods: {

    async getAllProjects() {
      this.overlay = true
      try {
        const response = await get(`/project/`)
        this.projects = response.data.data

        this.overlay = false
      } catch (error) {
        console.error('Error fetching product options:', error)
        this.overlay = false

      }
    },
    async deleteTeam() {
      try {
        this.overlay = true

        const response = await _delete(`/project/${this.deleteId}/`)
        this.deleteSnackbar = true
        this.deleteDialog = false
        this.overlay = false

        this.getAllProjects()
      } catch (error) {
        console.error('Error deleting product:', error)
        this.overlay = false

      }
    },

    async getTeamList(projectId) {
      this.overlay = true

      const response = await get('/generate-csv/' + projectId)

      // Extract data from the API response
      const data = response.data.data

      // Map the data to include only relevant properties
      const formattedData = data.map(item => ({
        name: item.name,
        category_name: item.category_name,
        sold_price: item.sold_price,
        batting_style: item.batting_style,
        bowling_hand: item.bowling_hand,
        bowling_style: item.bowling_style,
        fielding_position: item.fielding_position,
        availability: item.availability,
        previous_team: item.previous_team,
        division: item.division,
        team: item.team_name,
      }))

      // Create a worksheet
      const ws = XLSX.utils.json_to_sheet(formattedData)

      // Create a workbook with the worksheet
      const wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, ws, 'Players List')

      // Create a Blob from the workbook
      XLSX.writeFile(wb, 'list.xlsx')
      this.overlay = false

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