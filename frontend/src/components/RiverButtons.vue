<template lang="pug">
.btns(:style="`--sizeBtn:${size}`")
	.btn(@click.stop="$_river_buttons_clickBtn($event,'dislike')" :class="props.modelValue?props.modelValue==='dislike'?'activeBtn':'disabledBtn':''")
		img(src="/img/icons/angryFace.gif")
		.bodyPopover Не нравится
	.btn(@click.stop="$_river_buttons_clickBtn($event,'like')" :class="props.modelValue?props.modelValue==='like'?'activeBtn':'disabledBtn':''")
		img(src="/img/icons/redHeart.gif")
		.bodyPopover Нравится
</template>

<script setup>
	const emit = defineEmits(['change','update:modelValue'])
	const props = defineProps({
		modelValue:String,
		size: {
			type:String,
			default:'50px'
		}
	})

	function $_river_buttons_createParticle(x,y,text){
		const particle = document.createElement('particle');
		document.body.appendChild(particle);

		particle.style.fontSize = '25px'
		particle.innerHTML = text

		const destinationX = x + (Math.random() - 0.5) * 2 * 75;
		const destinationY = y + (Math.random() - 0.5) * 2 * 75;

		const animation = particle.animate([
			{
				transform: `translate(-50%, -50%) translate(${x}px, ${y}px)`,
				opacity: 1
			},
			{
				transform: `translate(${destinationX}px, ${destinationY}px)`,
				opacity: 0
			}
		], {
			duration: Math.random() * 1000 + 500,
			easing: 'cubic-bezier(0, .9, .57, 1)',
			delay: Math.random() * 200
		});
		animation.onfinish = () => {particle.remove()};
	}
	function $_river_buttons_clickBtn(e,type){
		let value = type
		if(props.modelValue === type) value = ''
		emit('update:modelValue',value)
		emit('change',value)
		if(value){
			const text = type==='dislike'?'💩':'❤'
			for (let i = 0; i < 30; i++) {
				$_river_buttons_createParticle(e.clientX, e.clientY ,text);
			}
		}
	}
</script>

<style scoped lang="scss">
	.btns{
		display: inline-flex;
		width: fit-content;
		margin-left: auto;
		gap: 10px;
		.btn{
			position: relative;
			user-select: none;
			height: var(--sizeBtn);
			width: var(--sizeBtn);
			display: flex;
			justify-content: center;
			align-items: center;
			cursor: pointer;
			background-color: #FFFFFF;
			border-radius: 90px;
			transition: .3s ease-in-out;
			img{height: 70%;}
			&.activeBtn{}
			&.disabledBtn{opacity: .3;}
		}
		.btn:hover .bodyPopover, .bodyPopover:hover{
			opacity: 1;
			visibility: visible;
			transition-delay: 1s;
			transform: translate(0, -5px);
		}
		.bodyPopover{
			display: flex;
			flex-direction: column;
			column-gap: 4px;
			z-index: 100;
			font-size: 12px;
			opacity: 0;
			visibility: hidden;
			transition: all 0.5s cubic-bezier(0.75, -0.02, 0.2, 0.97);
			padding: 8px;
			background-color: #0b101b;
			border-radius: 4px;
			position: absolute;
			bottom: var(--sizeBtn);
			width: 100px;
			text-align: center;
			color: white;
			right: calc((var(--sizeBtn) / 2) - 25px);
		}
		.bodyPopover::after {
			content: '';
			position: absolute;
			right: 14px; bottom: -20px;
			border: 10px solid transparent;
			border-top: 10px solid #0b101b;
		}
	}
</style>