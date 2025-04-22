<template>
  <div class="container auth-wrapper" :style="{ backgroundImage: backgroundUrl }">
    <VCard class="auth-card pa-6 pt-8 shadow-lg rounded-xl">
      <VCardItem class="justify-center mb-6">
        <!-- <template #prepend>
          <div class="d-flex mb-4">
            <div v-html="logo" />
          </div>
        </template> -->
        <VCardTitle class="heading text-uppercase">
          Welcome to {{ this.project_name }}
        </VCardTitle>
      </VCardItem>

      <VCardText class="pt-2">
        <h5 class="subheading center font-weight-semibold mb-1">
          Adventure starts here 🏏
        </h5>
        <p class="mb-0 x-small center">
          Submit the player details to register for the event!
        </p>
      </VCardText>

      <VCardText>
        <VForm @submit.prevent="submitForm" v-model="isValid">
          <!-- Name -->
          <VRow class="mb-2">
            <VCol cols="12" md="8">
              <VTextField
                v-model="formData.name"
                :rules="[rules.required]"
                label="Name"
                outlined
                dense
                required
              />
            </VCol>
            <VCol cols="12" md="4">
              <VFileInput
                ref="fileInput"
                label="Player Image"
                :rules="[rules.requiredFile]"
                chips
                type="file"
                @change="handleFileChange"
              />
            </VCol>
          </VRow>

          <!-- Batting and Bowling Details -->
          <VRow class="mb-4">
            <VCol cols="12" md="6">
              <VSelect
                v-model="formData.category"
                label="Category"
                :items="categories"
                item-value="id"
                item-title="name"
                :rules="[rules.required]"
                outlined
                dense
                required
              />
            </VCol>
            <VCol cols="12" md="6">
              <VTextField
                v-model="formData.batting_style"
                label="Batting Style"
                outlined
                dense
              />
            </VCol>
          </VRow>

          <VRow class="mb-4">
            <VCol cols="12" md="6">
              <VTextField
                v-model="formData.bowling_hand"
                label="Bowling Hand"
                outlined
                dense
              />
            </VCol>
            <VCol cols="12" md="6">
              <VTextField
                v-model="formData.bowling_style"
                label="Bowling Style"
                outlined
                dense
              />
            </VCol>
          </VRow>

          <!-- Availability and Fielding -->
          <VRow class="mb-4">
            <VCol cols="12" md="6">
              <VTextField
                v-model="formData.availability"
                label="Availability"
                outlined
                dense
              />
            </VCol>
            <VCol cols="12" md="6">
              <VTextField
                v-model="formData.fielding_position"
                label="Fielding Position"
                outlined
                dense
              />
            </VCol>
          </VRow>

          <!-- Division and Previous Team -->
          <VRow class="mb-4">
            <VCol cols="12" md="6">
              <VTextField
                v-model="formData.division"
                label="Division"
                outlined
                dense
              />
            </VCol>
            <VCol cols="12" md="6">
              <VTextField
                v-model="formData.previous_team"
                label="Previous Team"
                outlined
                dense
              />
            </VCol>
          </VRow>

          <!-- Submit and Cancel Buttons -->
          <VRow>
            <VCol cols="12" class="d-flex justify-end flex-wrap">
              <VBtn
                type="submit"
                color="primary"
                class="elevation-2 mr-4 mb-2"
                large
                :disabled="!isValid"
              >
                Submit
              </VBtn>
              <VBtn
                outlined
                color="grey"
                large
                class="mb-2"
                @click="resetForm"
              >
                Reset
              </VBtn>
            </VCol>
          </VRow>
        </VForm>
      </VCardText>
    </VCard>

    <VDialog v-model="isDialogVisible" max-width="500" transition="zoom-in-transition">
      <VCard class="success-dialog elevation-3">
        <!-- Video Section -->
        <VCardTitle class="text-center justify-center">
          <video
            src="../assets/images/approve.mp4"
            autoplay
            loop
            muted
            class="success-video"
          ></video>
        </VCardTitle>

        <!-- Success Message -->
        <VCardText>
          <h3 class="text-center text-success mb-4 glow-text">
            Player Registered Successfully!
          </h3>
          <p class="text-center">The player has been added to the system.</p>
        </VCardText>

        <!-- Actions -->
        <VCardActions class="d-flex justify-center">
          <VBtn color="success" class="elevation-2" large @click="closeDialog">
            OK!
          </VBtn>
        </VCardActions>
      </VCard>
    </VDialog>
  </div>
</template>

<script>
import logo from "@/assets/logo.svg?raw";
import { get, post } from "@/utils/api.js";
import Stadium from "../assets/images/1234.jpg";

export default {
  data() {
    return {
      isValid: false,
      formData: {
        name: "",
        category: null,
        batting_style: "",
        bowling_hand: "",
        bowling_style: "",
        availability: "",
        fielding_position: "",
        division: "",
        previous_team: "",
        profile_pic: null,
        is_active: false,
      },
      rules: {
        required: (value) => !!value || "This field is required.",
        requiredFile: () => !!this.selectedFile || "File is required.",
      },
      project_name: "",
      categories: [],
      projects: [],
      selectedFile: null,
      backgroundUrl: `url(${Stadium})`,
      isDialogVisible: false,
    };
  },

  mounted() {
    const projectId = this.$route.params.projectId;
    this.getCategories(projectId);
    this.getProject(projectId);
  },

  methods: {
    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
      }
    },

    async submitForm() {
      const formData = new FormData();

      if (this.selectedFile) {
        formData.append("profile_pic", this.selectedFile);
      }
      for (const key in this.formData) {
        if (this.formData.hasOwnProperty(key)) {
          formData.append(key, this.formData[key]);
        }
      }
      const projectId = this.$route.params.projectId;
      formData.append("project", projectId);
      try {
        const response = await post("/create/players/", formData);
        this.isDialogVisible = true;
        this.selectedFile = null;
        this.$emit("success", response.data.message);
      } catch (error) {
        console.error("Error submitting form:", error);
      }
    },

    closeDialog() {
      this.isDialogVisible = false;
      window.location.reload();
    },

    async getCategories(projectId) {
      try {
        const response = await get(`/all/category/${projectId}/`);
        this.categories = response.data.data;
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
    },

    async getProject(projectId) {
      try {
        const response = await get(`/project/${projectId}/`);
        this.project_name = response.data.data.name;
        console.log(this.project_name);
      } catch (error) {
        console.error("Error fetching project:", error);
      }
    },

    resetForm() {
      this.formData = {
        name: "",
        category: null,
        batting_style: "",
        bowling_hand: "",
        bowling_style: "",
        availability: "",
        fielding_position: "",
        division: "",
        previous_team: "",
        profile_pic: null,
      };
      window.location.reload();
      this.selectedFile = null;
    },
  },
};
</script>

<style scoped>
/* Container styles */
.container {
  min-height: 100vh;
  overflow-y: auto;
  padding: 2rem 1rem;
  background-color: #f5f5f5;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* Auth wrapper to center the content */
.auth-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

/* Auth card responsiveness */
.auth-card {
  width: 90%;
  max-width: 800px;
  margin: 0 auto;
  /* Additional padding is handled via Vuetify classes */
}

@media (min-width: 600px) {
  .auth-card {
    width: 80%;
  }
}

@media (min-width: 960px) {
  .auth-card {
    width: 800px;
  }
}

/* Heading font size responsive */
.heading {
  color: #a705cd;
  font-size: 16px;
  text-align: center;
}

@media (min-width: 600px) {
  .heading {
    font-size: 32px;
  }
}

@media (min-width: 960px) {
  .heading {
    font-size: 40px;
  }
}


@media (min-width: 600px) {
  .subheading {
    font-size: 1.5rem ;
  }
}

@media (min-width: 960px) {
  .subheading {
    font-size: 2.5rem ;
  }
}

@media (min-width: 600px) {
  .x-small {
    font-size: 15px;
  }
}

@media (min-width: 960px) {
  .x-small {
    font-size: 15px ;
  }
}

.x-small{
font-size: 15px;
}

.center{
  text-align: center;
  /* font-size: 1.5rem; */
}
.subheading{
  font-size: 1.2rem ;
}

/* Button hover effect */
.v-btn {
  transition: background-color 0.3s, transform 0.3s;
}

.v-btn:hover {
  background-color: #28a745;
  transform: scale(1.05);
}

/* Success dialog styling */
.success-dialog {
  border-radius: 12px;
  overflow: hidden;
  background-color: #eaebeb;
  width: 90%;
  max-width: 500px;
  margin: 0 auto;
}

/* Responsive video in dialog */
.success-video {
  width: 100%;
  max-width: 249px;
  height: auto;
  border-radius: 50%;
  display: block;
  margin: 0 auto;
}



/* Additional adjustments for small screens */
@media (max-width: 600px) {
  .auth-card {
    padding: 1.5rem;
  }
  .v-btn {
    width: 100%;
  }
}
</style>

<route lang="yaml">
meta:
  layout: blank
</route>
