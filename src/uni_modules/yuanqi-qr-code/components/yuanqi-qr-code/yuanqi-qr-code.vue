<template>
	<view class="yuanqi-qrcode" :style="{height:canvasSize+'px'}">
		<image v-if="url" :src="url" mode="widthFix" class="yuanqi-image"
			:style="{width:canvasSize+'px',height:canvasSize+'px'}">
		</image>
		 <canvas  :id="canvasId" :canvas-id="canvasId" class="yuanqi-canvas":style="{width:canvasSize+'px',height:canvasSize+'px'}" />
	</view>
</template>

<script>
	import uQRCode from "./uQRCode.js"
	export default {
		props: {
			text: {
				type: String,
				default: "hello world"
			},
			size: {
				type: Number,
				default: 512
			},
			bgColor: {
				type: String,
				default: "#FFFFFF"
			},
			color: {
				type: String,
				default: "#000000"
			},
			borderSize: {
				type: Number,
				default: 38
			},
			fileType: {
				type: String,
				default: "png"
			},
			correctLevel: {
				type: [String, Number],
				default () {
					return uQRCode.CorrectLevel.H
				}
			},
			logo: String,
			bgImg: String
		},
		data() {
			return {
				url: "",
				isPainted: false,
				canvasId: 'canvasId'

			};
		},
		computed: {
			canvasSize() {
				return uni.upx2px(this.size + this.borderSize * 2)
			},
			qrCodeSize() {
				return uni.upx2px(this.size)
			},
			qrCodeBorderSize() {
				return uni.upx2px(this.borderSize)
			},
			QRCorrectLevel() {
				return typeof this.correctLevel === "string" ? uQRCode.CorrectLevel[this.correctLevel] : this.correctLevel
			}
		},
		beforeCreate(){
			this.canvasId=`yuanqi_${Math.round(Math.random()*10000).toString(16)}`;
		},
		mounted() {
			this.$nextTick(() => {
				this._ctx = uni.createCanvasContext(this.canvasId,this)
				this.make()
			})
		},
		methods: {
			save() {
				if (!this.url) {
					return uni.showToast({
						icon: "none",
						title: "未生成二维码，保存失败"
					})
				}
				// #ifndef H5
				uni.saveImageToPhotosAlbum({
					filePath: this.url,
					success(res) {
						uni.showToast({
							icon: "none",
							title: "保存成功"
						})
					},
					fail(e) {
						if (!e.errMsg.includes('cancel')) {
							uni.showToast({
								icon: "none",
								title: "保存失败请检查是否有相册使用权限"
							})
						}
					}
				});
				// #endif
				// #ifdef H5
				uni.showModal({
					title: "H5不支持保存图片到相册",
					content: "需要保存图片，请长按图片保存！",
					showCancel: false
				})
				// #endif
			},
			make() {
				const QRCode = new uQRCode(this.text, this.QRCorrectLevel);
				this.QRCodeInstance = QRCode;
				this.draw(QRCode)
			},
			async getImagePath(src){
				const [err,res]=await uni.getImageInfo({
					src
				})
				return res?res.path:src
			},
			async drawLogo(src) {
				const img=await this.getImagePath(src)
        const _ctx = this._ctx;
				const _size = this.canvasSize;
				const logoSize = this.qrCodeSize / 4;
				const logoX = _size / 2 - logoSize / 2;
				const logoY = _size / 2 - logoSize / 2;
				const logoBorderSize = logoSize + 10;
				const logoBorderX = _size / 2 - logoBorderSize / 2;
				const logoBorderY = _size / 2 - logoBorderSize / 2;
				const borderRadius = 5;
				this.fillRoundRect(_ctx, borderRadius, logoBorderX, logoBorderY, logoBorderSize, logoBorderSize)
				_ctx.drawImage(img, logoX, logoY, logoSize, logoSize)
			},
			async draw(oQRCode) {
				const _ctx = this._ctx;
				const _size = this.qrCodeSize;
				const nCount = oQRCode.getModuleCount();
				const nWidth = _size / nCount;
				const nHeight = _size / nCount;
				const nRoundedWidth = Math.round(nWidth);
				const nRoundedHeight = Math.round(nHeight);
				const _logo = this.logo;
				let color = this.color
				let bgColor = this.bgColor
				this.clear();
				if (this.bgImg) {
					const img=await this.getImagePath(this.bgImg)
					_ctx.drawImage(img, 0, 0, this.canvasSize, this.canvasSize)
					bgColor = 'rgba(255,255,255,0)'
				} else {
					_ctx.setFillStyle(bgColor)
					_ctx.fillRect(0, 0, this.size, this.size)
				}
				for (let row = 0; row < nCount; row++) {
					for (let col = 0; col < nCount; col++) {
						let bIsDark = oQRCode.isDark(row, col)
						let nLeft = col * nWidth + this.qrCodeBorderSize
						let nTop = row * nHeight + this.qrCodeBorderSize
						_ctx.setStrokeStyle(bIsDark ? color : bgColor)
						_ctx.lineWidth = 1
						_ctx.setFillStyle(bIsDark ? color : bgColor)
						_ctx.fillRect(nLeft, nTop, nWidth, nHeight)
						_ctx.strokeRect(
							Math.floor(nLeft) + 0.5,
							Math.floor(nTop) + 0.5,
							nRoundedWidth,
							nRoundedHeight
						)
						_ctx.strokeRect(
							Math.ceil(nLeft) - 0.5,
							Math.ceil(nTop) - 0.5,
							nRoundedWidth,
							nRoundedHeight
						)
					}
				}
				if (Boolean(_logo)) {
					await this.drawLogo(_logo)
				}
				_ctx.draw(false, () => {
					this.isPainted = true
					this.$emit('onPainted')
					this.makeImage()
				})
			},
			makeImage() {
				// #ifndef MP-ALIPAY
				uni.canvasToTempFilePath({
					canvasId: this.canvasId,
					fileType: this.fileType,
					width: this.canvasSize,
					height: this.canvasSize,
					destWidth: this.canvasSize,
					destHeight: this.canvasSize,
					success: res => {
						this.url = res.tempFilePath
						this.$emit('onMakeImged', {
							imgUrl: res.tempFilePath
						})
					}
				}, this);
				// #endif
				// #ifdef MP-ALIPAY
				this._ctx.toTempFilePath({
					fileType: this.fileType,
					width: this.canvasSize,
					height: this.canvasSize,
					destWidth: this.canvasSize,
					destHeight: this.canvasSize,
					success: res => {
						this.url = res.apFilePath
						this.$emit('onMakeImged', {
							imgUrl: res.apFilePath
						})
					}
				})
				// #endif
			},
			clear() {
				this._ctx.clearRect(0, 0, this.canvasSize, this.canvasSize)
				if (this.isPainted) {
					this.url = "#"
				}
				this.isPainted = false
			},
			fillRoundRect(ctx, r, x, y, w, h) {
				ctx.save()
				ctx.translate(x, y)
				ctx.beginPath()
				ctx.arc(w - r, h - r, r, 0, Math.PI / 2)
				ctx.lineTo(r, h)
				ctx.arc(r, h - r, r, Math.PI / 2, Math.PI)
				ctx.lineTo(0, r)
				ctx.arc(r, r, r, Math.PI, Math.PI * 3 / 2)
				ctx.lineTo(w - r, 0)
				ctx.arc(w - r, r, r, Math.PI * 3 / 2, Math.PI * 2)
				ctx.lineTo(w, h - r)
				ctx.closePath()
				ctx.setFillStyle(this.bgColor)
				ctx.fill()
				ctx.restore()
			},
			getModules() {
				return this.QRCodeInstance.getModules();
			}
		}
	}
</script>

<style lang="scss">
	.yuanqi-qrcode {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}

	.yuanqi-image {
		flex: 1;
	}

	.yuanqi-canvas {
		position: fixed;
		visibility: hidden;
		z-index: -111;
	}
</style>
