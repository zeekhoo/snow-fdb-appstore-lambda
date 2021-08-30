<template>
  <div>
    <v-card class="pa-4" outlined flat>
      <div class="d-flex">
        <p class="overline pt-4 pr-4">Secure Join Settings</p>
        <div class="d-flex" v-if="saved">
          <v-icon color="green">mdi-weather-cloudy-arrow-right</v-icon>
          <div class="caption pt-6 pl-1 green--text">saving</div>
        </div>
      </div>
      <v-form ref="form" v-model="valid" lazy-validation>
        <v-row no-gutters>
          <v-col>
            <v-text-field
              class = "pr-4"
              v-model="binding.joinOn"
              label="Join On"
              required
              v-on:keyup="reset"
              :disabled="saved"
            ></v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              v-model="binding.commonSalt"
              label="Common Salt"
              required
              v-on:keyup="reset"
              :disabled="saved"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row no-gutters>
          <v-col>
            <v-text-field
              class = "pr-4"
              v-model="binding.secretMatchSalt"
              label="Secret Match Salt"
              required
              v-on:keyup="reset"
              :disabled="saved"
            ></v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              v-model="binding.secretNoMatchSalt"
              label="Secret No Match Salt"
              required
              v-on:keyup="reset"
              :disabled="saved"
            ></v-text-field>
          </v-col>
        </v-row>      
      </v-form>
    </v-card>
  </div>
</template>

<script>
import faunadb from "faunadb";

export default {
  name: "JoinSettings",
  data() {
    return {
      email: null,
      valid: true,
      binding: {},
      setTimeout: null,
      saved: false
    };
  },
  async mounted() {
    this.email = this.$root.$children[0].user;
    this.client = new faunadb.Client({
      headers: { "X-Fauna-Source": "faunaflix" },
      secret: process.env.VUE_APP_FAUNA_KEY
    });
    const q = faunadb.query;
    const res = await this.client.query(
      q.Call(q.Function('GetSecureJoinSettingsByOwner'), this.email)
    )
    this.binding = res.data;
  },
  methods: {
    reset() {
      this.typing = true;
      const self = this;
      const q = faunadb.query;
      if (this.setTimeout) {
        clearTimeout(this.setTimeout);
      }
      this.setTimeout = setTimeout(()=>{
        console.log(self.binding.joinOn);
        self.client.query(
          q.Call(q.Function('UpdateSecureJoinSettings'), self.email, self.binding)
        )
        self.saved = true;
        setTimeout(()=>{
          self.saved = false;
        }, 900)
      }, 600)
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
