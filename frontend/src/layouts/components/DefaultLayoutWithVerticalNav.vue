<template>
  <VerticalNavLayout>
    <template #navbar>
      <VSpacer />
      <VSpacer />
      <VSpacer />
      <VSpacer />
      <VSelect v-model="selectedProject" item-title="name" item-value="id" :items="projects" />

      <VBtn class="ml-3 " variant="text"  color="primary" size="large" prepend-icon="mdi-folder-plus-outline"
        @click="openModal = true">
        Create Project
      </VBtn>

      <VBtn class="" variant="text" color="danger" size="large" prepend-icon="mdi-logout" @click="logout">
      LogOut  
      </VBtn>


    </template>

    <template #navigation-drawer-content>
      <DrawerContent />
    </template>

    <div class="layout-page-content">
      <RouterView />
    </div>
  </VerticalNavLayout>


  <VDialog v-model="openModal" persistent width="500">
    <VCard>
      <VCardTitle class="headline">
        Create New Project
      </VCardTitle>
      <VDivider />
      <VCardText>
        <VRow class="mb-4">
          <VCol cols="12">
            <VTextField v-model="name" label="Project Name" required />
          </VCol>
        </VRow>
        <VRow>
          <VCol cols="12">
            <VBtn :disabled="name == ''" class="mr-2" @click="createNewProject">
              Submit
            </VBtn>
            <VBtn :disabled="projects.length == 0" color="secondary" @click="openModal = false">
              Cancel
            </VBtn>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>
  </VDialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import DrawerContent from './DrawerContent.vue'
import { VerticalNavLayout } from '@layouts'
import { useRouter } from 'vue-router'

// Components
import { get, post } from '@/utils/api.js'

const openModal = ref(false)
const projects = ref([])
const selectedProject = ref(null)
const isMounted = ref(false)
const name = ref('')
const router = useRouter()
const username = ref(localStorage.getItem('username') || '')
const role = ref(localStorage.getItem('role') || '')

watch(selectedProject, newValue => {
  if (isMounted.value == true) {
    isMounted.value = false

    return
  }
  localStorage.setItem('projectId', newValue)
  location.reload()
})

async function getAllProjects() {
  try {
    const response = await get('/project/')
    projects.value = response.data.data

    if (projects.value.length == 0) {
      localStorage.removeItem('projectId')
      openModal.value = true
    } else if (!selectedProject.value) {
      selectedProject.value = projects.value[0].id
    }

  } catch (error) {
    console.error('Error fetching product options:', error)
  }
}

async function createNewProject() {
  try {
    const response = await post('/create/project/', { name: name.value })
    openModal.value = false
    getAllProjects()
  } catch (error) {
    console.error('Error fetching product options:', error)
  }
}

function logout() {
  localStorage.clear()
  router.push('/login')
}

onMounted(() => {
  getAllProjects()
  let project = localStorage.getItem('projectId')
  if (project) {
    isMounted.value = true
    selectedProject.value = Number(project)
  }
})
</script>



<style scoped lang="scss">
.app-bar-search {
  .heading {
    color: blueviolet;
  }
}

.indigo {
  color: indigo;
}

@media only screen and (max-width: 600px) {
  .desktop {
    display: none;
  }
}

@media only screen and (min-width: 768px) {
  .mobile {
    display: none !important;
  }
}

.chip {
  color: indigo;
  width: 83px;
  height: 26px;
  font-size: 12px;
}
.small{
  font-size: small;
}
</style>
