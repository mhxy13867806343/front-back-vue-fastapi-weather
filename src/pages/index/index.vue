<template>
  <view class="">
		<view class="u-rela">
			<u-search @search="onSearch" height="88" placeholder="请输入地区进行查询所搜索的地区天气情况" v-model="search"></u-search>
			<view class="u-abso search-data" v-if="searchList.length">
				<view v-for="(a,b) in searchList" :key="b" class="datas" @click="onClickItem(a)">
					{{a.name}}
					<u-line color="red" />
				</view>
			</view>
		</view>
		<u-line color="red" />
		<view>
			<view class="u-margin-left-26">热门天气地区</view>
			<view class="ul u-flex">
				<view class="ul-item" v-for="(item,index) in  weatherList" :key="index"
				@click="onClickItem(item)"

				>
					{{item.name}}
				</view>
			</view>
		</view>
	</view>
</template>

<script>
import { ref } from '@vue/composition-api'
import {onLoad} from 'uni-composition-api'
import {getWeatherList,getWeather} from '@/api/weather'
export default {
	setup(){
		const search = ref('')//搜索框的值
		const weatherList = ref([])//热门天气地区
		const searchList = ref([])//搜索框的值
		onLoad(async ()=> {
			getWeatherList({}).then(res=>{
				weatherList.value = res.data
				console.log(weatherList.value)
			})
		})
		const onClickItem=item=>{
			uni.navigateTo({
				url:`/pages/details/details?name=${item.name}`
			})
		}
		const onSearch=name=>{
			getWeather(name).then(res=>{
				console.log(res.data)
				searchList.value=res.data
			})
		}
		return {
			search,
			searchList,
			weatherList,
			onClickItem,
			onSearch
		}
	}
}
</script>

<style lang="scss">
.ul{
	display: flex;
	flex-wrap: wrap;
	flex-direction: row;
	align-items: center;
	.ul-item{
		font-size:50rpx;
		padding: 20rpx;
	}
}
.search-data{
	width: 100%;
	z-index: 100;
	background-color: #fff;
	padding: 40rpx;
	text-align: center;
	.datas{
		padding: 20rpx;
	}
}
</style>
