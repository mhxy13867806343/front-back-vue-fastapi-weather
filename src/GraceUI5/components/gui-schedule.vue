<template>
	<view class="gui-schedule-wrap">
		<view class="gui-flex gui-rows gui-space-between gui-align-items-center">
			<picker  mode="date" 
			:value="currentDayIn" 
			:start="startDate" 
			:end="endDate" 
			@change="selectDate">
				<text 
				class="gui-schedule-header-date gui-icons">{{cYear}} 年 {{cMonthStr}} 月 &#xe603;</text>
			</picker>
			<text class="gui-border gui-schedule-today" @tap="gotoToday">返回今天</text>
		</view>
		<view class="gui-flex gui-rows gui-nowrap">
			<text class="gui-schedule-weeks gui-color-gray gui-block-text" 
			v-for="(item, index) in weeks" :key="index">{{item}}</text>
		</view>
		<view class="gui-flex gui-rows gui-wrap">
			<view class="gui-schedule-7item gui-flex gui-rows gui-justify-content-center"
			v-for="(item, index) in days" :key="index">
				<view 
				class="gui-date-ditems gui-flex gui-columns gui-justify-content-center" 
				v-if="item != ''" 
				:style="{
					backgroundColor:currentDayIn == cYear+'-'+cMonthStr+'-'+ item.date 
					? activeBgColor : bgColor
				}" 
				@click="chooseDate(cYear+'-'+cMonthStr+'-'+item.date, item.date)">
					<text class="gui-date-day gui-block-text" 
					:class="[currentDayIn == (cYear+'-'+cMonthStr+'-'+item.date) ? 
					'gui-d-current-txt' : '']">{{item.date}}</text>
					<text class="gui-date-nl gui-block-text" v-if="isLunar" 
					:class="[currentDayIn == (cYear+'-'+cMonthStr+'-'+item.date) ? 
					'gui-d-current-txt' : '']">{{item.nl}}</text>
					<view class="gui-schedule-point" 
					v-if="item.haveSe" 
					:style="{backgroundColor:pointColor}"></view>
				</view>
				<view class="gui-date-ditems" v-else style="background-color:none;"></view>
			</view>
		</view>
		<view class="gui-border-b gui-schedule-line"></view>
		<view class="gui-schedule-time-list-wrap">
			<view class="gui-schedule-time-list gui-flex gui-rows gui-nowrap"
			v-for="(item, index) in hours" :key="index">
				<text class="gui-schedule-timer gui-block-text gui-color-gray">{{item}}:00</text>
				<view class="gui-border-b gui-schedule-body gui-flex gui-columns">
					<text class="gui-schedules gui-block-text" 
					v-for="(schedule, idx) in schedulesIn[index]" :key="idx" 
					@tap="scheduleTap" :data-id="schedule.id" 
					:style="{
						backgroundColor:schedule.bgColor, 
						color:schedule.color}">{{schedule.content}}</text>
				</view>
			</view>
		</view>
	</view>
</template>
<script>
import guiCalendar from './gui-calendar.js';
export default{
	name : "gui-schedule",
	data() {
		return {
			cYear      : 2020,
			cMonth     : 1,
			cDay       : 10,
			cMonthStr  : '01',
			weeks      : ['一', '二', '三', '四', '五', '六', '日'],
			days       : [],
			currentDayIn : '',
			hours      : ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'],
			schedulesIn: [] 
		}
	},
	props:{
		// 当前默认日期
		currentDate   : {type:String, default:""},
		bgColor       : {type:String, default:"#F8F8F8"},
		activeBgColor : {type:String, default:"#008AFF"},
		isLunar       : {type:Boolean, default:true },
		startDate     : {type:String, default:'1950-01-01'},
		endDate       : {type:String, default:'2050-01-01'},
		schedules     : {type:Array, default:function () {return []}},
		pointColor    : {type:String, default:"#FF0036"}
	},
	created:function(){
		this.currentDayIn = this.currentDate;
		this.initTime();
		this.getSchedulesIn();
	},
	methods:{
		initTime : function(){
			if(this.currentDayIn == ''){
				var dateObj        = new Date();
				this.cYear         = Number(dateObj.getFullYear());
				this.cMonth        = Number(dateObj.getMonth() + 1);
				this.cMonthStr     = this.cMonth < 10 ? '0' + this.cMonth : this.cMonth;
				this.cDay          = dateObj.getDate();
				this.cDay          = this.cDay < 10 ? '0' + this.cDay : this.cDay;
				this.currentDayIn  = this.cYear + '-' + this.cMonthStr + '-' + this.cDay;
				this.changeMonth();
			}else{
				var dates          = this.currentDayIn.split(' ');
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
		changeMonth:function(){
			var daysList  = [];
			var days      = this.getDaysInOneMonth();
			var startWeek = this.getDay();
			var forSteps  = 0;
			for (var i = (0 - startWeek); i < days; i++){
				if(i >= 0){
					daysList[forSteps] = {date : i >= 9 ? i + 1 : '0' + (i+1), nl : ''};
					daysList[forSteps].nl = guiCalendar.getLunarInfo(this.cYear, this.cMonth, i + 1);
					daysList[forSteps].haveSe = this.haveSchedule(daysList[forSteps].date);
				}else{
					daysList[forSteps] = '';
				}
				forSteps++;
			}
			this.days    = daysList;
		},
		haveSchedule : function (day) {
			var cDay = this.cYear+'-'+this.cMonthStr+'-'+day;
			for(let i = 0; i < this.schedules.length; i++){
				if(this.schedules[i].datetime.indexOf(cDay) != -1){
					return true;
				}
			}
			return false;
		},
		getDaysInOneMonth : function (){
			var d = new Date(this.cYear, this.cMonth, 0);
			return d.getDate();
		},
		getDay : function (){
			var d = new Date(this.cYear, this.cMonth - 1, 0);
			return d.getDay();
		},
		selectDate : function(e){
			this.currentDayIn = e.detail.value;
			this.initTime();
			this.getSchedulesIn();
			this.$emit('selectDate', e.detail.value);
		},
		chooseDate: function (sedDate) {
			this.currentDayIn = sedDate;
			this.getSchedulesIn();
			this.$emit('chooseDate', sedDate);
		},
		getSchedulesIn : function (){
			var res = [];
			for(let i = 0; i < this.hours.length; i++){
				var ctime = this.currentDayIn + ' ' + this.hours[i] + ':00';
				res.push([]);
				for(let ii = 0; ii < this.schedules.length; ii++){
					if(this.schedules[ii].datetime == ctime){
						res[i].push(this.schedules[ii]);
					}
				}
			}
			this.schedulesIn = res;
		},
		scheduleTap : function (e) {
			var id = e.currentTarget.dataset.id;
			this.$emit('scheduleTap', id);
		},
		gotoToday : function(){
			var dateObj        = new Date();
			this.cYear         = Number(dateObj.getFullYear());
			this.cMonth        = Number(dateObj.getMonth() + 1);
			this.cMonthStr     = this.cMonth < 10 ? '0' + this.cMonth : this.cMonth;
			this.cDay          = dateObj.getDate();
			this.cDay          = this.cDay < 10 ? '0' + this.cDay : this.cDay;
			this.currentDayIn  = this.cYear + '-' + this.cMonthStr + '-' + this.cDay;
			this.changeMonth();
			this.getSchedulesIn();
			this.$emit('gotoToday', this.currentDayIn);
		}
	}
}
</script>
<style scoped>
.gui-schedule-wrap{width:690rpx;}
.gui-schedule-header-date{height:88rpx; line-height:88rpx; color:#2B2E3D; font-size:32rpx;}
.gui-schedule-7item{width:98rpx; margin-bottom:22rpx; position:relative;}
.gui-schedule-weeks{width:98rpx; height:88rpx; font-size:26rpx; line-height:88rpx; text-align:center;}
.gui-date-ditems{width:82rpx; height:82rpx; border-radius:80rpx;}
.gui-d-current-txt{color:#FFFFFF !important;}
.gui-date-day{height:32rpx; line-height:32rpx; text-align:center; font-size:28rpx;}
.gui-date-nl{height:24rpx; line-height:26rpx; color:#888888; font-size:20rpx; text-align:center;}
.gui-schedule-line{height:20rpx; border-color:#F8F8F8;}
.gui-schedule-time-list{margin-top:20rpx;}
.gui-schedule-timer{width:88rpx; font-size:22rpx; line-height:36rpx;}
.gui-schedule-body{width:200rpx; flex:1; border-color:#F8F8F8; margin-top:15rpx;}
.gui-schedules{padding:10rpx; line-height:30rpx; font-size:22rpx; margin-top:15rpx; border-radius:8rpx;}
.gui-schedule-time-list-wrap{padding:20rpx;}
.gui-schedule-today{line-height:50rpx; height:50rpx; font-size:22rpx; color:#828282; padding-left:20rpx; padding-right:20rpx; border-color:#F1F2F3;}
.gui-schedule-point{width:18rpx; height:18rpx; border-radius:10rpx; background-color:#FF0036; position:absolute; right:6rpx; top:6rpx;}
</style>