<template>
	<gui-popup ref="guipopupforareapicker" position="bottom">
		<view class="gap-body gui-bg-white" @tap.stop.prevent="stopfun">
			<view class="gap-header gui-flex gui-rows gui-space-between">
				<text class="gap-header-btn gui-block-text" :class="[cancelClass]" 
				@tap="close">{{cancelText}}</text>
				<text class="gap-header-btn gui-block-text" :class="[confirmClass]" 
				style="text-align:right;" @tap="confirm">{{confirmText}}</text>
			</view>
			<picker-view :indicator-style="indicatorStyle" 
			class="gap-main" :value="defaultVal" @change="change">
				<picker-view-column v-if="level >= 1">
					<text class="gap-item gui-block-text" v-for="(item, index) in province" 
					:key="index">{{item.label}}</text>
				</picker-view-column>
				<picker-view-column v-if="level >= 2">
					<text class="gap-item gui-block-text" v-for="(item, index) in city[defaultVal[0]]" 
					:key="index">{{item.label}}</text>
				</picker-view-column>
				<picker-view-column v-if="level >= 3">
					<text class="gap-item gui-block-text" v-for="(item, index) in area[defaultVal[0]][defaultVal[1]]" 
					:key="index">{{item.label}}</text>
				</picker-view-column>
			</picker-view>
		</view>
	</gui-popup>
</template>
<script>
import provinceData from '../data/city-data/province.js';
import cityData     from '../data/city-data/city.js';
import areaData     from '../data/city-data/area.js';
export default{
	name  : "gui-area-picker",
	props : {
		cancelText     : { type : String, default : '取消' },
		cancelClass    : { type : String, default : 'gui-color-gray' },
		confirmText    : { type : String, default : '确定' },
		confirmClass   : { type : String, default : 'gui-primary-color' },
		value          : { type : Array , default () { return ['', '', ''] }},
		level          : { type : Number, default : 3}
	},
	data() {
		return {
			indicatorStyle : 'height:35px',
			province       : provinceData,
			city           : cityData,
			area           : areaData,
			defaultVal     : [0,0,0],
			realshow       : false
		}
	},
	watch:{
		value      : function(nv, ov){this.setDefault();},
		defaultVal : function(nv, ov){
			if(ov[0] != nv[0]){
				this.defaultVal.splice(1,1,0);
				this.defaultVal.splice(2,1,0);
			}else if(ov[1] != nv[1]){
				this.defaultVal.splice(2,1,0);
			}
		}
	},
	created() {
		this.setDefault();
	},
	methods:{
		setDefault:function(){
			if(this.value[0] == ''){return ;}
			this.$nextTick(() => {
				this.defaultVal.splice(0, 1, this.arrayIndexOf(this.province, this.value[0]));
				if(this.value[1] == ''){return ;}
				this.$nextTick(() => {
					this.defaultVal.splice(1,1, this.arrayIndexOf(this.city[this.defaultVal[0]], this.value[1]));
					if(this.value[2] == ''){return ;}
					this.$nextTick(() => {
						this.defaultVal.splice(2,1, this.arrayIndexOf(this.area[this.defaultVal[0]][this.defaultVal[1]], this.value[2]));
					})
				})
			});
		},
		arrayIndexOf : function(arr, needFind){
			var index = 0;
			for(let i = 0; i < arr.length; i++){if(arr[i].label == needFind){index = i; return i;}}
			return index;
		},
		change : function (e) {
			var res = e.detail.value;
			if(!res[0]){res[0] = 0;}
			if(!res[1]){res[1] = 0;}
			if(!res[2]){res[2] = 0;}
			this.defaultVal    = res;
		},
		confirm:function () {
			var codes = [
				provinceData[this.defaultVal[0]].value,
				cityData[this.defaultVal[0]][this.defaultVal[1]].value,
				areaData[this.defaultVal[0]][this.defaultVal[1]][this.defaultVal[2]].value ? areaData[this.defaultVal[0]][this.defaultVal[1]][this.defaultVal[2]].value : 0
			];
			var names = [
				provinceData[this.defaultVal[0]].label,
				cityData[this.defaultVal[0]][this.defaultVal[1]].label,
				areaData[this.defaultVal[0]][this.defaultVal[1]][this.defaultVal[2]].label ? areaData[this.defaultVal[0]][this.defaultVal[1]][this.defaultVal[2]].label : ''
			];
			codes = codes.splice(0, this.level);
			names = names.splice(0, this.level);
			var res = {codes : codes, names : names, indexs : this.defaultVal};
			this.$emit('confirm', res);
			this.$refs.guipopupforareapicker.close();
		},
		open : function () {
			this.$refs.guipopupforareapicker.open();
		},
		close : function () {
			this.$refs.guipopupforareapicker.close();
		},
		stopfun : function(e){e.stopPropagation(); return null;}
	}
}
</script>
<style scoped>
.gap-body{height:500rpx;}
.gap-header{padding:25rpx;}
.gap-header-btn{width:200rpx; line-height:38rpx; height:38rpx; font-size:28rpx;}
.gap-main{width:750rpx; height:500rpx;}
.gap-item{height:35px; font-size:12px; line-height:35px; overflow:hidden; text-align:center;}
</style>