<template lang="pug">
.videoBlock(:style="`background-image:url(./img/categories/${mainStore.getCat(props.video.cat)})`" :id="`elVideo-${props.video.id}`"
	:class="{'active':props.video.reaction!==''}" @click="$_river_item_video_openModal")
	.idVideo ID: {{props.video.id}}
	.title(:key="props.video.id") {{props.video.name}}
	.desc(:key="props.video.id" v-if="props.video.description") Описание:&nbsp;
		span {{props.video.description}}
	.desc(v-else :key="props.video.id")
	.date(:key="props.video.id") {{props.video.date}}
	.tagList(:key="props.video.id")
		.tag.grey {{props.video.watch}} просмотров
		.tag.blue {{props.video.cat}}
	RiverButtons(v-model="reaction" @change="mainStore.changeReaction(props.video.id,$event)")
</template>

<script setup>
	import {ref,watch} from "vue";

	const emit = defineEmits(['openModal'])
	const props = defineProps({
		video:Object
	})
	import RiverButtons from "@/components/RiverButtons.vue";

	import {useMain} from "@/config/stores/main";
	const mainStore = useMain()

	const reaction = ref(props.video.reaction)

	function $_river_item_video_openModal(){
		const bbox = document.getElementById(`elVideo-${props.video.id}`).getBoundingClientRect();
		emit('openModal',[bbox.left, bbox.top])
	}
	watch(
		() => props.video.reaction,
		(value) => reaction.value = value
	)
</script>

<style scoped lang="scss">
	.videoBlock{
		height: 322px;
		width: calc(20% - 16px);
		flex: none;
		padding: 14px;
		border-radius: 12px;
		background-color: #1F2E4DB2;
		display: flex;
		flex-direction: column;
		gap: 10px;
		position: relative;
		background-position: bottom right;
		background-repeat: no-repeat;
		transition: .3s ease-in-out;
		&.active{
			box-shadow: 0 4px 22px 0 #FF5E5E;
		}
		.idVideo{
			font-size: 12px;
		}
		.title{
			font-size: 18px;
			line-height: 18px;
			font-weight: 700;
			text-overflow: ellipsis;
			display: -webkit-box;
			-webkit-box-orient: vertical;
			-webkit-line-clamp: 2;
			overflow: hidden;
		}
		.desc{
			font-size: 18px;
			line-height: 24px;
			font-weight: 700;
			overflow: hidden;
			text-overflow: ellipsis;
			display: -webkit-box;
			-webkit-box-orient: vertical;
			-webkit-line-clamp: 3;
			span{
				font-weight: 400;
			}
		}
		.date{
			flex: auto;
			display: flex;
			align-items: flex-end;
			font-size: 18px;
			font-weight: 400;
			line-height: 22px;
		}
		.tagList{
			display: flex;
			gap: 10px;
			flex-direction: column;
			flex-wrap: wrap;
			.tag{
				padding: 3px 4px;
				font-weight: 500;
				font-size: 14px;
				line-height: 12px;
				width: fit-content;
				border-radius: 5px;
				&.grey{
					color: #1B1B1B;
					background-color: #FFFFFFCC;
				}
				&.blue{
					background-color: #144EE3;
					color: #ffffff;
				}
			}
		}
	}
	@media (max-width: 1600px) {
		.videoBlock {
			width: calc(25% - 16px);
		}
	}
	@media (max-width: 1300px) {
		.videoBlock {
			width: calc( (100% / 3) - 16px);
		}
	}
	@media (max-width: 991px) {
		.videoBlock {
			width: calc( 50% - 16px);
		}
	}
	@media (max-width: 768px) {
		.videoBlock {
			width: 100%;
		}
	}
</style>