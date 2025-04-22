<template>
  <VCard class="pa-8" style="border-radius: 30px;">
    <VRow>
      <VCol cols="3">
        <h1 class="heading">
          Settings
        </h1>
      </VCol>


      <VCol cols="12">
        <!-- Form for adding a new setting -->
        <VForm @submit.prevent="submitForm">
          <VRow>
            <VCol cols="12" md="6">
              <VTextField v-model="formData.name" label="Project Name" required />
            </VCol>

            <VCol cols="12" md="6">
              <VTextField v-model="formData.unit" label="Project Unit" required />
            </VCol>


            <VCol cols="12">
              <VTextarea v-model="formData.description" label="Project Description" required />
            </VCol>

            <VCol cols="12" md="3">
              <div class="image-container" v-if="logo">
                <h1 class="logo"> Logo</h1>
                <img :src="logo" alt="Project Logo" style="width: 130px;height: 139px;border-radius: 33px;" />
                <VIcon class="delete-icon" @click="openDialog('logo')">mdi-delete</VIcon>
              </div>
              <VFileInput v-else label="Project Logo" chips type="file" @change="handleFileChange" />
            </VCol>

            <VCol cols="12" md="3">
              <div class="image-container" v-if="background">
                <h1 class="background-text">Auction Background </h1>
                <img :src="background" alt="Background" style="width: 130px; height: 130px; border-radius: 33px; " />
                <VIcon class="delete-icon" @click="openDialog('background')">mdi-delete</VIcon>
              </div>
              <VFileInput v-else label="Add Background" chips type="file" @change="handleBackgroundLogo" />
            </VCol>

            <VCol cols="12" md="3">
              <div class="image-container" v-if="sponsor1">
                <h1 class="sponsor1">Sponsor 1</h1>
                <img :src="sponsor1" alt="Sponsor 1 Logo" style="width: 130px; height: 130px; border-radius: 33px;" />
                <VIcon class="delete-icon" @click="openDialog('sponsor1')">mdi-delete</VIcon>
              </div>
              <VFileInput v-else label="Sponsor 1 Logo" chips type="file" @change="handleSponsor1Logo" />
            </VCol>

            <VCol cols="12" md="3">
              <div class="image-container" v-if="sponsor2">
                <h1 class="sponsor2">Sponsor 2 </h1>
                <img :src="sponsor2" alt="Sponsor 2 Logo" style="width: 130px; height: 130px;  border-radius: 33px;" />
                <VIcon class="delete-icon" @click="openDialog('sponsor2')">mdi-delete</VIcon>
              </div>
              <VFileInput v-else label="Sponsor 2 Logo" chips type="file" @change="handleSponsor2Logo" />
            </VCol>


          </VRow>
          <VRow>

            <VCol cols="12">
              <VBtn type="submit" class="mr-2 mt-5">
                Save Changes
              </VBtn>
            </VCol>
          </VRow>
        </VForm>
      </VCol>
    </VRow>
  </VCard>

  <LoadingOverlay :isVisible="overlay" />

  <!-- delete logo -->
  <VDialog v-model="deleteDialog" persistent max-width="400">
    <VCard>
      <VCardTitle class="headline red--text">Delete Confirmation</VCardTitle>
      <VDivider />
      <VCardText>
        Are you sure you want to delete this {{ subType }}?
      </VCardText>
      <VCardActions>
        <VBtn color="grey" @click="deleteDialog = false; subType = null;">Cancel</VBtn>
        <VBtn color="red" @click="deleteImage()">Delete</VBtn>
      </VCardActions>
    </VCard>
  </VDialog>

  <VSnackbar v-model="showSnackbar" color="success" rounded="pill">
      Record Created / Updated Successfully
    </VSnackbar>

  <!-- ALL DIALOGS ARE HERE -->
</template>


<script>
import { get, post, patch, _delete } from '@/utils/api.js'
import LoadingOverlay from '@/shared/LoadingOverlay.vue'

export default {
  components: {
    LoadingOverlay
  },
  data() {
    return {
      deleteDialog: false,
      subType: null,
      overlay: false,
      projectId: null,
      selectedFile: null,
      selectedSponsor1: null,
      selectedSponsor2: null,
      selectedbackground: null,
      logo: null,
      sponsor1: null,
      sponsor2: null,
      background: null,
      showSnackbar: false,
      formData: {
        unit: '',
        min_players: 0,
        max_players: 0,
        description: '',
        name: '',
      },
    }
  },
  mounted() {
    this.projectId = localStorage.getItem('projectId')
    if (this.projectId) {
      this.getProjectSettings()
    }
  },
  methods: {
    async deleteImage() {
      const obj = {
        id: this.projectId,
        type: 'settings',
        sub_type: this.subType
      }

      try {
        this.overlay = true
        await post(`/delete/image/`, obj);
        if (this.subType === 'logo') {
          this.logo = null
        } else if (this.subType === 'sponsor1') {
          this.sponsor1 = null;
        } else if (this.subType === 'sponsor2') {
          this.sponsor2 = null;
        } else if (this.subType === 'background') {
          this.background = null;
        }
        this.subType = null
        this.deleteDialog = false
        this.overlay= false
      } catch (error) {
        console.error('Error deleting logo:', error);
      }
    },


    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.logo = URL.createObjectURL(file);
        this.selectedFile = file;

      }
    },

    handleSponsor1Logo(event) {
      const file = event.target.files[0];
      if (file) {
        this.sponsor1 = URL.createObjectURL(file);
        this.selectedSponsor1 = file;
      }
    },

    handleSponsor2Logo(event) {
      const file = event.target.files[0];
      if (file) {
        this.sponsor2 = URL.createObjectURL(file);
        this.selectedSponsor2 = file;

      }
    },

    handleBackgroundLogo(event) {
      const file = event.target.files[0];
      if (file) {
        this.background = URL.createObjectURL(file);
        this.selectedbackground = file;

      }
    },


    async submitForm() {
      const formData = new FormData()

      if (this.selectedFile) {
        formData.append('logo', this.selectedFile)
      }

      if (this.selectedSponsor1) {
        formData.append('sponsor1', this.selectedSponsor1)
      }

      if (this.selectedSponsor2) {
        formData.append('sponsor2', this.selectedSponsor2)
      }

      if (this.selectedbackground) {
        formData.append('background', this.selectedbackground)
      }

      for (const key in this.formData) {
        if (this.formData.hasOwnProperty(key)) {
          formData.append(key, this.formData[key])
        }
      }

      this.overlay = true
      try {
        await patch(`/project/${this.projectId}/`, formData)
        this.getProjectSettings()
        this.showSnackbar = true
        this.overlay = false

      } catch (error) {
        console.error('Error editing item:', error)
        this.overlay = false

      }
    },

    async getProjectSettings() {
      this.overlay = true
      try {
        const response = await get(`/project/${this.projectId}/`)
        let obj = response.data.data
        this.formData['name'] = obj['name']
        this.formData['description'] = obj['description']
        this.formData['min_players'] = 0
        this.formData['max_players'] = 0
        this.formData['unit'] = obj['unit']
        this.logo = obj['logo']
        this.sponsor1 = obj['sponsor1']
        this.sponsor2 = obj['sponsor2']
        this.background = obj['background']

        this.overlay = false
      } catch (error) {
        console.error('Error fetching product options:', error)
        this.overlay = false

      }
    },
    openDialog(subType) {
      this.subType = subType
      this.deleteDialog = true;
    }
  },
}
</script>

<style scoped>
.image {
  height: 80px;
  width: 80px;
  border-radius: 50%;
}

.heading {
  color: blueviolet;
  font-size: 25px;
}

.image-container {
  position: relative;
  display: inline-block;
}



.delete-icon {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  margin: auto;
  padding: 5px;
  border-radius: 50%;
  cursor: pointer;
  display: none;
}


.logo {
  margin-bottom: 16px;
  margin-left: 32%;
  font-weight: 700;
  color: black;
}

.background-text {
  margin-bottom: 19px;
  margin-left: -20px;
  font-weight: 700;
  color: black;
}

.image-container:hover .delete-icon {
  display: block;
}

.sponsor1 {
  margin-bottom: 16px;
  margin-left: 13%;
  font-weight: 700;
  color: black;
}

.sponsor2 {
  margin-bottom: 16px;
  margin-left: 20%;
  font-weight: 700;
  color: black;
}
</style>