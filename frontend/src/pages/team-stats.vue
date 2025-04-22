<template>
  <VContainer>
    <VRow v-if="team" class="team-info-row">
      <VCol cols="12" md="6" class="purse-info">
        <img v-if="team.logo" class="image" :src="team.logo">
        <h1 class="team-name">
          {{ team.name }}
        </h1>
      </VCol>

      <VCol cols="12" md="4" class="purse-info">
        <span class="purse-label">Available Purse: {{ team.available_purse }}</span>
      </VCol>

      <VCol cols="12" md="2" class="purse-info" style="justify-content: end;">
        <VBtn icon variant="text" color="warning" @click="getTeamById">
          <VIcon size="32" icon="mdi-refresh" />
        </VBtn>
        <VBtn icon variant="text" color="error" @click="logout">
          <VIcon size="32" icon="mdi-logout" />
        </VBtn>
      </VCol>
    </VRow>

    <!-- table for showing data -->

    <VRow>
      <VTable class="width-100">
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
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in players" :key="item.name">
            <td>{{ item.name }}</td>
            <td>
              <img v-if="item.profile_pic" class="image" :src="item.profile_pic">
            </td>
            <td>{{ item.sold_price }}</td>
            <td>{{ item.category_name }}</td>
          </tr>
        </tbody>
      </VTable>
    </VRow>
  </VContainer>
</template>


<script>
import { get, _delete } from '@/utils/api.js'

export default {

  data() {
    return {
      players: [],
      team: {},
      selectedTeam: null,
    }
  },
  mounted() {
    this.selectedTeam = localStorage.getItem('teamId')

    if (!this.selectedTeam) {
      localStorage.clear()
      this.$router.push('/login')
    } else {
      this.getTeamPlayers()
      this.getTeamById()
    }
  },
  methods: {

    async getTeamPlayers() {
      try {
        const response = await get(`/players/team/${this.selectedTeam}/`)
        this.players = response.data.data
      } catch (error) {
        console.error('Error fetching product options:', error)
      }
    },
    async getTeamById() {
      try {
        const response = await get(`/teams/${this.selectedTeam}/`)
        this.team = response.data.data
      } catch (error) {
        console.error('Error fetching product options:', error)
      }
    },
    logout() {
      localStorage.clear()
      this.$router.push('/login')
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

.heading {
  color: blueviolet;
  font-size: 25px;
}

.team-info-row {
  background-color: black;
  border-radius: 12px;

}

.team-name {
  color: white;
  font-size: 27px;
  font-weight: 800;
  margin-left: 12px;
}

.purse-info {
  display: flex;
  align-items: center;
}

.purse-label {
  font-weight: bold;
  font-size: 20px;
  color: whitesmoke;
}

.width-100 {
  width: 100%;
  margin-top: 12px;
}

.v-table {
  max-width: 100%;
  overflow-x: auto;
}

.v-table tbody tr {
  height: 2rem;
}

@media (min-width: 376px) {

  .purse-label {
    font-weight: bold;
    font-size: 25px;
    color: whitesmoke;
  }

  .team-name {
    color: white;
    font-size: 35px;
    font-weight: 800;
    margin-left: 12px;
  }

  .team-info-row {
    background-color: black;
    border-radius: 12px;
    margin-bottom: 20px;
    margin-top: 20px;
  }


}
</style>

<route lang="yaml">
meta:
    layout: blank
</route>