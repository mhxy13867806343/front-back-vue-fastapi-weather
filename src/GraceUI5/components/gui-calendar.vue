<template>
<gui-popup 
	ref="guipopupforcalendar" 
	position="bottom" 
	:canCloseByShade="false" 
	:zIndex="zIndex">
	<view class="gui-calendar gui-bg-white gui-box-shadow" 
	@tap.stop.prevent="stopfun">
		<!-- 顶部日期及切换 -->
		<view class="gui-calendar-header gui-flex gui-rows gui-nowrap gui-justify-content-center gui-align-items-center">
			<text class="gui-calendar-header-btn gui-icons" 
			@click="prevYear">&#xe600;&#xe600;</text>
			<text class="gui-calendar-header-btn gui-icons" 
			@click="prevMonth">&#xe600;</text>
			<text class="gui-calendar-header-btn gui-icons" 
			style="margin:20rpx;">{{cYear}} 年 {{cMonth}} 月</text>
			<text class="gui-calendar-header-btn gui-icons" 
			@click="nextMonth">&#xe601;</text>
			<text class="gui-calendar-header-btn gui-icons" 
			@click="nextYear">&#xe601;&#xe601;</text>
		</view>
		<!-- 星期 -->
		<view class="gui-flex gui-rows gui-nowrap gui-justify-content-center gui-align-items-center">
			<text class="gui-calendar-weeks gui-block-text" v-for="(item, index) in weeks" :key="index">{{item}}</text>
		</view>
		<!-- 日历列表 -->
		<view class="gui-bg-gray gui-flex gui-rows gui-wrap gui-calendar-days">
			<view class="gui-calendar-ditems gui-flex gui-columns gui-justify-content-center gui-align-items-center"
			:style="{
				backgroundColor: currentDayIn == cYear+'-'+cMonthStr+'-'+ item.date ? activeBgColor : bgColor, 
			borderRadius:borderRadius}" 
			@click="chooseDate(cYear+'-'+cMonthStr+'-'+item.date, item.date)" 
			v-for="(item, index) in days" :key="index">
				<text class="gui-date-day" 
				:style="{color : currentDayIn == (cYear+'-'+cMonthStr+'-'+item.date) ? '#FFFFFF' : 'rgba(69, 90, 100, 0.6)'}">{{item.date}}</text>
				<text class="gui-date-nl" v-if="isLunar" 
				:style="{color : currentDayIn == (cYear+'-'+cMonthStr+'-'+item.date) ? '#FFFFFF' : 'rgba(69, 90, 100, 0.6)'}">{{item.nl}}</text>
			</view>
		</view>
		<!-- 时间选择 -->
		<view 
		class="gui-flex gui-rows gui-justify-content-center gui-align-items-center gui-bg-gray " 
		v-if="isTime">
			<picker mode="time" @change="timechange" :value="currentTimeIn">
				<text 
				class="gui-date-time gui-border-b gui-border-t gui-block-text" 
				style="border-color:#D1D1D1;" >时间 : {{currentTimeIn}}</text>
			</picker>
		</view>
		<!-- 按钮 -->
		<view class="gui-flex gui-rows gui-space-between gui-align-items-center">
			<view class="gui-date-btns-text" hover-class="gui-tap" @tap="close">
				<text class="gui-date-btns-text gui-block-text gui-color-gray">取消</text>
			</view>
			<view class="gui-date-btns-text" hover-class="gui-tap" @tap="submit">
				<text class="gui-date-btns-text gui-block-text gui-primary-color">确认</text>
			</view>
		</view>
	</view>
</gui-popup>
</template>
<script>
import guiCalendar from './gui-calendar.js';
export default {
	name  : "gui-calendar", 
	props : {
		currentDate   : { type : String,  default : "" },
		isTime        : { type : Boolean, default : true },
		bgColor       : {type  : String,  default : "#F7F8FA"},
		activeBgColor : {type  : String,  default : "#008AFF"},
		borderRadius  : {type  : String,  default : "6rpx"},
		isLunar       : {type  : Boolean, default : true },
		zIndex        : {type  : Number,  default : 2}
	},
	data(){
		return {
			weeks         : ['一', '二', '三', '四', '五', '六', '日'],
			cYear         : 2016,
			cMonth        : 6,
			cMonthStr     : "06",
			cDay          : "01",
			days          : '',
			currentDayIn  : '',
			currentTimeIn : ''
		}
	},
	created:function(){
		this.initTime();
	},
	watch:{
		currentDate  : function(){this.initTime();},
	},
	methods: {
		stopfun:function(e){e.stopPropagation(); return ;},
		timechange : function(e){
			this.currentTimeIn = e.detail.value;
		},
		getDaysInOneMonth : function (){
			var d = new Date(this.cYear, this.cMonth, 0);
			return d.getDate();
		},
		getDay : function (){
			var d = new Date(this.cYear, this.cMonth - 1, 0);
			return d.getDay();
		},
		prevYear : function(){
			this.cYear = this.cYear - 1;
			this.changeMonth();
		},
		prevMonth : function(){
			this.cMonth =  this.cMonth - 1;
			if (this.cMonth < 1) { this.cMonth = 12; this.cYear = this.cYear - 1; }
			this.cMonthStr = this.cMonth < 10 ? '0' + this.cMonth : this.cMonth;
			this.changeMonth();
		},
		nextMonth : function(){
			this.cMonth = this.cMonth + 1;
			if (this.cMonth > 12){this.cMonth = 1; this.cYear = this.cYear + 1;}
			this.cMonthStr = this.cMonth < 10 ? '0' + this.cMonth : this.cMonth;
			this.changeMonth();
		},
		nextYear : function(){
			this.cYear = this.cYear + 1;
			this.changeMonth();
		},
		changeMonth:function(){
			var daysList  = [];
			var days      = this.getDaysInOneMonth();
			var startWeek = this.getDay();
			var forSteps  = 0;
			for (var i = (0 - startWeek); i < days; i++){
				if(i >= 0){
					daysList[forSteps] = {date : i >= 9 ? i + 1 : '0' + (i+1), nl : ''};
					daysList[forSteps].nl = guiCalendar.getLunarInfo(this.cYear, this.cMonth, i + 1);
				}else{
					daysList[forSteps] = '';
				}
				forSteps++;
			}
			this.days    = daysList;
		},
		chooseDate: function (sedDate, isday) {
			if(!isday){return ;}
			this.currentDayIn = sedDate;
			if(this.isTime){return ;}
			this.$emit('changeDate', sedDate);
		},
		submit : function(){
			if(this.isTime){
				this.$emit('changeDate', this.currentDayIn + ' ' + this.currentTimeIn);
				this.$emit('confirm'   , this.currentDayIn + ' ' + this.currentTimeIn);
			}else{
				this.$emit('changeDate', this.currentDayIn);
				this.$emit('confirm'   , this.currentDayIn);
			}
			this.close();
		},
		//初始化时间
		initTime : function(){
			if(this.currentDate == ''){
				var dateObj        = new Date();
				this.cYear         = dateObj.getFullYear();
				this.cMonth        = dateObj.getMonth() + 1;
				this.cMonthStr     = this.cMonth < 10 ? '0' + this.cMonth : this.cMonth;
				this.cDay          = dateObj.getDate();
				this.cDay          = this.cDay < 10 ? '0' + this.cDay : this.cDay;
				this.currentDayIn  = this.cYear + '-' + this.cMonthStr + '-' + this.cDay;
				this.currentTimeIn = '00:00';
				this.changeMonth();
			}else{
				var dates          = this.currentDate.split(' ');
				if (!dates[1]) { dates[1] = '';}
				var dayArr         = dates[0].split('-');
				this.cYear         = Number(dayArr[0]);
				this.cMonth        = dayArr[1];
				this.cDay          = dayArr[2];
				var reg            = new RegExp('^0[0-9]+$');
				if(reg.test(this.cMonth)){this.cMonth = this.cMonth.substr(1,1);}
				this.cMonth        = Number(this.cMonth);
				this.cMonthStr     = this.cMonth < 10 ? '0'+this.cMonth : this.cMonth;
				this.currentDayIn  = dates[0];
				this.currentTimeIn = dates[1];
				this.changeMonth();
			}
		},
		open:function(){this.$refs.guipopupforcalendar.open();},
		close:function(){this.$refs.guipopupforcalendar.close();}
	}
}
</script>
<style scoped>
.gui-calendar{border-top-left-radius:10rpx; border-top-right-radius:10rpx; padding:10rpx 0;}
.gui-calendar-header{height:80rpx;}
.gui-calendar-header-btn{font-size:32rpx; padding:0 10rpx; color:rgba(69, 90, 100, 0.6);}
.gui-calendar-weeks{width:100rpx; color:#2B2E3D; height:80rpx; text-align:center; font-size:30rpx; line-height:80rpx;}
.gui-calendar-days{padding:25rpx;}
.gui-calendar-ditems{width:96rpx; height:96rpx; margin:2rpx;}

.gui-date-day{height:38rpx; line-height:38rpx; text-align:center; font-size:32rpx;}
.gui-date-nl{height:26rpx; line-height:26rpx; font-size:20rpx; text-align:center;}
.gui-date-btns-text{line-height:100rpx; font-size:28rpx; text-align:center; width:300rpx;}
.gui-date-time{font-size:28rpx; line-height:80rpx; height:80rpx; margin-bottom:30rpx;}
</style>