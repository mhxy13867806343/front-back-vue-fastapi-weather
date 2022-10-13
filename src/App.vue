<template>
  <div id="app">
    <keep-alive>
      <router-view v-if="$route.meta.keepAlive"></router-view>
    </keep-alive>
    <router-view v-if="!$route.meta.keepAlive"></router-view>
  </div>
</template>
<script>
  import '.env.js'
  const pageJson = require('@/static/pages.json')
  export default {
    methods: {
    },
    // #ifdef  H5
    globalData: process.uniEnv,
    onLaunch: function () {
    },
    // #endif
    onShow: function () {},
    onHide: function () {},
  }
</script>
<style>
/*每个页面公共css */
/* 加载框架核心样式 */
@import "./GraceUI5/css/graceUI.css";
/* 加载主题样式 */
@import "./GraceUI5/skin/v1.css";
/* 加载图标字体 - 条件编译模式 */
/* #ifdef APP-PLUS-NVUE */
.gui-icons{font-family:graceIconfont;}
/* #endif */
</style>
<style lang="scss">
  /* 注意要写在第一行，同时给style标签加入lang="scss"属性 */
  @import 'uview-ui/index.scss';
</style>
