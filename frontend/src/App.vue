<template>
  <div id="app">
    <section class="header">
      <md-toolbar class="md-primary">
        <div class="md-toolbar-row">
          <div class="md-toolbar-section-start">
            <h3 class="md-title">Online Clipboard</h3>
          </div>
          <md-autocomplete
            md-input-placeholder="Search by channel name..."
            class="search"
            :md-options="[]"
            v-model="channelName"
            md-layout="box"
          ></md-autocomplete>
        </div>
      </md-toolbar>
    </section>

    <section class="main">
      <md-field md-clearable id="newClipTextField">
        <md-textarea autofocus cols="10" v-model="newClipText" @keyup.ctrl.enter="addClip"></md-textarea>
      </md-field>
      <div class="textarea-actions">
        <md-button class="md-raised md-primary" @click="addClip">添加</md-button>
      </div>
      <div class="clipboard-actions">
        <md-button class="md-accent md-raised" @click="clearClipboard">删除全部</md-button>
      </div>

      <div class="clips">
        <p class="current-channel-message">{{currentChannelMessage}}</p>
        <div
          v-for="clip in clips"
          class="clip"
          :key="clip.id"
          @click="showGlobalMessage('已复制到粘贴板')"
          @mouseenter="clip.hovered=true"
          @mouseleave="clip.hovered=false"
        >
          <md-card md-with-hover>
            <md-card-content v-clipboard:copy="clip.text">{{ clip.text }}</md-card-content>
            <div class="clip-actions" :style="{visibility: clip.hovered?'visible':'hidden'}">
              <span>
                <v-icon
                  v-clipboard:copy="clip.text"
                  @click.stop="showGlobalMessage('已复制到粘贴板')"
                >mdi-content-copy</v-icon>
                <md-tooltip md-direction="bottom" md-delay="500">复制文本</md-tooltip>
              </span>
              <span>
                <v-icon size="28px" @click.stop="removeClip(clip)">mdi-trash-can-outline</v-icon>
                <md-tooltip md-direction="bottom" md-delay="500">删除</md-tooltip>

              </span>
            </div>
          </md-card>
        </div>
      </div>
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
import _ from "lodash";

export default {
  name: "App",
  data: function() {
    return {
      clips: [],
      channelName: "",
      newClipText: "",
      snackbarConfig: {
        showSnackBar: false,
        message: "",
        duration: 1500
      }
    };
  },
  computed: {
    currentChannelMessage: function() {
      return this.channelName
        ? "当前所在频道：" + this.channelName
        : "当前正处于公开频道";
    }
  },
  mounted: function() {
    // 监听全局消息提醒事件
    eventBus.$on("global-snackbar-message", eventArgs => {
      this.snackbarConfig.message = eventArgs.message;
      this.snackbarConfig.showSnackBar = true;
    });
  },
  created: async function() {
    let clips = await this.getClipsFromApi(this.channelName);
    for (let clip of clips) {
      clip.hovered = false;
    }
    this.clips = clips;
    this.sortClips();
  },
  watch: {
    channelName: function(newChannelName) {
      this.refreshClipsByChannelName(newChannelName);
    }
  },
  methods: {
    async addClip() {
      if (!this.newClipText) return;
      let clipJson = { text: this.newClipText };
      if (this.channelName) clipJson.channel_name = this.channelName;
      let res = await axios.post("/clips", clipJson);
      let newClipObj = res.data;
      newClipObj.hovered = false;
      this.clips.push(newClipObj);
      this.sortClips();
      this.newClipText = "";
    },
    refreshClipsByChannelName: _.debounce(async function(channelName) {
      let clips = await this.getClipsFromApi(channelName);
      for (let clip of clips) {
        clip.hovered = false;
      }
      this.clips = clips;
      this.sortClips();
    }, 500),
    async getClipsFromApi(channelName = null) {
      if (channelName === "") channelName = null;
      let res = await axios.get("/clips", {
        params: { channel_name: channelName }
      });
      return res.data;
    },
    async removeClip(clip) {
      await axios.delete("/clips", {
        params: { id: clip.id }
      });
      this.clips.splice(this.clips.indexOf(clip), 1);
    },
    async clearClipboard() {
      // TODO channelName
      await axios.delete("/channel/clips", {
        params: { channel_name: this.channelName || null }
      });
      this.clips = [];
    },
    sortClips: function() {
      this.clips.sort(function(clipA, clipB) {
        return clipA.created_at > clipB.created_at ? -1 : 1;
      });
    },
    showGlobalMessage: function(message) {
      eventBus.$emit("global-snackbar-message", { message: message });
    }
  }
};
</script>

<style scoped>
#app {
  background-color: #fafafa;
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  width: 70%;
  margin: auto;
  overflow: auto;
}

#newClipTextField {
  background-color: white;
  margin: 20px 10px 0px 10px;
}

#app .main {
  margin-top: 40px;
}

#app .md-textarea {
  margin: 20px 10px 0 10px;
  display: block;
  resize: none;
}

#app .main .clip {
  margin: 20px 10px 0 10px;
}

#app .md-card-content {
  white-space: pre-wrap;
  padding: 50px 100px 50px 50px;
}

#app .footer {
  margin-top: 30px;
}

.md-toolbar-section-start {
  max-width: 200px;
  margin-right: 300px;
}

.search {
  margin-left: 200px;
  max-width: 400px;
}

.current-channel-message {
  margin-left: 20px;
  margin-top: 30px;
}

#app div .clip {
  position: relative;
}

#app .main .clips .clip .clip-actions {
  position: absolute;
  top: 20px;
  right: 20px;
}

#app .main .clips .clip .clip-actions .v-icon {
  margin-left: 10px;
  /* border: 2px #c5c5c5 solid; */
}
</style>


<style>
body {
  background-color: #adacac;
  overflow: auto;
}
</style>