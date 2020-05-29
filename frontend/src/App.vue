<template>
  <div id="app">
    <section class="header">
      <md-field>
        <md-textarea cols="10" md-counter v-model="newClipText"></md-textarea>
      </md-field>
      <md-button class="md-raised" @click="clearNewClipText">清空</md-button>
      <md-button class="md-raised md-primary" @click="addClip">添加</md-button>
    </section>

    <section class="main">
      <div class="clips">
        <div v-for="clip in clips" class="clip" :key="clip.id">
          <md-card md-with-hover>
            <md-card-content v-clipboard:copy="clip.text" @click="showCopiedMsg()">{{ clip.text }}</md-card-content>
            <div class="clip-actions">
              <md-button
                class="md-raised md-primary"
                v-clipboard:copy="clip.text"
                @click="showCopiedMsg()"
              >复制</md-button>
              <md-button class="md-raised" @click="removeClip(clip)">
                <v-icon>mdi-delete</v-icon>
              </md-button>
            </div>
          </md-card>
        </div>
      </div>
    </section>

    <section class="footer">
      <md-button class="md-accent md-raised" @click="clearClipboard">删除全部</md-button>
    </section>

    <md-snackbar
      :md-active.sync="snackbarConfig.showSnackBar"
      :md-duration="snackbarConfig.duration"
      md-position="center"
    >
      <span>{{ snackbarConfig.message }}</span>
    </md-snackbar>
  </div>
</template>

<script>
import axios from "@/modules/request";
import eventBus from "@/modules/event-bus";

export default {
  name: "App",
  data: function() {
    return {
      clips: [],
      newClipText: "",
      snackbarConfig: {
        showSnackBar: false,
        message: "",
        duration: 4000
      }
    };
  },
  mounted: function() {
    eventBus.$on("global-snackbar-message", eventArgs => {
      this.snackbarConfig.message = eventArgs.message;
      this.snackbarConfig.showSnackBar = true;
    });
  },
  created: async function() {
    let res = await axios.get("/clips");
    this.clips = res.data;
    // this.sortClips();
  },
  methods: {
    async addClip() {
      if (this.newClipText.length == 0) {
        return;
      }
      let json = { text: this.newClipText };
      let res = await axios.post("/clips", json);
      let newClipObj = res.data;
      this.clips.push(newClipObj);
      // this.sortClips();
      console.log(this.clips);
      this.newClipText = "";
    },
    async removeClip(clip) {
      await axios.delete("/clips", {
        params: { id: clip.id }
      });
      this.clips.splice(this.clips.indexOf(clip), 1);
    },
    async clearClipboard() {
      await axios.delete("/channel/clips");
      this.clips = [];
    },
    clearNewClipText: function() {
      this.newClipText = "";
    },
    sortClips: function() {
      this.clips.sort(function(a, b) {
        return a.id < b.id ? 1 : -1;
      });
    },
    showCopiedMsg: function(message = "已复制到粘贴板") {
      eventBus.$emit("global-snackbar-message", { message: message });
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
  /* margin: 30px 0px 0px 0px; */
  resize: none;
}

#app .main .clip {
  margin-top: 20px;
}

#app .md-card-content {
  white-space: pre-wrap;
  padding: 50px 0px 50px 50px;
}

#app .footer {
  margin-top: 30px;
}
</style>


<style>
body {
  background-color: #e9ecef;
}
</style>