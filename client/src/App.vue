<template>
  <v-app>
    <v-content>
      <reader/>
    </v-content>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';
import Reader from "./components/Reader.vue";

export default Vue.extend({
  name: 'App',

  components: {
    Reader
  },

  data: () => ({
    //
  }),
});
</script>
