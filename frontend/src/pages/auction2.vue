<template>
    <div v-if="isLoaded" class="divStyle"
        :style="{ backgroundImage: selectedProject.background ? `url(${selectedProject.background})` : 'none', overflow: 'hidden' }">

        <div class="row justify-center">
            <div class="col-2 d-flex align-items-center" v-if="selectedProject.sponsor1">
                <VImg class="mt-2 ml-2" :src="selectedProject.sponsor1" />
            </div>

            <div class="col-8" :class="{ 'col-10': !selectedProject.sponsor1 && !selectedProject.sponsor2 }">
                <VImg class="mx-auto mt-8 center" :src="selectedProject.logo" />
                <div class="mt-2 grid gap-[0.5rem] opacity-80 transition-all duration-300 grid-cols-4"
                    :class="{ 'grid-cols-5': !selectedProject.sponsor1 && !selectedProject.sponsor2 }">
                    <div v-for="(team, key) in teams" :key="key"
                        class="h-full rounded-md overflow-hidden bg-black shadow-lg rounded-3xl hover:bg-gray-700"
                        @click="soldPlayer(team)">
                        <div class="grid h-full">
                            <div class="md:mb-0 flex justify-between cart">
                                <img :src="team.team_logo" class="object-cover cardImage p-2" />

                                <p class="text-end">
                                <h5 class="text-lg font-semibold text-white mr-6">
                                    {{ team.team_name }}
                                </h5>

                                <h6 class="text-md text-white mr-6">
                                    Max Bid : {{ team.max_bid }}
                                </h6>

                                <h7 class="text-sm text-white mr-6">
                                    Remaining: {{ playersPurchased(team.categories) }}
                                </h7>
                                </p>

                            </div>
                        </div>
                    </div>
                </div>
                <div v-if="playerLoading" class="mt-16">
                    <v-progress-linear indeterminate color="green"></v-progress-linear>
                </div>
                <template v-else>
                    <div v-if="player && player.video" style="justify-items: center;">
                        <video class="video" :src="player.video" autoplay controls width="840" height="460">
                            Your browser does not support the video tag.
                        </video>
                    </div>
                    <div v-else-if="player && player.name"
                        class="mt-12 grid grid-cols-1 lg:grid-cols-[65%_35%] pt-2 pl-2 pr-2 align-center w-[66rem] mx-auto rounded-tl-[50px] rounded-tr-[200px] bg-white opacity-80">
                        <div class="mb-0 p-5  ">
                            <h5 class="text-6xl font-bold leading-tight mb-4">
                                {{ player.name }}
                            </h5>
                            <h5 class="text-xl font-semibold leading-tight mb-4 textheading pt-6">
                                Category: <span class="text-yellow-500">{{ player.category_name }}</span>
                            </h5>
                            <h5 class="text-xl font-semibold leading-tight mb-4 textheading pt-6">
                                Availability: <span class="text-yellow-500">{{ player.availability }}</span>
                            </h5>
                        </div>

                        <div class="mb-0 p-5">
                            <img v-if="player.profile_pic" :src="player.profile_pic"
                                class="object-cover rounded-[50px] h-[220px]" alt="">
                        </div>
                    </div>
                    <div v-else class="text-center mt-16 no-player">
                        <h3 class="text-2xl font-bold text-red-900 leading-tight textheading">
                            No Player Available!
                        </h3>
                    </div>
                </template>
            </div>

            <div class="col-2 d-flex align-items-center" v-if="selectedProject.sponsor2">
                <VImg class="mt-2 mr-2" :src="selectedProject.sponsor2" />
            </div>
        </div>

        <footer class="width-100 fixed bottom-0 text-center py-4 container mx-auto text-gray-500 text-sm bg-black">
            <div class="md:flex justify-between items-center">
                <div class="flex text">
                    <div class="col-lg-4 col-12">
                        <VTextField v-model="points" :disabled="!player" type="number" class="text input-field"
                            placeholder="Bid Amount" />
                    </div>
                    <div class="col-lg-4 col-12">
                        <VSelect v-model="selectedCategory" class=" text input-field" label="Category"
                            :items="categories" item-value="id" item-title="name" />
                    </div>
                    <div class="col-lg-4 col-12">
                        <VTextField v-model="playerId" type="number" class="text input-field" placeholder="Player Id" />
                    </div>
                </div>
                <div class="lg:flex">
                    <div class="col-md-4 col-12">
                        <button type="button"
                            class="text-white second-button bg-[#2557D6] hover:bg-[#2557D6]/90 focus:ring-4 focus:ring-[#2557D6]/50 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#2557D6]/50 me-2 mb-2 "
                            @click="getRandomPlayer">
                            <VImg :src="batting" cover class="first-button-image" alt="Cricket Image" />
                            Player
                        </button>
                    </div>

                    <div class="col-md-4 col-12">
                        <button type="button"
                            class="text-white second-button bg-[#2557D6] hover:bg-[#2557D6]/90 focus:ring-4 focus:ring-[#2557D6]/50 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#2557D6]/50 me-2 mb-2 "
                            @click="resetPlayers">
                            <VImg :src="cricket" cover class="first-button-image" alt="Cricket Image" />
                            Reset
                        </button>
                    </div>

                    <div class="col-md-4 col-12">
                        <button type="button"
                            class="text-white second-button bg-[#2557D6] hover:bg-[#2557D6]/90 focus:ring-4 focus:ring-[#2557D6]/50 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#2557D6]/50 me-2 mb-2 "
                            @click="goHome">
                            <VImg :src="home" cover class="first-button-image" alt="Cricket Image" />
                            Home
                        </button>
                    </div>
                </div>
            </div>
        </footer>
    </div>

    <div v-else class="container center divStyle" :style="{ backgroundImage: backgroundUrl }">
        <div class="center-container">
            <VCard class="cart-bg">
                <VCardText>
                    <VSelect v-model="selectedProject" label="Projects" return-object :items="projects"
                        item-title="name" />

                    <div class="center-containers">
                        <VBtn :disabled="!selectedProject" class="mt-5" @click="initialize">
                            Click Here to Start Auction
                        </VBtn>
                    </div>
                </VCardText>
            </VCard>
        </div>
    </div>

    <VDialog v-model="dialog" width="960px" persistent>
        <VCard>
            <img :src="sold" style="max-width: 25%;" class="mx-auto mt-4" />
            <VCardText class="dialog-cart-text">

                <p class="text-2xl font-bold text-grey-700 leading-tight">
                    <span class="text-3xl font-bold text-grey-700 leading-tight"><b>{{ player.name }}</b></span> sold
                    to <span class="selected-team text-3xl font-bold  leading-tight">{{ selectedTeam.team_name
                        }}</span>
                    in
                    <span class="text-3xl font-bold text-grey-700 leading-tight"><b>{{ points }}</b></span> {{
                        selectedProject.unit }}
                </p>
            </VCardText>
            <VCardActions>
                <VSpacer />
                <VBtn class="error" text="Close" @click="closeDialog">
                    Close
                </VBtn>
            </VCardActions>
        </VCard>
    </VDialog>
</template>

<script>
import { get, post } from '@/utils/api.js'
import batting from '@/assets/images/logos/batting.png'
import congratulation from '@/assets/images/logos/congratulation.png'
import sold from '@/assets/images/sold.jpeg'
import cricket from '@/assets/images/logos/cricket.png'
import Stadium from '@/assets/images/stadium.png'
import home from '@/assets/images/logos/home.png'

export default {
    data() {
        return {
            dialog: false,
            selectedTeam: {},
            teams: [],
            player: {},
            isLoaded: false,
            selectedCategory: null,
            projects: [],
            selectedProject: null,
            categories: null,
            openDialog: false,
            points: null,
            batting: batting,
            congratulation: congratulation,
            sold: sold,
            cricket: cricket,
            home: home,
            backgroundUrl: `url(${Stadium}) `,
            playerId: null,
            playerLoading: false
        }
    },
    watch: {
        selectedProject() {
            this.getCategories()
        },
    },
    mounted() {
        this.getProjects()
    },
    methods: {
        async goHome() {
            this.$router.push('/');
        },
        async getTeamsMaxBid() {
            const obj = {
                'category_id': this.selectedCategory,
                'project_id': this.selectedProject.id
            }
            const response = await post('/auction/teams-bid/', obj)
            this.teams = response.data.data
        },

        async getRandomPlayer() {

            if (!this.selectedProject || (!this.selectedCategory && !this.playerId)) return

            try {
                this.getTeamsMaxBid()
                this.playerLoading = true
                this.player = {}

                const obj = {
                    'category_id': this.selectedCategory,
                    'project_id': this.selectedProject.id,
                    'player_id': this.playerId
                }

                const response = await post('/auction/random-player/', obj)
                this.player = response.data.data
                this.playerId = null
                this.playerLoading = false
            } catch (error) {
                this.playerLoading = false
                console.error('Error loading player:', error)
            }
        },


        async soldPlayer(team) {

            if (!team.team_id || !this.points || !this.player) return

            try {
                let obj = {
                    'team_id': team.team_id,
                    'sold_price': this.points,
                    'player_id': this.player.id,
                }

                this.selectedTeam = team

                await post('/auction/sold-player/', obj)
                this.dialog = true
                this.getTeamsMaxBid()
            } catch (error) {
                console.error('Error editing item:', error)
            }
        },
        async getProjects() {
            try {
                const response = await get('/project/')
                this.projects = response.data.data
            } catch (error) {
                console.error('Error fetching product options:', error)
            }
        },
        async getCategories() {

            try {
                const response = await get(`/all/category/${this.selectedProject.id}/`)
                this.categories = response.data.data
            } catch (error) {
                console.error('Error fetching product options:', error)
            }
        },
        initialize() {
            this.isLoaded = true
        },
        playersPurchased(categories) {
            let purchased = 0
            let available = 0
            categories.forEach(e => {
                purchased = e.purchased + purchased + e.remaining
                available = e.remaining + available
            })

            return `${available} / ${purchased}`
        },
        async resetPlayers() {
            await get(`/players/reset/${this.selectedProject.id}/`)
        },
        closeDialog() {
            this.dialog = false
            this.player = {}
            this.points = null
            this.selectedTeam = {}
        },
    },

}
</script>

<style>
.divStyle {
    background-size: cover;
    height: 96vh;
}

.cardImage {
    width: 35%;
    height: 100px;
}

.textheading {
    font-size: 30px;
}

.divPicture {
    width: 80%;
    height: 500px;
    border-radius: 30%;
}

.cart {
    cursor: pointer;
}

.cart-bg {
    width: 400px;
}

.center-container {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
}

.center-containers {
    display: flex;
    align-items: center;
    justify-content: center;
}

.text {
    color: white;
}

.input-field {
    width: 200px;
}

.center-container {
    display: flex;
    align-items: center;
    justify-content: center;
}

.dialog-image {
    width: 50%;
    place-self: center;
}

.selected-team {
    color: green;
}

.dialog-cart-text {
    text-align: center;
}

.first-button-image {
    width: 30px;
    margin-right: 10px;
}

.second-button-image {
    width: 30px;
    margin-right: 10px;
}

.width-100 {
    max-width: 100%;
}

.no-player {
    height: 600px;
    padding-top: 8%;
}

.video {
    margin-top: 70px;
}
</style>


<route lang="yaml">
meta:
    layout: blank
</route>