<template>
  <div id="app">
    <section class="header">
      <md-field>
        <md-textarea cols="10" md-counter v-model="newClip"></md-textarea>
      </md-field>
      <md-button class="md-raised" @click="clearNewClip">清空</md-button>
      <md-button class="md-raised md-primary">添加</md-button>
    </section>

    <section class="main">
      <div class="clips">
        <div v-for="clip in clips" class="clip" :key="clip.id">
          <md-card md-with-hover>
            <md-card-content>{{ clip.text }}</md-card-content>
            <md-card-actions>
              <md-button class="md-raised md-primary">复制</md-button>
              <md-button class="md-accent md-raised">删除</md-button>
            </md-card-actions>
          </md-card>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data: function() {
    return {
      clips: [
        { id: 1, text: "git@github.com:Orenoid/online-clipboard.git" },
        { id: 2, text: "aaSELECT t1.company_id, t1.sales_plan_id, t1.seller_id, t1.marketplace_id, t1.plan_name, t1.plan_time, t1.username, t1.builder, t1.sales_volume, t1.sales_amount, t1.create_type FROM (SELECT * FROM dim_sales_plan WHERE username IN ('sandra.tan@loftk.us','tim.huang@loftk.us')) t1 WHERE company_id = 1 ORDER BY plan_time DESC" }
      ],
      newClip: ""
    };
  },
  created: function() {
    axios;
    document.title = "Online Clipboard";
  },
  methods: {
    addClip: function() {},
    clearNewClip: function() {
      this.newClip = "";
    }
  }
};
</script>

<style>

.md-textarea {
  resize: none;
}

</style>
