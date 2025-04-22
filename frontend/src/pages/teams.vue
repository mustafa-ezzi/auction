<template>
  <div style="background-color: white;border-radius: 30px;">

    <VRow>
      <VCol sm="6" md="9">
        <h1 class="ml-5 mt-2 heading">Teams</h1>
      </VCol>
      <VCol sm="6" class="mb-3" md="3">
        <VBtn class="primary left" @click="createTeam = true">
          Add Teams +
        </VBtn>
      </VCol>
    </VRow>
    <!-- table for showing data -->
    <VTable style="border-radius: 20px;">
      <thead>

        <tr>
          <th>Name</th>
          <th>Logo</th>
          <th>Purse Allocated</th>
          <th>Purse Available</th>
          <th>Username</th>
          <th>Password</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.name">
          <td>{{ item.name }}</td>
          <td>
            <img v-if="item.logo" class="image" :src="item.logo" />
          </td>
          <td>{{ item.purse_allocated }}</td>
          <td>{{ item.available_purse }}</td>
          <td>{{ item.username }}</td>

          <td>
            <div class="d-flex align-center">
              <span v-if="!item.showPassword"></span>
              <span v-else>{{ item.password }}</span>

              <VIcon small class="ml-2" @click="togglePasswordVisibility(item)">
                {{ item.showPassword ? 'mdi-eye-off' : 'mdi-eye' }}
              </VIcon>
            </div>
          </td>

          <td>
            <VBtn class="m-1" color="primary" size="small" @click="openEditDialog(item)">
              <VIcon>mdi-edit</VIcon>
            </VBtn>

            <VBtn color="error" class="m-1" text="Open Dialog" size="small"
              @click="deleteDialog = true, deleteId = item.id">
              <VIcon>mdi-delete</VIcon>
            </VBtn>
          </td>
        </tr>
      </tbody>
    </VTable>
  </div>
  <!-- Delete dialogue -->
  <VDialog v-model="deleteDialog" persistent width="450">
    <VCard>
      <VCardTitle class="headline red--text"> Confirm Delete ? </VCardTitle>
      <VDivider />
      <VCardText> Are you sure you want to delete this item? </VCardText>
      <VCardActions>
        <!-- {{ item.id }} -->
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

  <!-- edit dialogue -->
  <VDialog v-model="editDialog" persistent max-width="550">
    <VCard>
      <VCardTitle class="headline blue--text"> Update {{ editformData.name }} </VCardTitle>
      <VDivider />
      <VCardText>
        <VForm @submit.prevent="submitEditForm">
          <VContainer>
            <VRow>
              <VCol cols="12" md="6">
                <VTextField v-model="editformData.name" label="Name" required hide-details />
              </VCol>

              <VCol cols="12" md="6">
                <div v-if="editformData.logo" class="image-container">
                  <img :src="editformData.logo" alt="Logo" style="width: 100px; height: 100px; border-radius: 50%" />
                  <VIcon class="delete-icon" @click="openDeleteDialog">mdi-delete</VIcon>
                </div>
                <VFileInput v-else ref="fileInput" label="Upload Image" chips type="file" @change="handleFileChange" />
              </VCol>

              <VCol cols="12" md="6">
                <VTextField v-model="editformData.purse_allocated" type="number" label="Purse Allocated" hide-details
                  required />
              </VCol>

              <VCol cols="12" md="6">
                <VTextField v-model="editformData.available_purse" type="number" label="Purse Available" hide-details
                  required />
              </VCol>
            </VRow>

            <VRow>
              <VCol cols="12">
                <VBtn type="submit" class="mr-2">Save Changes</VBtn>
                <VBtn color="secondary" @click="editDialog = false">Cancel</VBtn>
              </VCol>
            </VRow>
          </VContainer>
        </VForm>
      </VCardText>
    </VCard>
  </VDialog>

  <!-- delete Profile Pic -->
  <VDialog v-model="DeleteLogoDialogue" persistent max-width="400">
    <VCard>
      <VCardTitle class="headline red--text text-center">
        <VIcon large>mdi-delete</VIcon> Delete Confirmation
      </VCardTitle>
      <VDivider />
      <VCardText class="text-center">
        <p>Are you sure you want to delete this Profile Pic</p>
      </VCardText>
      <VCardActions class="justify-center">
        <VBtn color="grey" @click="DeleteLogoDialogue = false">Cancel</VBtn>
        <VBtn color="red" @click="deleteLogo">Delete</VBtn>
      </VCardActions>
    </VCard>
  </VDialog>

  <!-- Create Dialogue -->
  <VDialog v-model="createTeam" persistent width="550">
    <VCard>
      <VCardTitle class="headline red--text"> Add Teams </VCardTitle>
      <VDivider />
      <VCardText>
        <VForm @submit.prevent="submitForm">
          <VContainer>
            <VRow>
              <VCol cols="12" md="6">
                <VTextField v-model="formData.name" label="Name" hide-details />
              </VCol>

              <VCol cols="12" md="6">
                <VFileInput ref="fileInput" label="Upload Image" chips type="file" @change="handleFileChange" />
              </VCol>

              <VCol cols="12" md="6">
                <VTextField v-model="formData.purse_allocated" type="number" label="Purse Allocated" hide-details
                  required />
              </VCol>

              <VCol cols="12" md="6">
                <VTextField v-model="formData.available_purse" type="number" label=" Purse Available" hide-details
                  required />
              </VCol>
            </VRow>
            <VRow>
              <VCol cols="12">
                <VBtn type="submit" class="mr-2">
                  Save Changes
                </VBtn>
                <VBtn color="secondary" @click="createTeam = false">
                  Cancel
                </VBtn>
              </VCol>
            </VRow>
          </VContainer>
        </VForm>
      </VCardText>
    </VCard>
  </VDialog>

  <LoadingOverlay :isVisible="overlay" />

  <VSnackbar v-model="snackbar" color="error" rounded="pill">
    {{ message }}
  </VSnackbar>
 </template>

<script>
import { get, post, patch, _delete } from '@/utils/api.js'
import LoadingOverlay from '@/shared/LoadingOverlay.vue'
export default {
  components: {
    LoadingOverlay,
  },
  data() {
    return {
      overlay: false,
      DeleteLogoDialogue: false,
      projectId: null,
      formData: {
        name: '',
        purse_allocated: 0,
        available_purse: 0,
        logo: null,
      },
      editformData: {
        name: '',
        password: '',
        username: '',
        id: null,
        purse_allocated: 0,
        available_purse: 0,
        logo: null,
      },
      showPassword: false,
      items: [],
      deleteDialog: false,
      createTeam: false,
      editDialog: false,
      selectedFile: null,
      deleteId: null,
      message: null,
      snackbar: false,
    }
  },
  mounted() {
    this.projectId = localStorage.getItem('projectId')
    this.getAllTeamsByProjectId()
  },

  methods: {
    openDeleteDialog() {
      this.DeleteLogoDialogue = true
    },

    async deleteLogo() {
      const obj = {
        id: this.editformData.id,
        type: 'team',
        subType: null,
      }

      try {
        this.overlay = true
        await post(`/delete/image/`, obj)
        this.editformData.logo = null
        this.selectedFile = null
        this.overlay = false
        this.DeleteLogoDialogue = false
        this[this.subType] = null
        this.subType = null
      } catch (error) {
        console.error('Error deleting logo:', error)
      }
    },

    handleFileChange(event) {
      const file = event.target.files[0]
      if (file) {
        this.selectedFile = file
        this.editformData.logo = URL.createObjectURL(file)
      }
    },
    openEditDialog(item) {
      this.editformData = { ...item }
      this.selectedFile = this.editformData.logo
      this.editDialog = true
    },

    async submitEditForm() {
      const formData = new FormData()
      if (this.selectedFile) {
        formData.append('logo', this.selectedFile)
      } else if (!this.editformData.logo) {
        this.editformData.logo = null
        this.selectedFile = null
      }

      for (const key in this.editformData) {
        if (this.editformData.hasOwnProperty(key)) {
          formData.append(key, this.editformData[key])
        }
      }

      formData.append('project', this.projectId)

      this.overlay = true
      try {
        await patch(`/teams/${this.editformData.id}/`, formData)
        this.message = 'Record Created / Updated Successfully'
        this.snackbar = true
        this.getAllTeamsByProjectId()
        this.closeEditDialog()
        this.overlay = false
      } catch (error) {
        console.error('Error editing item:', error)
        this.overlay = false
      }
    },

    closeEditDialog() {
      this.editDialog = false
      this.selectedFile = null
      this.editformData = {
        name: '',
        purse_allocated: 0,
        purse_available: 0,
        id: null,
      }
    },
    async submitForm() {
      const formData = new FormData()

      if (this.selectedFile) {
        formData.append('logo', this.selectedFile)
      } else {
        this.message = 'Team Logo Missing'
        this.snackbar = true
        return
      }

      for (const key in this.formData) {
        if (this.formData.hasOwnProperty(key)) {
          formData.append(key, this.formData[key])
        }
      }

      formData.append('project', this.projectId)

      this.overlay = true
      try {
        await post('/create/teams/', formData)
        this.showSnackbar = true
        this.createTeam = false
        this.selectedFile = null
        this.getAllTeamsByProjectId()
        this.resetForm()
        this.overlay = false
      } catch (error) {
        console.log(error)
        this.overlay = false
      }
    },
    togglePasswordVisibility() {
      this.showPassword = true
    },
    async getAllTeamsByProjectId() {
      this.overlay = true
      try {
        const response = await get(`/all/teams/${this.projectId}/`)
        this.items = response.data.data.map(item => ({ ...item, showPassword: false }))
      } catch (error) {
        console.error('Error fetching teams:', error)
      } finally {
        this.overlay = false
      }
    },

    async deleteTeam() {
      this.overlay = true
      try {
        await _delete(`/teams/${this.deleteId}/`)
        this.message = 'Record Deleted Successfully'
        this.snackbar = true
        this.deleteDialog = false
        this.getAllTeamsByProjectId()
        this.overlay = false
      } catch (error) {
        console.error('Error deleting product:', error)
        this.overlay = false
      }
    },
    togglePasswordVisibility(item) {
      item.showPassword = !item.showPassword
    },
    resetForm() {
      // Reset the form data to its initial state
      this.formData.name = ''
      this.formData.purse_allocated = 0
      this.formData.available_purse = 0
      this.formData.logo = null
    },
  },
}
</script>

<style>
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

.green-text {
  color: green;
}

.red-text {
  color: red;
}

.left {
  margin-left: 130px;
  /* max-width : 29.333333% */
}

.image {
  height: 80px;
  width: 80px;
  border-radius: 50%;
  margin: 7px;
}

.text-center {
  text-align: center;
}

.delete-icon {
  position: absolute;
  margin-top: -19%;
  margin-left: 76px;
  background-color: rgba(0, 0, 0, 0.5);
  /* margin: 30px; */
  color: white;

  padding: 5px;
  border-radius: 50%;
  cursor: pointer;
  display: none;
}

.logo {
  margin-bottom: 16px;
  margin-left: 46%;
  font-weight: 700;
  color: black;
}

.image-container:hover .delete-icon {
  display: block;
}

.heading {
  color: blueviolet;
  font-size: 25px;
}
</style>
