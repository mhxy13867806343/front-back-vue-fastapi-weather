import Vue from 'vue'
import App from './App'
Vue.config.productionTip = false
import uView from 'uview-ui'
import VueCompositionAPI from '@vue/composition-api';
import UniCompositionAPI from 'uni-composition-api';
Vue.use(VueCompositionAPI).use(UniCompositionAPI).use(uView)
App.mpType = 'app'

const app = new Vue({
  ...App,
})

app.$mount()
