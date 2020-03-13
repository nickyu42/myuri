<template>
  <div class="reader">

    <v-app-bar
        hide-on-scroll="true"
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
          src=""
          max-width="700"
        >

        </v-img>
      </v-row>

      <v-row>
        <v-pagination></v-pagination>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: 'Reader',
  components: {
  },
  data: () => ({
    drawer: false,
  }),
}
</script>
