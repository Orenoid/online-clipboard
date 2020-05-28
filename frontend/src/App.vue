<template>
  <div id="app">
    <section class="header">
      <md-textarea cols="10" md-counter v-model="newClipText"></md-textarea>
      <md-button class="md-raised" @click="clearNewClipText">清空</md-button>
      <md-button class="md-raised md-primary" @click="addClip">添加</md-button>
    </section>

    <section class="main">
      <div class="clips">
        <div v-for="clip in clips" class="clip" :key="clip.id">
          <md-card>
            <md-card-content v-clipboard:copy="clip.text">{{ clip.text }}</md-card-content>
            <div class="clip-actions">
              <md-button class="md-raised md-primary" v-clipboard:copy="clip.text">复制</md-button>
              <md-button class="md-raised" @click="removeClip(clip)">
                <v-icon>mdi-delete</v-icon>
              </md-button>
            </div>
          </md-card>
        </div>
      </div>
    </section>

    <section class="footer"></section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data: function() {
    return {
      clips: [],
      newClipText: ""
    };
  },
  created: async function() {
    let res = await axios.get("http://127.0.0.1:5000/clips");
    this.clips = res.data;
  },
  methods: {
    async addClip() {
      if (this.newClipText.length == 0) {
        return;
      }
      let json = { text: this.newClipText };
      let res = await axios.post("http://127.0.0.1:5000/clips", json);
      let newClipObj = res.data;
      this.clips.push(newClipObj);
      this.newClipText = "";
    },
    async removeClip(clip) {
      await axios.delete("http://127.0.0.1:5000/clips", {
        params: { id: clip.id }
      });
      this.clips.splice(this.clips.indexOf(clip), 1);
    },
    async clearClipboard() {
      await axios.delete("http://127.0.0.1:5000/clips");
      this.clips = [];
    },
    clearNewClipText: function() {
      this.newClipText = "";
    }
  }
};
</script>

<style scoped>
#app {
  width: 70%;
}

#app .md-textarea {
  display: block;
  margin: 30px 0px 0px 0px;
  background-color: aliceblue;
  resize: none;
}

#app .main .clip {
  margin-top: 20px;
}

#app .main .clip-actions {
  position: absolute;
  top: 10px;
  right: 10px;
}

#app .md-card-content {
  padding: 30px 0px 30px 30px;
}
</style>


<style>
body {
  background-color: #e9ecef;
}
</style>