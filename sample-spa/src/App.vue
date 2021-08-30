<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <v-img
          alt="SnowflakeLogo"
          class="shrink mr-2"
          contain
          src="https://www.snowflake.com/wp-content/themes/snowflake/assets/img/logo-white.svg"
          transition="scale-transition"
          width="130"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="/"
        text
        >
        <span class="mr-2">{{user}}</span>
        <v-icon>mdi-account</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <JoinSettings/>
        <Results/>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import JoinSettings from './components/JoinSettings';
import Results from './components/Results';

export default {
  name: 'App',

  components: {
    JoinSettings,
    Results
  },

  data: () => ({
    user: 'zee.khoo@fauna.com'
  }),
};
</script>
