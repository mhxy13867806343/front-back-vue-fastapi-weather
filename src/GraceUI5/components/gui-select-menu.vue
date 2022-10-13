<template>
	<view class="gui-select-menu-wrap">
		<!-- #ifndef APP-NVUE -->
		<view class="gui-masker" 
		v-if="show"
		@tap.stop.prevent="close" 
		@touchmove.stop.prevent="stopfun" 
		:style="{zIndex:(zIndex-1)}" ></view>
		<!-- #endif -->
		<view class="gui-select-menu-title gui-flex gui-rows gui-nowrap gui-justify-content-center gui-align-items-center" 
		@click.stop="showMenu" 
		id="menuMain">
			<text class="gui-block-text gui-ellipsis" 
			:style="{
				fontSize:fontSize, 
				color:titleColor
			}">{{itemsIn[currentIndex]}}</text>
			<text :style="{fontSize:fontSize, color:iconColor}" 
			class="gui-icons gui-select-menu-title-icon gui-block-text" 
			v-if="!show">&#xe603;</text>
			<text :style="{fontSize:fontSize, color:iconColor}" 
			class="gui-icons gui-select-menu-title-icon gui-block-text" 
			v-if="show">&#xe654;</text>
		</view>
		<view class="gui-select-menu" 
		v-if="show" 
		:style="{top : top +'px', height:height, zIndex:zIndex}" 
		@tap.stop="close" 
		@touchmove.stop.prevent="stopfun">
			<scroll-view :scroll-y="true" 
			:show-scrollbar="false" 
			:style="{height:height, marginTop:'100rpx'}" 
			class="gui-select-menus gui-border-box">
				<view @tap.stop="stopfun" 
				class="gui-select-item gui-flex gui-rows gui-nowrap gui-align-items-center gui-bg-gray" 
				v-if="isInput">
					<input type="text" 
					v-model="inputVal" 
					class="gui-select-input gui-flex1 gui-border-box"
					@confirm="addTag" 
					:placeholder="placeholder" />
					<text class="gui-select-input-btn gui-block-text" 
					:style="{color:activeColor}" 
					@tap.stop="addTag">{{addBtnName}}</text>
				</view>
				<view class="gui-select-item gui-flex gui-rows gui-nowrap gui-align-items-center gui-bg-white" 
				v-for="(item, index) in itemsIn" :key="index" 
				:class="[index < getSize() ?'gui-border-b':'']" 
				:data-index="index" 
				@tap.stop="select" 
				:style="{height:itemHeight}">
					<text class="gui-selected-icon gui-icons" 
					:style="{
						color : index == currentIndex ? activeColor : color, 
						fontSize:fontSize
					}" 
					v-if="index == currentIndex">&#xe7f8;</text>
					<text :style="{
						fontSize:fontSize, 
						color : index == currentIndex ? activeColor : color
					}">{{item}}</text>
				</view>
				<view style="height:25rpx;" class="gui-bg-white"><text> </text></view>
			</scroll-view>
		</view>
	</view>
</template>
<script scoped>
export default {
	name  : "gui-select-menu",
	props : {
		items          : { type : Array,   default : function () { return [] } },
		titleColor     : { type : String,  default : "#2B2E3D" },
		color          : { type : String,  default : "#2B2E3D" },
		iconColor      : { type : String,  default : "rgba(69, 90, 100, 0.3)"},
		activeColor    : { type : String,  default : "#008AFF" },
		selectIndex    : { type : Number,  default : 0},
		isH5header     : { type : Boolean, default : true },
		fontSize       : { type : String,  default : '28rpx' },
		zIndex         : { type : Number,  default : 9999 },
		isInput        : { type : Boolean, default : false},
		placeholder    : { type : String,  default : "请输入自定义条件"},
		addBtnName     : { type : String,  default :"+ 添加"},
		height         : { type : String,  default : '600rpx'},
		itemHeight     : { type : String,  default : '88rpx'}
	},
	data() {
		return {
			currentIndex : 0,
			top          : 0,
			showRes      : [],
			inputVal     : '',
			show         : false,
			itemsIn      : []
		}
	},
	watch:{
		selectIndex : function () {
			this.currentIndex = this.selectIndex;
		},
		items : function (val) {
			this.itemsIn = val;
		}
	},
	created : function () {
		this.currentIndex = this.selectIndex;
		this.itemsIn      = this.items;
	},
	methods:{
		stopfun  : function (e) {e.stopPropagation(); return ;},
		showMenu : function () {
			uni.createSelectorQuery().in(this).select('#menuMain').fields(
				{rect: true}, (res) => {
					this.top       = res.top;
					// #ifdef H5
					if(this.isH5header){
						this.top      += 44;
					}
					// #endif
					this.show = true;
					this.$emit('showMenu');
				}
			).exec();
		},
		close : function(){
			setTimeout(()=>{this.show = false;}, 100);
			this.$emit('close');
		},
		select : function(e){
			var index = Number(e.currentTarget.dataset.index);
			this.currentIndex = index;
			this.$emit('select', index, this.items[index]);
			this.close();
		},
		addTag : function () {
			if(this.inputVal == ''){return ;}
			var newArr   = JSON.stringify(this.itemsIn);
			newArr       = JSON.parse(newArr);
			newArr.unshift(this.inputVal);
			this.itemsIn = [];
			this.itemsIn = newArr;
			 //newArr;
			this.$emit('submit', this.inputVal);
			this.inputVal = '';
			this.close();
		},
		getSize : function(){
			return (this.itemsIn.length - 1);
		},
		setCurrentIndex : function (index) {
			this.currentIndex = index;
		}
	}
}
</script>
<style scoped>
/* #ifndef APP-NVUE */
@import "@/GraceUI5/css/animate.css";
.animate{animation-duration:200ms; animation-timing-function:linear;}
/* #endif */
.gui-masker{width:750rpx; position:fixed; left:0; top:250rpx; bottom:0; flex:1; background-color:rgba(0,0,0,0.3);}
.gui-select-menu-title{height:100rpx;}
.gui-select-menu-title-icon{margin-left:5px; margin-top:3px;}
.gui-select-menu{position:fixed; width:750rpx; left:0; top:0;}
.gui-select-menus{ height:300px;}
.gui-select-item{padding:0 25rpx; height:88rpx;}
.gui-selected-icon{margin-right:15rpx;}
.gui-select-input{line-height:60rpx; height:100rpx; width:200rpx; padding:20rpx 0; font-size:26rpx; background-color:rgba(0,0,0,0);}
.gui-select-input-btn{width:120rpx; line-height:60rpx; height:60rpx; text-align:center; font-size:24rpx; border-radius:6rpx;}
</style>