<template lang="pug">
.modal(:style="`--startLeft:${coords[0]}px;--startTop:${coords[1]}px`")
	.backDrop
	.contentModal(:class="{'active':video.reaction!==''}"
		:style="`background-image:url(./img/categories/${mainStore.getCat(video.cat)})`")
		.head Подробнее
			img(src="/img/icons/close.svg"
				@click="emit('close')")
		.idVideo ID: {{video.id}}
		.title.customScroll {{video.name}}
		.date {{video.date}}
		.tag.grey {{video.watch}} просмотров
		.tag.blue {{video.cat}}
		.description.customScroll(v-if="video.description") Описание:&nbsp;
			span {{video.description}}
		.description(v-else)
		.btnBlock
			RiverButtons(v-model="activeBtn" size="80px" @change="mainStore.changeReaction(video.id,$event)")
</template>

<script setup>
import {onBeforeUnmount, onMounted, ref} from "vue";

	import RiverButtons from "@/components/RiverButtons.vue";
	import {useMain} from "@/config/stores/main";

	const mainStore = useMain()

	const emit = defineEmits(['close'])
	const props = defineProps({
		coords:Array,
		id:{
			type:[Number,String],
			default:''
		}
	})
	const video = mainStore.getVideoById(props.id)
	const activeBtn = ref(video.reaction)


	onMounted(()=>{
		switch (true){
			case window.innerWidth<=576:
				document.body.style='overflow:hidden'
				break
			case window.innerWidth<=1600:
				document.body.style='overflow:hidden;padding-right:55px'
				break
		}
	})
	onBeforeUnmount(()=>{document.body.style=''})
</script>

<style scoped lang="scss">
	.modal {
		position: absolute;
		z-index: 1000;
		.contentModal{
			z-index: 2;
			position: fixed;
			padding: 40px 30px 30px 30px;
			width: 700px;
			height: 70vh;
			border-radius: 20px;
			transform: scale(1), translate(0, calc(50% - 350px));
			top: calc(50% - (70vh / 2));
			left: calc(50% - 350px);
			transition: .3s ease-in-out;
			animation: showingModal .3s ease-in-out;
			background-color: #18233B;
			background-position: bottom right;
			background-repeat: no-repeat;
			background-size: 80%;
			&.active{box-shadow: 0 4px 22px 0 #FF5E5E;}
			.head{
				display: flex;
				justify-content: space-between;
				align-items: center;
				margin-bottom: 30px;
				font-size: 20px;
				font-weight: 700;
				line-height: 30px;
				img{
					transition: .2s ease-in-out;
					cursor: pointer;
					&:hover{
						opacity: .5;
					}
				}
			}
			.idVideo{
				font-size: 12px;
				margin-bottom: 5px;
			}
			.title{
				font-size: 24px;
				font-weight: 700;
				line-height: 30px;
				margin-bottom: 10px;
				max-height: 60px;
			}
			.date{
				margin-bottom: 12px;
				font-size: 18px;
				font-weight: 400;
				line-height: 22px;
			}
			.tag{
				padding: 7px 12px;
				font-weight: 500;
				font-size: 16px;
				line-height: 12px;
				width: fit-content;
				margin-bottom: 12px;
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
			.description{
				font-size: 20px;
				line-height: 27px;
				font-weight: 700;
				height: 230px;
				overflow-y: auto;
				span{
					font-weight: 500;
				}
			}
			.btnBlock{
				margin-top: 30px;
				margin-left: auto;
				width: fit-content;
			}
		}
		.backDrop{
			position: fixed;
			height: 100vh;
			width: 100vw;
			background: #0E131E80;
			z-index: 1;
			top: 0;
			left: 0;
			backdrop-filter: blur(4px);
			animation: showingBackdrop .3s ease-in-out;
		}
	}
	@keyframes showingModal {
		from{
			transform: scale(.1);
			left: var(--startLeft);
			top: var(--startTop);
			opacity: 0;
		}
		to{
			transform: scale(1), translate(0, calc(50% - 350px));
			top: calc(50% - (70vh / 2));
			left: calc(50% - 350px);
			opacity: 1;
		}
	}
	@keyframes showingBackdrop {
		from{
			opacity: 0;
			backdrop-filter: blur(0);
		}
		to{
			opacity: 1;
			backdrop-filter: blur(4px);
		}
	}
	@media (max-width: 768px) {
		.modal {
			.contentModal{
				padding: 10px;
				width: calc(100vw - 30px);
				height: calc(100vh - 50px);

				background-position: 30% bottom;
				background-size: contain;

				transform: scale(1), translate(0, calc(50% - ((100vw - 30px) / 2)));
				top: calc(50% - ((100vh - 50px) / 2));
				left: calc(50% - ((100vw - 30px) / 2));

				.title,.date{
					font-size: 16px;
					line-height: 20px;
					max-height: 100px;
				}
				.description{
					height: 50vh;
					font-size: 14px;
					line-height: 20px;
				}
			}
		}
		@keyframes showingModal {
			from{
				transform: scale(.1);
				left: var(--startLeft);
				top: var(--startTop);
				opacity: 0;
			}
			to{
				transform: scale(1), translate(0, calc(50% - ((100vw - 30px) / 2)));
				top: calc(50% - ((100vh - 50px) / 2));
				left: calc(50% - ((100vw - 30px) / 2));
				opacity: 1;
			}
		}
	}
</style>