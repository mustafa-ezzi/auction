<template>
  <div style="background-color: white;border-radius: 30px;">
    <VRow>
      <VCol sm="6" md="9">
        <h1 class="ml-5 mt-2 heading">
          Category
        </h1>
      </VCol>
      <VCol sm="6" md="3">
        <VBtn  class="primary  left" @click="addCategoryDialog = true">
          Add Category +
        </VBtn>
      </VCol>
    </VRow>
    

    <VRow>
      <VCol cols="12">
        <VTable style="border-radius: 20px;">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Players</th>
              <th>Base Price</th>
              <th>
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="6">
                <VProgressLinear color="primary" max="500" indeterminate rounded width="10" height="10" />
              </td>
            </tr>
            <tr v-for="(item, index) in items" v-else :key="index">
              <td>{{ item.id }}</td>
              <td>{{ item.name }}</td>
              <td>
                {{ item.player }}
              </td>
              <td>
                {{ item.base_price }}
              </td>

              <td>
                <VBtn class="m-1" color="primary" size="small" @click="openEditDialog(item)">
                  <VIcon>mdi-edit</VIcon>
                </VBtn>

                <VBtn color="error" class="m-1" text="Open Dialog" size="small"
                  @click="deleteDialog = true; deleteId = item.id">
                  <VIcon>mdi-delete</VIcon>
                </VBtn>
              </td>
            </tr>
          </tbody>
        </VTable>
      </VCol>
    </VRow>
  </div>


  <VDialog v-model="editDialog" max-width="500" persistent>
    <VCard>
      <VCardTitle class="headline blue--text">
        Update {{ editFormData.name }}
      </VCardTitle>
      <VDivider />
      <VCardText>
        <VForm @submit.prevent="submitEditForm">
          <VRow>
            <VCol cols="12" md="12">
              <VTextField v-model="editFormData.name" label="Name" required />
            </VCol>

            <VCol cols="12" md="12">
              <VTextField v-model="editFormData.base_price" type="number" label="Base Price" required />
            </VCol>

            <VCol cols="12" md="12">
              <VTextField v-model="editFormData.player" type="number" label="Max Players" required />
            </VCol>
          </VRow>

          <VRow class="mt-6">
            <VCol cols="12">
              <VBtn type="submit" class="mr-2">
                Save Changes
              </VBtn>
              <VBtn color="secondary" @click="editDialog = false">
                Cancel
              </VBtn>
            </VCol>
          </VRow>
        </VForm>
      </VCardText>
    </VCard>
  </VDialog>

  <VDialog v-model="deleteDialog" width="450" persistent>
    <VCard>
      <VCardTitle class="headline red--text">
        Confirm Delete
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
          <VBtn color="secondary" @click="deleteDialog = false">
            Cancel
          </VBtn>
        </VCol>
      </VCardActions>
    </VCard>
  </VDialog>

  <VDialog v-model="addCategoryDialog" max-width="500" persistent>
    <VCard>
      <VCardTitle class="headline">
        Add Category
      </VCardTitle>
      <VDivider />
      <VCardText>
        <VForm @submit.prevent="submitForm">
          <VRow>
            <VCol cols="12" md="12">
              <VTextField v-model="formData.name" label="Name" required />
            </VCol>

            <VCol cols="12" md="12">
              <VTextField v-model="formData.base_price" type="number" label="Base Price" required />
            </VCol>

            <VCol cols="12" md="12">
              <VTextField v-model="formData.player" type="number" label="Max Players" required />
            </VCol>
          </VRow>

          <VRow class="mt-6">
            <VCol cols="12">
              <VBtn type="submit" class="mr-2">
                Submit
              </VBtn>
              <VBtn color="secondary" @click="addCategoryDialog = false">
                Cancel
              </VBtn>
            </VCol>
          </VRow>
        </VForm>
      </VCardText>
    </VCard>
  </VDialog>

  <VSnackbar v-model="showSnackbar" color="success" rounded="pill">
      Record Created / Updated Successfully
    </VSnackbar>

    <VSnackbar v-model="deleteSnackbar" color="error" rounded="pill">
      Your record deleted successfully
    </VSnackbar>

  <LoadingOverlay :isVisible="overlay" />

</template>

<script>
import { get, post, patch, _delete } from '@/utils/api.js'
import LoadingOverlay from '@/shared/LoadingOverlay.vue';
export default {
  components: {
    LoadingOverlay
  },
  data() {
    return {
      overlay: false,
      projectId: null,
      formData: {
        name: '',
        base_price: 0,
        player: '',
      },
      showSnackbar: false,

      addCategoryDialog: false,
      deleteDialog: false,
      loading: false,
      items: [],
      editDialog: false,
      editFormData: {
        name: '',
        base_price: 0,
        purse: 0,
        player: 0,
        id: null,
      },
      deleteId: null,
      deleteSnackbar: false,

    }
  },

  mounted() {
    this.projectId = localStorage.getItem('projectId')
    this.getAllCategories()
  },
  methods: {
    closeDeleteDialog() {
      this.deleteDialog = false
    },
    openEditDialog(item) {
      this.editFormData = { ...item }
      this.editDialog = true
    },
    async submitEditForm() {
      let obj = this.editFormData
      obj['project'] = this.projectId
      this.overlay = true

      try {
        const response = await patch(`/categories/${this.editFormData.id}/`, obj)
        this.showSnackbar = true

        this.editDialog = false
        this.getAllCategories()
        this.closeEditDialog()
        this.overlay = false

      } catch (error) {
        console.error('Error editing item:', error)
        this.overlay = false

      }
    },
    closeEditDialog() {
      this.editDialog = false

      this.editFormData = {
        unit: '',
        min_players: 0,
        purse: 0,
        max_players: 0,
        id: null,
      }
    },
    async submitForm() {
      let obj = this.formData
      obj['project'] = this.projectId
      this.overlay = true

      try {
        const response = await post('/create/categories/', obj)

        this.showSnackbar = true
        this.getAllCategories()
        this.addCategoryDialog = false
        this.resetForm()
        this.overlay = false

      } catch (error) {
        console.log(error)
        this.overlay = false

      }
    },

    resetForm() {
      // Reset the form data to its initial state
      this.formData.name = ''
      this.formData.base_price = 0
      this.formData.player = ''

    },

    async getAllCategories() {
      this.overlay = true
      try {
        const response = await get(`/all/category/${this.projectId}/`)
        this.items = response.data.data
        this.overlay = false

      } catch (error) {
        console.error('Error fetching product options:', error)
        this.overlay = false

      }

    },
    async deleteTeam() {
      this.overlay = true
      try {
        const response = await _delete(`/categories/${this.deleteId}/`)
        this.deleteSnackbar = true
        this.deleteDialog = false
        this.getAllCategories()
        this.overlay = false

      } catch (error) {
        console.error('Error deleting product:', error)
        this.overlay = false

      }
    },
  },
}
</script>

<style scoped>
.margin {
  margin-bottom: 30px;
}

.left{
  margin-left: 116px;
  /* max-width : 29.333333% */
}
.snack {
  color: white;
}

.heading {
  color: blueviolet;
  font-size: 25px;
}
</style>