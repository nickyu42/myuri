<template>
  <div class="reader">
    <v-container>
      <v-row
        justify="center"
      >
        <v-img
          v-bind:src="imageURL"
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

export default Vue.extend({
  name: 'Reader',

  data: () => ({
    window: {
      width: 0,
      maxWidth: 700,
      height: 0,
    },

    settings: {
      fitWidth: false,
    },

    totalPages: 177,
    currentComic: 1,
    currentChapter: "1",
    currentPage: 0,
    imageURL: "",

    // current comic meta
    // TODO make some sort of data store with Vuex?
    comicMetadata: {},
    chapterMetadata: {},
    apiInstance: Api.getInstance("http://myuri.njkyu.com/api"),
  }),

  created() {
    // add event handlers
    window.addEventListener('resize', this.handleResize);
    window.addEventListener('keydown', this.keyHandler);
    this.handleResize();

    // get metadata
    this.apiInstance.getComicInfo(this.currentComic).then((response) => this.comicMetadata = response);
    // this.apiInstance.getChapterInfo(this.currentChapter).then((response) => this.chapterMetadata = response);
    
    // set page
    this.changePage(this.currentPage);
  },

  destroyed() {
    // remove event handlers
    window.removeEventListener('resize', this.handleResize);
    window.removeEventListener('keydown', this.keyHandler);
    this.handleResize();
  },

  methods: {
    handleResize() {
      this.window.width = window.innerWidth;
      this.window.height = window.innerHeight;
    },

    keyHandler(event: Event) {
      if (event instanceof KeyboardEvent) {
        if (event.key == "ArrowLeft") 
          this.handleKeyLeft();

        if (event.key == "ArrowRight")
          this.handleKeyRight();

      }
    },

    handleKeyRight() {
      if (this.currentPage < this.totalPages) {
        this.currentPage += 1;
        this.changePage(this.currentPage);
      }
    },

    handleKeyLeft() {
      if (this.currentPage > 0) {
        this.currentPage -= 1;
        this.changePage(this.currentPage);
      }
    },
    
    changePage(page: number) {
      const imagePromise = this.apiInstance.getPage(this.currentComic, this.currentChapter, page);
      imagePromise.then((blob) => {
        const url = URL.createObjectURL(blob);
        this.imageURL = url;
      });
    }
  }
});

</script>
