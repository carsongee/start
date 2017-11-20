<template>
  <div id="app" :style="style">
    <router-view :config="config"/>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'app',
    computed: {
      style: function style() {
        if (this.config.background_img === undefined) return '';
        return `background: url(${this.config.background_img}) no-repeat center center fixed;`;
      },
    },
    data: function appData() {
      return {
        config: {},
      };
    },
    mounted: function mountedData() {
      const vthis = this;
      axios.get('/start-api/v1/config')
        .then((response) => {
          vthis.config = response.data;
        });
    },
  };
</script>

<style lang="scss">
  @import url('https://fonts.googleapis.com/css?family=Barlow+Semi+Condensed');
  @import url('https://fonts.googleapis.com/css?family=Slabo+27px');

  @import 'assets/scss/reset.scss';
  #app {
      min-height: 100vh;
      margin-bottom: -24px;
  }
  h1 {
      font-family: 'Barlow Semi Condensed', sans-serif;
  }
  body {
      font-family: 'Slabo 27px', serif;
      margin: 0;
  }
  
</style>
