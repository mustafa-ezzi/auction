<script setup>
import {
  VerticalNavLink,
  VerticalNavSectionTitle,
} from '@layouts'
</script>

<template>
  <!-- 👉 Nav header -->
  <div class="nav-header">
    <RouterLink to="/" class="app-logo d-flex align-center gap-x-3 app-title-wrapper">
      <Transition name="vertical-nav-app-title">
        <h1 class="font-weight-bold leading-normal text-xl text-uppercase">
          Auction Pro
        </h1>
      </Transition>
    </RouterLink>
  </div>

  <!-- 👉 Nav items -->
  <ul class="sidebar-menu">
    <div class=" ">
      <!-- 👉 Project Section -->
      <VerticalNavSectionTitle :item="{ heading: 'PROJECT' }" />
      <VerticalNavLink class="m-0 p-0 " :item="{ title: 'Categories', to: 'category', icon: { icon: 'mdi-pill' } }" />
      <VerticalNavLink class="m-0 p-0" :item="{ title: 'Players', to: 'players', icon: { icon: 'mdi-human' } }" />
      <VerticalNavLink class="m-0 p-0" :item="{ title: 'Teams', to: 'teams', icon: { icon: 'mdi-account-multiple' } }" />
      <VerticalNavLink class="m-0 p-0" :item="{ title: 'Settings', to: 'settings', icon: { icon: 'mdi-settings' } }" />

      <!-- 👉 Admin Section -->
      <VerticalNavSectionTitle :item="{ heading: 'ADMIN' }" />
      <VerticalNavLink class="m-0 p-0"
        :item="{ title: 'Team Players', to: 'teams-players', icon: { icon: 'mdi-account-group' } }" />
      <VerticalNavLink class="m-0 p-0"
        :item="{ title: 'Unsold Players', to: 'unsold-players', icon: { icon: 'mdi-account-remove-outline' } }" />
      <VerticalNavLink class="m-0 p-0" :item="{ title: 'Projects', to: 'projects', icon: { icon: 'mdi-dock-window' } }" />

      <!-- 👉 Auction Section -->
      <VerticalNavSectionTitle :item="{ heading: 'AUCTION' }" />
      <a style="color: rgb(74 71 80);"  href="auction1" target="_blank">
      <VerticalNavLink class="m-0 p-0 "
        :item="{ title: ' Auction 1',  icon: { icon: 'mdi-apps' } }" />
        </a>
        <a style="color: rgb(74 71 80);"  href="auction2" target="_blank">
      <VerticalNavLink class="m-0 p-0 "
        :item="{ title: ' Auction 2',  icon: { icon: 'mdi-apps-box' } }" href="auction2" />
        </a>
    </div>
  </ul>
</template>

<style lang="scss">
/* Sidebar styles */
.sidebar-menu {
  max-height: 100vh;
  overflow: hidden; /* Hide scrollbar by default */
  transition: all 0.3s ease;
}

.sidebar-menu:hover {
  overflow-y: auto; /* Show scrollbar on hover */
}


.nav-header {
  padding: 16px;
  color: #fff;
  font-size: 16px;
  text-align: center;
}

/* Section title */
.vertical-nav-section-title {
  font-family: 'Poppins', sans-serif;
  color: black;
  // font-size: small;
  font-weight: bold;
  text-transform: uppercase;
  margin: 10px 0;
}

/* Nav link styles */
.vertical-nav-link {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  font-family: 'Poppins', sans-serif;
  font-size: medium;
  color: black;
  transition: background 0.3s ease, color 0.3s ease;
}

.vertical-nav-link:hover {
  background: #f0f0f0;
  color: #000;
}

.vertical-nav-link .mdi {
  margin-right: 8px;
}

/* Active link styling */
.vertical-nav-link.router-link-active {
  background: #007bff;
  color: #fff;
}

/* Scrollbar styles */
::-webkit-scrollbar {
  width: 6px;
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.5);
}


</style>
