<template>
  <div class="reader">

    <v-app-bar
        :hide-on-scroll="true"
        dark
      >
        <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>
  
        <v-toolbar-title>Myuri</v-toolbar-title>

        <v-spacer></v-spacer>

        <v-btn icon>
          <v-icon>mdi-magnify</v-icon>
        </v-btn>

    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      absolute
      temporary
    >
      <v-list
        nav
        dense
      >
        <v-list-item-group
          v-model="group"
        >
          <v-list-item>
            <v-list-item-icon>
              <v-icon>mdi-home</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item>

        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <v-container>
      <v-row
        justify="center"
      >
        <v-img
          v-bind:src="readerInstance.getImage()"
          v-on:input="changePage"
          v-bind:max-width="settings.fitWidth ? window.width : window.maxWidth"
        >

        </v-img>
      </v-row>

      <v-row>
        <v-pagination></v-pagination>
      </v-row>
    </v-container>
  </div>
</template>

<script lang=ts>
import Vue from "vue";
import { Api } from "../ts_lib/api";
import { Reader } from "../ts_lib/reader";

export default Vue.extend({
  name: 'Reader',

  data: () => ({
    drawer: false,

    window: {
      width: 0,
      maxWidth: 700,
      height: 0,
    },

    settings: {
      fitWidth: false,
    },

    apiInstance: Api.getInstance("http://myuri.njkyu.com/api"),
    readerInstance: new Reader(),
  }),

  created() {
    window.addEventListener('resize', this.handleResize);
    this.handleResize();

    this.changePage(1);

    // this.apiInstance.getInfo(1).then((response) => console.log(response))
  },

  destroyed() {
    window.addEventListener('resize', this.handleResize);
    this.handleResize();
  },

  methods: {
    handleResize() {
      this.window.width = window.innerWidth;
      this.window.height = window.innerHeight;
    },
    
    changePage(page: number) {
      const url: string = "http://myuri.njkyu.com/api/c/1/1/" + page.toString();
      this.readerInstance.setImage(url);
    }
  }
});

</script>
