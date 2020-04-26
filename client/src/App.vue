<template>
  <v-app>
    <navigation/>

    <v-content>
      <reader/>
    </v-content>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';
import Reader from "./components/Reader.vue";
import Navigation from "./components/Navigation.vue";

export default Vue.extend({
  name: 'App',

  components: {
    Reader,
    Navigation
  },

  data: () => ({
    //
  }),
});
</script>
