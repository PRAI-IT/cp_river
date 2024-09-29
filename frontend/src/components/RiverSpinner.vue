<template lang="pug">
.contentSpinner
	img(src="/img/goose.gif")
</template>

<script setup>

</script>

<style scoped lang="scss">
	.contentSpinner{
		display: flex;
		justify-content: center;
		align-items: center;
		position: fixed;
		z-index: 2000;
		height: 100vh;
		width: 100vw;
		backdrop-filter: blur(4px);
		background: #0E131E80;
		top: 0;
		left: 0;
		img{
			animation: goingGoose 2s linear;
		}
	}
	@keyframes goingGoose {
		from{
			transform: scale(.4);
		}
		to{
			transform: scale(1);
		}
	}
</style>