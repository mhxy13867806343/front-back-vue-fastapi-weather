

## 二维码组件
> **组件名：yuanqi-qr-code **


组合框组件。

### 平台兼容性说明

**暂不支持nvue**

### 安装方式

本组件符合[easycom](https://uniapp.dcloud.io/collocation/pages?id=easycom)规范，`HBuilderX 2.5.5`起，只需将本组件导入项目，在页面`template`中即可直接使用，无需在页面中`import`和注册`components`。

### 基本用法

在 ``template`` 中使用组件
```html
<yuanqi-qr-code 
	ref="yuanqiQRCode"
	:text="text"
	:color="color"
	:bgColor="bgColor" 
	:logo="logo"
	:bgImg="bgImg" 
	:size="size" 
	:borderSize="borderSize" 
	:fileType="fileType"
	:correctLevel="correctLevel" 
	@onPainted='onPainted'
	@onMakeImged='onMakeImged'></yuanqi-qr-code>
```

## API

### yuanqi-qr-code Props

|属性名		|类型			|默认值		|说明								|
|:-:		|:-:			|:-:		|:-:								|
|text		|String			|-			|二维码内容							|
|color		|String			|#000000	|前景颜色(任意有效果颜色格式,rgb、rgba)|
|bgColor	|String			|#FFFFFF	|背景颜色(任意有效果颜色格式,rgb、rgba)，透明背景设置为:transparent或rgba(0,0,0,0)|
|logo		|String			|-			|中间logo图片（支持网络图片,小程序下需先配置download域名白名单才能生效。）|
|bgImg		|String			|-			|背景图片(设置了背景图片，背景颜色属性会自动更换成透明，支持网络图片,小程序下需先配置download域名白名单才能生效。)	|
|size		|Number			|256		|二维码大小(单位:rpx)					|
|borderSize	|Number			|38			|二维码边框大小(单位:rpx)				|
|fileType	|String			|png		|图片输出格式							|
|correctLevel|Number/String	|H			|纠错等级，包含 `L`、`M`、`Q`、`H` 四个级别，`L`: 最大 7% 的错误能够被纠正；`M`: 最大 15% 的错误能够被纠正；`Q`: 最大 25% 的错误能够被纠正；`H`: 最大 30% 的错误能够被纠正。`L`与数值`1`相同,`M`与数值`0`相同,`Q`与数值`3`相同,`H`与数值`2`相同,			|

### yuanqi-qr-code Events

|事件称名	|说明					|返回值	|
|:-:		|:-:					|:-:	|
|@onPainted	|二维码绘制完成事件		|-		|
|@onMakeImged|生成图片完成事件		|图片临时路径		|





## 组件示例

```html
<template>
	<view class="yuanqi-qrcode">
		<yuanqi-qr-code ref="yuanqiQRCode" :fileType="fileType" :correctLevel="correctLevel" :logo="logo" :size="size"
		@onPainted='onPainted' @onMakeImged='onMakeImged' :borderSize="borderSize" :bgImg="bgImg" :color="color" :bgColor="bgColor" :text="text"></yuanqi-qr-code>
		<view class="controller">
			<view class="title">
				<text>参数</text>
			</view>
			<view class="row">
				<text>内容：</text>
				<view class="row-right">
					<input type="text" v-model="text" placeholder="内容" />
				</view>
			</view>
			<view class="row">
				<text>Logo：</text>
				<view class="row-right">
					<input type="text" v-model="logo" placeholder="logo Url" />
				</view>
				<button type="warn" size="mini" @click="chooseLogo">选择LOGO</button>
			</view>
			<view class="row">
				<text>背景图片：</text>
				<view class="row-right">
					<input type="text" v-model="bgImg" placeholder="bgImg Url" />
				</view>
				<button type="primary" size="mini" @click="chooseBgImg">选择背景图片</button>
			</view>
			<view class="row">
				<view class="row">
					<text>前景颜色：</text>
					<view class="row-right">
						<input type="text" v-model="color" placeholder="前景颜色" />
					</view>
				</view>
				<view class="row">
					<text>背景颜色：</text>
					<view class="row-right">
						<input type="text" v-model="bgColor" placeholder="背景颜色" />
					</view>
				</view>
			</view>
			<view class="row">
				<text>容错等级：</text>
				<view class="row-right">
					<picker mode="selector" :value="correctLevel" :range="correctLevelList"
						@change="correctLevelChange">
						<view>{{correctLevel}}</view>
					</picker>
				</view>

			</view>
			<view class="row">
				<text>输出图片格式：</text>
				<view class="row-right">
					<picker mode="selector" :value="fileTypeList.indexOf(fileType)" :range="fileTypeList"
						@change="fileTypeChange">
						<view>{{fileTypeList[fileTypeList.indexOf(fileType)]}}</view>
					</picker>
				</view>
			</view>
			<view class="row">
				<text>二维码大小：</text>
				<view class="row-right">
					<slider max="680" :value="size" :show-value="true" @change="sizeChange" />
				</view>

			</view>
			<view class="row">
				<text>边框大小：</text>
				<view class="row-right">
					<slider max="60" :show-value="true" :value="borderSize" @change="borderSizeChange" />
				</view>
			</view>
		</view>
		<button type="default" @click="make">生成</button>
		<button type="default" @click="save">保存到相册</button>
		<button type="default" @click="clear">清除</button>
		<button type="default" @click="test">生成多个二维码演示</button>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				text: "https://uniapp.dcloud.net.cn",
				size: 256,
				logo: "https://bjetxgzv.cdn.bspapp.com/VKCEYUGU-dc-site/9a952c80-6080-11eb-a16f-5b3e54966275.png",
				bgColor: "#FFFFFF",
				color: "#000000",
				correctLevel: "H",
				correctLevelListIndex:3,
				borderSize: 90,
				bgImg: "https://img0.baidu.com/it/u=2999772846,389396931&fm=26&fmt=auto",
				fileType: "png",
				fileTypeList: ['png', 'jpg'],
				correctLevelList: ["L(7%)", "M(15%)", "Q(25%)", "H(30%)"]
			};
		},
		methods: {
			test(){
				uni.navigateTo({
					url:'/pages/mulit/mulit'
				})
			},
			save() {
				this.$refs.yuanqiQRCode.save()
			},
			make() {
				this.$refs.yuanqiQRCode.make()
			},
			clear() {
				this.$refs.yuanqiQRCode.clear()
			},
			correctLevelChange(e) {
				const index=e.detail.value
				this.correctLevel = this.correctLevelList[index].charAt(0)
				this.correctLevelListIndex=index
			},
			fileTypeChange(e) {
				this.fileType = this.fileTypeList[e.detail.value]
			},
			sizeChange(e) {
				this.size = e.detail.value
			},
			borderSizeChange(e) {
				this.borderSize = e.detail.value
			},
			chooseLogo() {
				uni.chooseImage({
					count: 1,
					success: (res) => {
						this.logo = res.tempFilePaths[0]
					}
				})
			},
			chooseBgImg() {
				uni.chooseImage({
					count: 1,
					success: (res) => {
						this.bgImg = res.tempFilePaths[0]
					}
				})
			},
			onPainted(){
				
			},
			onMakeImged(e){
				
			}
		}
	}
</script>

<style lang="scss">
	.title {
		text-align: center;
		background-color: #333;
		color: #fff;
		font-size: 18px;
		padding: 5px;
		margin-top: 5px;
	}

	.row {
		display: flex;
		flex-direction: row;
		margin: 5px;
		border-bottom: 1px solid #999;
		&-right {
			flex: 1;
			padding: 0 5px;
			margin: 0 10px;
		}
	}
</style>


```
只测试了google、firefox、微信浏览器、手机浏览器、微信小程序、安卓APP，目前没有发现问题
如果发现问题或有好的建议和不明白的地方可以加QQ交流一下，联系方式：QQ:85308607。