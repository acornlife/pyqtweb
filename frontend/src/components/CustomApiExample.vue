<template>
  <button type="button" @click="getUser">获取用户信息</button>
  <span>{{info}}</span>
</template>

<script setup>

import {UserInfo} from "../pyjs/custom.js";
import {ref} from "vue";

const info = ref('')
const getUser = () => {
  let userId = window.prompt('请输入用户id')
  UserInfo(userId).then(res => {
    info.value = JSON.stringify(res)
  })
}

</script>