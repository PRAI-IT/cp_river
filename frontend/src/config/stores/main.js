import { defineStore } from 'pinia'
import axios from "axios";
export const useMain = defineStore('main', {
	state: () => ({
		url: import.meta.env.VITE_URL,
		cats:{
			'видеоигры':'1.svg',
			'авто':'2.svg',
			'аниме':'3.svg',
			'блогеры':'4.svg',
			'детям':'5.svg',
			'еда':'6.svg',
			'интервью':'7.svg',
			'культура':'8.svg',
			'лайфхаки':'9.svg',
			'музыка':'10.svg',
			'новости и СМИ':'11.svg',
			'обучение':'12.svg',
			'подкасты':'13.svg',
			'путешествия':'14.svg',
			'радио':'15.svg',
			'сериалы':'16.svg',
			'спорт':'17.svg',
			'тв онлайн и телеканалы':'18.svg',
			'телешоу':'19.svg',
			'трансляции':'20.svg',
			'фильмы':'21.svg',
			'фонды помощи':'22.svg',
			'футбол':'23.svg',
			'юмор':'24.svg',

			'телепередачи':'18.svg',
			'мультфильмы':'5.svg',
			'разное':'4.svg',
			'авто-мото':'2.svg',
		},
		listVideo:[],
		spinner:false
	}),
	actions: {
		changeReaction(id,value){
			this.listVideo.find(item=>item.id === id).reaction = value
		},
		async loadVideo(){
			this.spinner = true

			const selected = this.listVideo.filter(item=>item.reaction === 'like').map(item=>item.id)
			this.listVideo = []

			const res = await this.request('POST','video',{id:selected})
			if(res){
				for(let item of res){
					const video = await this.request('GET',`video/${item}`)
					if(video){
						const getValueByKey = (key)=>{
							try {
								if(video[key]){
									return Object.values(video[key])[0]||''
								}else return ''
							}catch (e){return ''}
						}
						this.listVideo.push({
							name:getValueByKey('title'),
							description:getValueByKey('description'),
							date:new Date(getValueByKey('v_pub_datetime')).toLocaleString(),
							watch:getValueByKey('v_year_views').toLocaleString(),
							cat:getValueByKey('category_id'),
							reaction:'',
							id:getValueByKey('video_id')
						})
					}
				}
			}
			this.spinner = false
		},
		async request(method,url,formData={}){
			try {
				const {data} = await axios({
					method,
					url: encodeURI(`${this.url}/${url}`),
					data: formData
				})
				if(data.err) return false
				return data
			} catch (error) {
				console.warn('Error', error.message);
				if(method === 'POST') alert('Произошла ошибка, попробуйте повторить позже')
				return false
			}
		}
	},
	getters: {
		getCat: (state) => {
			return (cat) => {return state.cats[cat.toLowerCase()]||'4.svg'}
		},
		getListVideo: (state)=>{
			return state.listVideo
		},
		getVideoById: (state)=>{
			return (id) => {return state.listVideo.find(item=>item.id === id)}
		}
	},
})