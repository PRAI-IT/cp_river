<template lang="pug">
.titleBlock
	.contentTitle
		.title Рекомендации для вас
		.subTitle Отметьте видео, которые вам нравятся и поставьте
			img(src="/img/icons/redHeart.gif")
			|Если не зашло, то поставьте
			img(src="/img/icons/angryFace.gif")
	.btnBlue(@click="mainStore.loadVideo()" v-if="!(mainStore.getListVideo.length === 0 && !mainStore.spinner)")
		span Следующие 10 рекомендаций
		img(src="/img/icons/arrowRight.svg")
.listVideo
	RiverItemVideo(v-for="item of mainStore.getListVideo" :video="item"
		@openModal="$_river_index_openModal($event,item.id)")
.noData(v-if="mainStore.getListVideo.length === 0 && !mainStore.spinner") Видимо что то пошло не так, обновите страницу и попробуйте ещё раз
.footer(v-if="!(mainStore.getListVideo.length === 0 && !mainStore.spinner)")
	.btnBlue(@click="mainStore.loadVideo()")
		span Следующие 10 рекомендаций
		img(src="/img/icons/arrowRight.svg")
transition(name="fade" mode="out-in")
	RiverItemModal(v-if="modalItem.show" :coords="modalItem.coords" :id="modalItem.id"
		@close="modalItem.show = false")
transition(name="fadeAll" mode="out-in")
	RiverSpinner(v-if="mainStore.spinner")
</template>

<script setup>
	import {defineAsyncComponent,ref} from "vue";

	import RiverItemVideo from "@/components/RiverItemVideo.vue";
	const RiverItemModal = defineAsyncComponent(()=>import("@/components/RiverItemModal.vue"))
	const RiverSpinner = defineAsyncComponent(()=>import("@/components/RiverSpinner.vue"))

	import {useMain} from "@/config/stores/main";
	const mainStore = useMain()

	const modalItem = ref({
		show:false,
		coords:[0,0],
		id:''
	})

	function $_river_index_openModal(coords,id){
		modalItem.value.coords = coords
		modalItem.value.id = id
		modalItem.value.show = true
	}
</script>

<style scoped lang="scss">
	.titleBlock{
		display: flex;
		justify-content: space-between;
		align-items: flex-end;
		flex-wrap: wrap;
		margin-bottom: 24px;
		.title{
			font-size: 24px;
			font-weight: 700;
			line-height: 29px;
			margin-bottom: 24px;
		}
		.subTitle{
			font-size: 18px;
			font-weight: 400;
			line-height: 22px;
			img{
				height: 20px;
				margin: 0 3px;
			}
		}
	}
	.btnBlue{
		display: flex;
		align-items: center;
		gap: 10px;
		width: fit-content;
		padding: 0 25px;
		height: 60px;
		background-color: #144EE3;
		box-shadow: 10px 9px 22px 0 #144EE361;
		cursor: pointer;
		border-radius: 48px;
		font-size: 16px;
		font-weight: 600;
		line-height: 18px;
		position: relative;
		overflow: hidden;
		span,img{z-index: 2;}
		&:before{
			transition: .2s ease-in-out;
			content: '';
			width: 100%;
			height: 0;
			position: absolute;
			left: 0;
			bottom: 0;
			background-color: #1a3885;
			z-index: 1;
		}
		&:hover:before{
			height: 60px;
		}
	}
	.listVideo{
		display: flex;
		flex-wrap: wrap;
		gap: 20px;
	}
	.fade-leave-active {
		transition: opacity .3s ease-in-out;
	}
	.fade-leave-to {
		opacity: 0;
	}
	.fadeAll-enter-active, .fadeAll-leave-active {
		transition: opacity 0.5s ease;
	}
	.fadeAll-enter-from, .fadeAll-leave-to {
		opacity: 0;
	}
	.footer{
		display: none;
	}
	.noData{
		height: 40vh;
		font-size: 40px;
		font-weight: 600;
		text-align: center;
		display: flex;
		align-items: center;
		justify-content: center;
		max-width: 700px;
		margin: auto;
	}
	@media (max-width: 1600px) {
		.footer{
			display: block;
			margin-top: 24px;
			width: fit-content;
			margin-left: auto;
		}
	}
	@media (max-width: 1300px) {
		.titleBlock{
			.contentTitle{
				flex-basis: 100%;
				.title{
					margin-bottom: 10px;
				}
			}
			.btnBlue{
				margin-top: 10px;
				margin-left: auto;
			}
		}
	}
	@media (max-width: 991px) {
		.subTitle{
			flex-wrap: wrap;
		}
		.btnBlue{
			padding: 0 16px;
			font-size: 14px;
		}
		.noData{
			font-size: 20px;
		}
	}
</style>