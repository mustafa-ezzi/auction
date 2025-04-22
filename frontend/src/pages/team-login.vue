<script setup>
import { useTheme } from 'vuetify'
import logo from '@/assets/logo.svg?raw'
import AuthProvider from '@/views/pages/authentication/AuthProvider.vue'
import authV1MaskDark from '@/assets/images/pages/auth-v1-mask-dark.png'
import authV1MaskLight from '@/assets/images/pages/auth-v1-mask-light.png'
import authV1Tree2 from '@/assets/images/pages/auth-v1-tree-2.png'
import authV1Tree from '@/assets/images/pages/auth-v1-tree.png'
import { useRouter } from 'vue-router'
import { get, post, patch, _delete } from '@/utils/api.js'


const form = ref({
  username: '',
  password: '',
})

const vuetifyTheme = useTheme()
const authThemeMask = computed(() => {
  return vuetifyTheme.global.name.value === 'light' ? authV1MaskLight : authV1MaskDark
})

const isPasswordVisible = ref(false)
const router = useRouter()

const login = async () => {

  try {
    const response = await post('/team/login/', form.value)
    if (response.data.data) {
      localStorage.setItem('teamLogin', 'true')
      localStorage.setItem('teamId', response.data.data.id)
      router.push('/team-stats')
    } else {
      alert('Invalid Credentials')
    }
  } catch {
    alert('Invalid Credentials')
  }

}
</script>

<template>
  <div class="auth-wrapper d-flex align-center justify-center pa-4">
    <VCard
      class="auth-card pa-4 pt-7"
      width="450"
    >
      <VCardItem class="justify-center">
        <!--
          <template #prepend>
          <div class="d-flex">
          <div v-html="logo" />
          </div>
          </template> 
        -->

        <VCardTitle class="font-weight-semibold text-2xl text-uppercase">
          Auction Pro
        </VCardTitle>
      </VCardItem>

      <VCardText class="pt-2 ">
        <h5 class="text-h5 text-center font-weight-semibold mb-1">
          Team Login 👋🏻
        </h5>
      </VCardText>

      <VCardText>
        <VForm @submit.prevent="() => { }">
          <VRow>
            <!-- email -->
            <VCol cols="12">
              <VTextField
                v-model="form.username"
                label="Username"
                type="email"
              />
            </VCol>

            <!-- password -->
            <VCol cols="12">
              <VTextField
                v-model="form.password"
                label="Password"
                :type="isPasswordVisible ? 'text' : 'password'"
                :append-inner-icon="isPasswordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                @click:append-inner="isPasswordVisible = !isPasswordVisible"
              />

              <!--
                remember me checkbox
                <div class="d-flex align-center justify-space-between flex-wrap mt-1 mb-4">
                <VCheckbox v-model="form.remember" label="Remember me" />
                </div> 
              -->

              <!-- login button -->
              <VBtn
                class="mt-4"
                block
                type="submit"
                @click="login"
              >
                Login
              </VBtn>
            </VCol>
          </VRow>
        </VForm>
      </VCardText>
    </VCard>

    <VImg
      class="auth-footer-start-tree d-none d-md-block"
      :src="authV1Tree"
      :width="250"
    />

    <VImg
      :src="authV1Tree2"
      class="auth-footer-end-tree d-none d-md-block"
      :width="350"
    />

    <!-- bg img -->
    <VImg
      class="auth-footer-mask d-none d-md-block"
      :src="authThemeMask"
    />
  </div>
</template>

<style lang="scss">
@use "@core/scss/pages/page-auth.scss";
</style>

<route lang="yaml">
meta:
  layout: blank
</route>
