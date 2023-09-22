<script setup>

</script>

<template>

  <div style="margin: 10px">

    <div>
      <router-link to="/api">CustomApiExample (自定义事件)</router-link>
    </div>
    <div>
      <router-link to="/">WindowEventExample (windows 窗口事件)</router-link>
    </div>
  </div>
  <div style="margin: 10px">
    <router-view></router-view>
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
