<template lang="pug">
RiverHeader
router-view
</template>

<script setup>
	import RiverHeader from "@/components/RiverHeader.vue";

	import {useMain} from "@/config/stores/main";
	const mainStore = useMain()

	mainStore.loadVideo()
</script>

<style scoped>

</style>
