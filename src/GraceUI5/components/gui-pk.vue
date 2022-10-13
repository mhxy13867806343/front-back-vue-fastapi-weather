<template>
	<view class="gui-pk-wrap" 
	:style="{width:width,height:height,borderRadius:borderRadius}">
		<!-- 背景 -->
		<image 
		src="https://upload-images.jianshu.io/upload_images/15372054-ef5c77eb84052ec1.png?imageMogr2/auto-orient/strip|imageView2/2/w/750/format/webp" 
		class="gui-pk-bg" style="width:690rpx; height:460rpx;"></image>
		<!-- pk 图标 -->
		<view class="gui-pk-icon-wrap gui-flex gui-rows gui-justify-content-center gui-align-items-center" 
		:style="{width:width, height:height,borderRadius:borderRadius}">
			<view class="gui-pk-icon gui-border-box">
				<image 
				src="https://upload-images.jianshu.io/upload_images/15372054-24bbe2c57e61d1a2.png?imageMogr2/auto-orient/strip|imageView2/2/w/140/format/webp" 
				mode="widthFix" style="width:80rpx; height:80rpx;"></image>
			</view>
		</view>
		<view class="gui-pk gui-flex gui-rows gui-space-between gui-align-items-center" 
		:style="{width:width, height:height,borderRadius:borderRadius}">
			<view class="gui-pk-item gui-flex gui-columns">
				<text class="gui-pk-title gui-block-text">{{title[0]}}</text>
				<view class="gui-pk-btn-wrap" hover-class="gui-tap" v-if="status == 'button'">
					<text class="gui-pk-btn gui-block-text" 
					data-index="left" @tap="choose">{{btnName}}</text>
				</view>
				<view class="gui-pk-btn-wrap" v-if="status == 'progress'">
					<progress :percent="progress[0]" activeColor="#FFFFFF" :active="active" 
					stroke-width="3" class="gui-pk-progress" backgroundColor="#3699ff" />
				</view>
				<text class="gui-pk-text gui-block-text" v-if="status == 'progress'">{{progress[2]}}</text>
			</view>
			<view class="gui-pk-item">
				<text class="gui-pk-title gui-block-text" style="text-align:right;">{{title[1]}}</text>
				<view class="gui-pk-btn-wrap gui-flex gui-rows" hover-class="gui-tap" 
				style="justify-content:flex-end;" v-if="status == 'button'">
					<text class="gui-pk-btn gui-block-text" 
					style="color:#FF0036;" data-index="right" @tap="choose">{{btnName}}</text>
				</view>
				<view class="gui-pk-btn-wrap" style="justify-content:flex-end;" v-if="status == 'progress'">
					<progress :percent="progress[1]" stroke-width="3" class="gui-pk-progress" 
					:active="active" activeColor="#FFFFFF" backgroundColor="#FF6666"/>
				</view>
				<text class="gui-pk-text gui-block-text" style="text-align:right;" v-if="status == 'progress'">{{progress[3]}}</text>
			</view>
		</view>
	</view>
</template>
<script>
export default{
	name  : "gui-pk",
	props : {
		width        : {type:String, default:'690rpx'},
		height       : {type:String, default:'260rpx'},
		borderRadius : {type:String, default:'8rpx'},
		title        : {type:Array, default:function(){return ['',''];}},
		btnName      : {type:String, default:'站队'},
		status       : {type:String, default:'button'},
		progress     : {type:Array, default:function(){return [80,20,'8000 票', '2000 票'];}}
	},
	methods:{
		choose:function (e) {
			this.$emit('choose', e.currentTarget.dataset.index);
		}
	},
	data() {
		return {
			// #ifndef APP-NVUE
			active: true,
			// #endif
			// #ifdef APP-NVUE
			active: false
			// #endif
		}
	},
}
</script>
<style scoped>
.gui-pk-wrap{font-size:0; overflow:hidden; position:relative;}
.gui-pk-bg{position:absolute; left:0; top:0; z-index:1;}
.gui-pk{position:absolute; left:0; top:0; z-index:3;}
.gui-pk-item{width:220rpx; overflow:hidden; padding-left:35rpx; padding-right:35rpx;}
/* #ifndef APP-PLUS */
.gui-pk-item{box-sizing:border-box;}
/* #endif */
.gui-pk-title{color:#FFFFFF; font-size:50rpx; line-height:60rpx;}
.gui-pk-btn-wrap{margin-top:32rpx;}
.gui-pk-btn{width:120rpx; height:50rpx; line-height:50rpx; text-align:center; background-color:#FFFFFF; font-size:24rpx; border-radius:100rpx; color:#3687FF;}
.gui-pk-btn-hv{font-weight:bold;}
.gui-pk-progress{width:150rpx;}
.gui-pk-text{font-size:22rpx; color:#FFFFFF; line-height:50rpx; margin-top:2px;}
.gui-pk-icon-wrap{position:absolute; top:0px; left:0px; z-index:2;}
.gui-pk-icon{width:120rpx; height:120rpx; padding-top:20rpx; padding-bottom:20rpx; padding-left:20rpx; padding-right:20rpx; background-color:#FFFFFF; border-radius:100rpx; font-size:0;}
</style>