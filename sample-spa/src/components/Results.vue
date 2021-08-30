<template>
  <div class="pa-4">
    <div class="d-flex">
      <p class="overline pt-1">Results</p>
      <v-btn text @click="getData">
        <v-icon small>mdi-refresh</v-icon>
      </v-btn>
    </div>
    <v-simple-table>
      <template v-slot:default>
        <thead>
          <tr>
            <th class="text-left">User ID</th>
            <th class="text-left">Hashed Email</th>
            <th class="text-left">Link Id</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in data" :key="item.userId">
            <td>{{ item.userId }}</td>
            <td>{{ item.hashedEmail }}</td>
            <td>{{ item.linkId }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </div>
</template>

<script>
import faunadb from "faunadb";

export default {
  name: "Results",
  data() {
    return {
      client: null,
      data: []
    };
  },
  mounted() {
    this.client = new faunadb.Client({
      headers: { "X-Fauna-Source": "faunaflix" },
      secret: process.env.VUE_APP_FAUNA_KEY
    });

    this.getData()
  },
  methods: {
    async getData() {
      const q = faunadb.query;
      const res = await this.client.query(
        q.Call(q.Function('GetAllResults')) // call the GetAllResults UDF
      )
      this.data = res.data;
    }
  }
};
</script>
