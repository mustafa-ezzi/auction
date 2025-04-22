  <template>
    <div style="background-color: white;border-radius: 30px;">
      <VRow >
        <VCol md="7" sm="12">
          <h1 class="ml-5 mt-2 heading">
            Players
          </h1>
        </VCol>
        <VCol class="left" md="4" sm="5">
        <VBtn class="primary mr-2 mb-2" @click="addPlayerDialog = true">
            Add Player +
          </VBtn>
          <VBtn color="warning" class="mr-2 mb-2" @click="triggerUploadZip">Upload</VBtn>
          <input ref="bulkFileInput" style="display: none" label="Upload Image" chips type="file" class="mr-2"
            @input="handleFileInput" />
          <VBtn color="secondary" class="mb-2" @click="downloadSampleZip">
            Sample
          </VBtn>
        </VCol>
      </VRow>



      <VRow>
        <VCol cols="12">
          <div style="border-radius: 20px;" class="table-container">
            <VTable class="scroll-container" dense fixed-header>
              <thead>
                <tr>
                  <th class="table-header">ID</th>
                  <th class="table-header">Image</th>
                  <th class="table-header">Name</th>
                  <th class="table-header">Category</th>
                  <th class="table-header">Batting / Bowling Style</th>
                  <th class="table-header">Bowling Hand</th>
                  <th class="table-header">Availability</th>
                  <th class="table-header">Fielding Position</th>
                  <th class="table-header">Division</th>
                  <th class="table-header">Previous Team</th>
                  <th class="table-header">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="loading">
                  <td colspan="11">
                    <VProgressLinear color="primary" max="200" indeterminate rounded width="100%" height="10" />
                  </td>
                </tr>
                <tr v-for="(item, index) in players" v-else :key="index">
                  <td class="table-cell">{{ item.id }}</td>
                  <td class="table-cell">
                    <img v-if="item.profile_pic" class="image" :src="item.profile_pic" />
                  </td>
                  <td class="table-cell">{{ item.name }}</td>
                  <td class="table-cell">{{ item.category_name }}</td>
                  <td class="table-cell">{{ item.batting_style }}/{{ item.bowling_style }}</td>
                  <td class="table-cell">{{ item.bowling_hand }}</td>
                  <td class="table-cell">{{ item.availability }}</td>
                  <td class="table-cell">{{ item.fielding_position }}</td>
                  <td class="table-cell">{{ item.division }}</td>
                  <td class="table-cell">{{ item.previous_team }}</td>
                  <td class="table-cell">
                    <VBtn class="m-1" color="primary" size="small" @click="openEditDialog(item)">
                      <VIcon>mdi-edit</VIcon>
                    </VBtn>

                    <VBtn color="error" class="m-1" text="Open Dialog" size="small"
                      @click="Deletedialog = true; deleteId = item.id">
                      <VIcon>mdi-delete</VIcon>
                    </VBtn>
                  </td>
                </tr>
              </tbody>
            </VTable>
          </div>
          <div  style="border-radius: 20px;" class="flex items-center justify-between bg-white px-4 py-3 sm:px-6">
            <div class="flex flex-1 justify-between sm:hidden">
              <a href="#"
                class="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                @click="page = page - 1">Previous</a>
              <a href="#"
                class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                @click="page = page + 1">Next</a>
            </div>
            <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
              <div>
                <p class="text-sm text-gray-700">
                  Showing
                  <span class="font-medium">{{ startItem }}</span>
                  to
                  <span class="font-medium">{{ endItem }}</span>
                  of
                  <span class="font-medium">{{ items.length }}</span>
                  results
                </p>
              </div>
              <div>
                <nav class="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
                  <!-- Previous Button -->

                  <VBtn outline class="ml-1" variant="text" color="warning  " size="small" prepend-icon="mdi-skip-previous"
                    :disabled="currentPage === 1" @click="prevPage">
                    Previous
                  </VBtn>

                  <!-- Current Page Display -->
                  <span class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900">
                    Page {{ currentPage }} of {{ totalPages }}
                  </span>

                  <!-- Next Button -->
                  

                  <VBtn outline class="ml-1" variant="text" color="warning" size="small" prepend-icon="mdi-skip-next"
                  :disabled="currentPage === totalPages" @click="nextPage">
                    Next
                  </VBtn>
                </nav>
              </div>
            </div>
          </div>
        </VCol>
      </VRow>
    </div>

    <!-- Add model -->
    <VDialog v-model="addPlayerDialog" persistent max-width="800">
      <VCard>
        <VCardTitle class="headline purple--text text--darken-3">
          Add Player
        </VCardTitle>
        <VDivider />
        <VCardText>
          <VForm @submit.prevent="submitForm">
            <VContainer>
              <VRow>
                <VCol cols="12" md="6">
                  <VTextField v-model="formData.name" label="Name" />
                </VCol>

                <VCol cols="12" md="4">
                  <div class="image-container" v-if="players.profile_pic">
                    <img :src="players.profile_pic" alt="Player Image"
                      style="width: 100px; height: 100px; margin-left: 132px; border-radius: 50%;" />
                    <VIcon class="delete-icon" @click="openDeleteDialog; imageId = players.id">mdi-delete</VIcon>
                  </div>
                  <VFileInput v-else label="Player Image" chips type="file" @change="handleFileChange" />
                </VCol>
              </VRow>
              <VRow>
                <VCol cols="12" md="4">
                  <VTextField v-model="formData.video" label="Video Link" />
                </VCol>
                <VCol cols="12" md="6">
                  <VSelect v-model="formData.category" label="Category" :items="categories" item-value="id"
                    item-title="name" />
                </VCol>
              </VRow>
              <VRow>
                <VCol cols="12" md="4">
                  <VTextField v-model="formData.batting_style" label="Batting Style" />
                </VCol>

                <VCol cols="12" md="4">
                  <VTextField v-model="formData.bowling_hand" label="Bowling Hand" />
                </VCol>

                <VCol cols="12" md="4">
                  <VTextField v-model="formData.bowling_style" label="Bowling style" />
                </VCol>
              </VRow>
              <VRow>
                <VCol cols="12" md="4">
                  <VTextField v-model="formData.availability" label="Availiblity" />
                </VCol>

                <VCol cols="12" md="4">
                  <VTextField v-model="formData.fielding_position" label="Fielding Position" />
                </VCol>
              </VRow>
              <VRow>
                <VCol cols="12" md="4">
                  <VTextField v-model="formData.division" label="Division" />
                </VCol>

                <VCol cols="12" md="4">
                  <VTextField v-model="formData.previous_team" label="Previous Team" />
                </VCol>
              </VRow>
              <VRow>
                <VCol cols="12">
                  <VBtn type="submit" class="mr-2">
                    Save Changes
                  </VBtn>
                  <VBtn color="secondary" @click="addPlayerDialog = false; this.selectedFile = null; this.resetForm()">
                    Cancel
                  </VBtn>
                </VCol>
              </VRow>
            </VContainer>
          </VForm>
        </VCardText>
      </VCard>
    </VDialog>

    <!-- Delete Modal -->
    <VDialog v-model="Deletedialog" persistent width="450">
      <VCard>
        <VCardTitle class="headline red--text">
          Delete Team
        </VCardTitle>
        <VDivider />
        <VCardText>
          Are you sure you want to delete this item?
        </VCardText>
        <VCardActions>
          <VCol cols="12">
            <VBtn class="mr-2" color="error" dark @click="deleteTeam">
              Delete
            </VBtn>
            <VBtn color="secondary" @click="Deletedialog = false">
              Cancel
            </VBtn>
          </VCol>
        </VCardActions>
      </VCard>
    </VDialog>

    <!-- Edit Modal -->
    <VDialog v-model="editDialog" persistent max-width="800">
      <VCard>
        <VCardTitle class="headline blue--text">
          Update {{ editFormData.name }}
        </VCardTitle>
        <VDivider />
        <VCardText>
          <VForm @submit.prevent="submitEditForm">
            <VContainer>
              <VRow>
                <VCol cols="12" md="6">
                  <VTextField v-model="editFormData.name" label="Name" />
                </VCol>
                <VCol cols="12" md="4">
                  <div class="image-container" v-if="editFormData.profile_pic">
                    <img :src="editFormData.profile_pic" alt="Profile Picture"
                      style="width: 100px; height: 100px; margin-left: 132px; border-radius: 50%;" />
                    <VIcon class="delete-icon" @click="openDeleteDialog">mdi-delete</VIcon>
                  </div>
                  <VFileInput v-else label="Player Image" chips type="file" @change="handleFileChange" />
                </VCol>
              </VRow>
              <VRow>
                <VCol cols="12" md="4">
                  <VTextField v-model="editFormData.video" label="Video Link " />
                </VCol>
                <VCol cols="12" md="6">
                  <VSelect v-model="editFormData.category" label="Category" :items="categories" item-value="id"
                    item-title="name" />
                </VCol>
              </VRow>
              <VRow>
                <VCol cols="12" md="4">
                  <VTextField v-model="editFormData.batting_style" label="Batting Style" />
                </VCol>

                <VCol cols="12" md="4">
                  <VTextField v-model="editFormData.bowling_hand" label="Bowling Hand" />
                </VCol>

                <VCol cols="12" md="4">
                  <VTextField v-model="editFormData.bowling_style" label="Bowling Style" />
                </VCol>
              </VRow>

              <VRow>
                <VCol cols="12" md="4">
                  <VTextField v-model="editFormData.availability" label="Availiblity" />
                </VCol>

                <VCol cols="12" md="4">
                  <VTextField v-model="editFormData.fielding_position" label="Fielding Position" />
                </VCol>
              </VRow>

              <VRow>
                <VCol cols="12" md="4">
                  <VTextField v-model="editFormData.division" label="Division" />
                </VCol>

                <VCol cols="12" md="4">
                  <VTextField v-model="editFormData.previous_team" label="Previous Team" />
                </VCol>
              </VRow>
              <VRow>
                <VCol cols="12">
                  <VBtn type="submit" class="mr-2">
                    Save Changes
                  </VBtn>
                  <VBtn color="secondary" @click="editDialog = false; getAllPlayers()">
                    Cancel
                  </VBtn>
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
          <p>Are you sure you want to delete this Profile Pic </p>
        </VCardText>
        <VCardActions class="justify-center">
          <VBtn color="grey" @click="DeleteLogoDialogue = false">Cancel</VBtn>
          <VBtn color="red" @click="deleteLogo">Delete</VBtn>
        </VCardActions>
      </VCard>
    </VDialog>

    <VSnackbar v-model="showSnackbar" color="success" rounded="pill">
      Record Created / Updated Successfully
    </VSnackbar>

    <VSnackbar v-model="deleteSnackbar" color="error" rounded="pill">
      Your record deleted successfully
    </VSnackbar>

    <VSnackbar v-model="bulkSnackbar" rounded="pill" class="snack">
      {{ message }}
    </VSnackbar>

    <LoadingOverlay :isVisible="overlay" />

  </template>

<script>
import { get, post, patch, _delete } from '@/utils/api.js'
import LoadingOverlay from '@/shared/LoadingOverlay.vue';
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
        category: null,
        batting_style: '',
        bowling_hand: '',
        bowling_style: '',
        availability: '',
        fielding_position: '',
        division: "",
        previous_team: "",
        profile_pic: null,
        is_active: true,
        video:'',
      },
      showSnackbar: false,
      totalPages: 10,
      deleteSnackbar: false,
      bulkSnackbar: false,
      mesasge: null,
      loading: false,
      selectedFile: null,
      selectedZipFile: null,
      items: [],
      Deletedialog: false,
      addPlayerDialog: false,
      categories: [],
      editDialog: false,
      excel: null,
      bulkFileInput: null,
      editFormData: {
        name: '',
        category: null,
        profile_pic: null,
        id: null,
        batting_style: '',
        bowling_hand: '',
        bowling_style: '',
        availability: '',
        fielding_position: '',
        division: '',
        is_active: true,
        video:'',
        previous_team: ''
      },
      tableHeaders: [
        { text: "ID", tooltip: "Unique Player ID" },
        { text: "Name", tooltip: "Player's Full Name" },
        { text: "Category", tooltip: "Player's Category" },
        { text: "Batting/Bowling Style", tooltip: "Batting and Bowling Style" },
        { text: "Bowling Hand", tooltip: "Bowling Hand Preference" },
        { text: "Availability", tooltip: "Player's Current Availability" },
        { text: "Fielding Position", tooltip: "Preferred Fielding Position" },
        { text: "Division", tooltip: "Division Assigned to Player" },
        { text: "Previous Team", tooltip: "Player's Last Team" },
        { text: "Image", tooltip: "Player's Profile Picture" },
        { text: "Actions", tooltip: "Edit or Delete Actions" },
      ],
      deleteId: null,
      page: 0,
      itemsPerPage: 10, // Define how many items to show per page
      currentPage: 1, // Current page number
      totalPages: 0,
    }
  },
  computed: {
    players() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.items.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.items.length / this.itemsPerPage);
    },
    startItem() {
      return (this.currentPage - 1) * this.itemsPerPage + 1;
    },
    endItem() {
      return Math.min(this.currentPage * this.itemsPerPage, this.items.length);

    },
  },
  watch: {
    selectedZipFile() {
      this.uploadZipfile()
      this.selectedZipFile = null

    },
  },
  mounted() {
    // this.fetchIsrcData();
    this.projectId = localStorage.getItem('projectId')
    this.getAllPlayers()
    this.getCategories()

  },
  methods: {
    openDeleteDialog() {

      this.DeleteLogoDialogue = true; // Open the delete confirmation dialog
    },

    async deleteLogo() {
      const obj = {
        id: this.editFormData.id,
        type: 'player',
        subType: null
      }

      try {
        this.overlay = true
        await post(`/delete/image/`, obj);
        this.overlay = false

        this.DeleteLogoDialogue = false
        this.editFormData.profile_pic = null;
        this[this.subType] = null
        this.subType = null
      } catch (error) {
        console.error('Error deleting logo:', error);
      }
    },

    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },


    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    handlePageChange(pageNumber) {
      if (pageNumber >= 1 && pageNumber <= this.totalPages) {
        this.currentPage = pageNumber;
      }
    },



    handleFileInput(event) {
      this.selectedZipFile = event.target.files[0];
      console.log(this.selectedZipFile);
      const fileInput = this.$refs.bulkFileInput;
      if (fileInput) {
        fileInput.value = '';
      }
    },

    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
        this.editFormData.profile_pic = URL.createObjectURL(file);
      }
    },
    closeDeleteDialog() {
      this.Deletedialog = false
    },
    openEditDialog(item) {
      this.editFormData = { ...item }
      this.editFormData.profile_pic = this.editFormData.profile_pic
      this.editDialog = true
    },
    async submitEditForm() {
      const formData = new FormData()

      if (this.selectedFile) {
        formData.append('profile_pic', this.selectedFile)
      }

      for (const key in this.editFormData) {
        if (this.editFormData.hasOwnProperty(key)) {
          formData.append(key, this.editFormData[key])
        }
      }

      formData.append('project', this.projectId)
      this.overlay = true
      try {
        await patch(`/players/${this.editFormData.id}/`, formData)
        this.showSnackbar = true
        this.closeEditDialog()
        this.getAllPlayers() // Update the items after editing
        this.overlay = false
      } catch (error) {
        console.error('Error editing item:', error)
        this.overlay = false

      }
    },
    closeEditDialog() {
      this.editDialog = false

      this.editFormData = {
        name: '',
        category: null,
        batting_style: '',
        bowling_hand: '',
        bowling_style: '',
        availability: '',
        fielding_position: '',
        division: '',
        previous_team: '',
        id: null,
      }
      this.selectedFile = null
    },
    async submitForm() {
      const formData = new FormData()

      if (this.selectedFile) {
        formData.append('profile_pic', this.selectedFile)
      }


      // Loop through the fields and append them to FormData
      for (const key in this.formData) {
        if (this.formData.hasOwnProperty(key)) {
          formData.append(key, this.formData[key])
        }
      }

      formData.append('project', this.projectId)

      this.overlay = true
      try {

        const response = await post('/create/players/', formData)
        this.showSnackbar = true
        this.selectedFile = null

        this.addPlayerDialog = false
        this.getAllPlayers()
        this.resetForm()
        this.message = response.data.message
        this.overlay = false

      } catch (error) {
        console.log(error)
        this.selectedFile = null
        this.resetForm()
        this.overlay = false

      }
    },
    resetForm() {
      this.formData.name = ''
      this.formData.category = null
      this.formData.batting_style = ""
      this.formData.bowling_hand = ""
      this.formData.bowling_style = ""
      this.formData.availability = ""
      this.formData.fielding_position = ""

      this.formData.division = ""
      this.formData.previous_team = ""
      this.formData.video = ""

    },
    async getAllPlayers() {
      let obj = this.projectId
      this.overlay = true
      try {
        const response = await get(`/all/players/${obj}/`)
        this.items = response.data.data
        this.totalPages = Math.ceil(this.items.length / this.itemsPerPage);
        this.overlay = false

      } catch (error) {
        console.error('Error fetching product options:', error)
        this.overlay = false

      }
    },
    async deleteTeam() {
      this.overlay = true
      try {

        const response = await _delete(`/players/${this.deleteId}/`)
        this.deleteSnackbar = true
        this.Deletedialog = false
        this.getAllPlayers()
        this.overlay = false

      } catch (error) {
        console.error('Error deleting product:', error)
        this.overlay = false

      }
    },
    async getCategories() {
      this.overlay = true

      try {
        const response = await get(`/all/category/${this.projectId}/`)
        this.categories = response.data.data
        this.overlay = false

      } catch (error) {
        console.error('Error fetching product options:', error)
        this.overlay = false

      }
    },
    triggerUploadZip() {
      this.$refs.bulkFileInput.click();
      if (this.selectedZipFile) {
        this.selectedZipFile = null
        this.$refs.bulkFileInput.value = null
      }


    },
    async uploadZipfile() {
      try {
        if (!this.selectedZipFile) return

        const _50mb = 50 * 1024 * 1024
        if (this.selectedZipFile.size > _50mb) {
          this.message = 'File size should not exceed 50mb'
          this.bulkSnackbar = true
          this.selectedZipFile = null
          return
        }

        this.overlay = true
        const formData = new FormData()

        formData.append('file', this.selectedZipFile)
        formData.append('project', this.projectId)

        await post('/bulk/', formData)
        this.selectedZipFile = null
        this.message = 'Bulk Upload Player Success'
        this.bulkSnackbar = true
        this.getAllPlayers()
        this.overlay = false

      } catch (error) {
        console.log(error)
        this.selectedZipFile = null
        this.overlay = false
      }
    },
    downloadSampleZip() {
      this.overlay = true
      window.open('https://auction-software-media.s3.us-east-1.amazonaws.com/sample.csv', '_blank')
      this.overlay = false

    },
  },
}

</script>

<style scoped>
.table-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  max-width: 100%;
}

.v-table {
  width: 100%;
  min-width: 1200px;
}

.table-header {
  white-space: nowrap;
  padding: 10px;
  text-align: left;
  font-weight: bold;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
}

.table-cell {
  white-space: nowrap;
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f1f1f1;
  cursor: pointer;
}

.image {
  max-width: 80px;
  height: auto;
  border-radius: 50%;
}


.file-alert {
  font-size: 11px;
  color: red;
}

.image {
  height: 80px;
  width: 80px;
  border-radius: 50%;
}

.v-dialog {
  border-radius: 16px;
}

.v-card {
  border-radius: 16px;
  box-shadow: 0 6px 18px x rgba(0, 0, 0, 0.1);
}

.v-text-field,
.v-select {
  width: 100%;
  margin-bottom: 24px;
  font-size: 1.2rem;
}

.image {
  height: 80px;
  width: 80px;
  border-radius: 50%;
}

.text-center {
  text-align: center;
}

.red--text {
  color: #f44336;
}

.heading {
  color: blueviolet;
  font-size: 25px;

}

.image-container {
  position: relative;
  display: inline-block;
}

.image {
  border-radius: 22%;
  margin: 6px;
}

.dialogue-v-btn {
  margin-right: 12px;
  font-size: 1.2rem;
  min-width: 120px;
}

.v-btn.primary {
  background-color: #4caf50;
  color: #fff;

}
.left{
  margin-left: 146px;
  max-width : 29.333333%
}


.v-btn.secondary {
  background-color: #f44336;
  color: #fff;
}

.heading {
  color: blueviolet;
  font-size: 25px;
}

.delete-icon {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  margin: auto;
  margin-left: 20px;
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

.head {
  max-width: 56%
}
</style>
