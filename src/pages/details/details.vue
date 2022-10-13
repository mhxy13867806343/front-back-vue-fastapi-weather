
<template>
	<view class="cu-bar bg-white">
		<view class="cuIcon-title text-red u-font-26 u-text-center u-padding-35 ">当前所在地区:
			{{forecastsCom&&forecastsCom.province}}-
			{{forecastsCom&&forecastsCom.city}}</view>
		<view class="cuIcon-title text-red u-font-26 u-text-center u-padding-35 ">当前所在地区code:{{forecastsCom&&forecastsCom.adcode}}</view>
		<view class="cuIcon-title text-red u-font-26 u-text-center u-padding-35 ">更新时间:{{forecastsCom&&forecastsCom.reporttime}}</view>
		<scroll-view class="scroll-view_H" scroll-x="true" @scroll="scroll" scroll-left="120"
		v-if="forecastsCom&&forecastsCom.casts&&forecastsCom.casts.length">
			<view  class="scroll-view-item_H uni-bg-red"
						 v-for="(a,b) in forecastsCom&&forecastsCom.casts" :key="b">
				<text>当前时间:{{a.date}},星期{{a.week}}</text>
				<view>白天天气1:{{a.dayweather}}</view>
				<view>白天天气2:{{a.nightweather}}</view>
				<view>{{a.daywind}}:{{a.daytemp}}:{{a.daypower}}</view>
				<view>{{a.nightwind}}:{{a.nighttemp}}:{{a.nightpower}}</view>
			</view>
		</scroll-view>
	</view>
</template>
<script>
import {onLoad} from 'uni-composition-api'
import { ref,computed,set } from '@vue/composition-api'
import {getWeatherDetails,gdWeatherCode}from '@/api/weather'
export default {
	setup(){
		console.log('onLoad')
		const details=ref({})
		onLoad(opt=>{
			getWeatherDetails(opt.name).then(res=>{
				details.value=res.data
				gdWeatherCode(details.value.adcode).then(res=>{
				const {status,info,forecasts}=res.data
				if(status==='1'&&info==='OK'){
					set(details.value,'forecasts',forecasts)
				}
				})
			})
		})
		const forecastsCom=computed(()=>{
			return details.value.forecasts?.[0]
		})
		return {
			details,
			forecastsCom
		}
	}
}
</script>


<style scoped>
.cuIcon-title{
	font-weight: bold;
	font-size:50rpx;
}
</style>
