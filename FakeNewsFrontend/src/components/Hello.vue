<template>
  <div class="hello">
    <md-layout md-gutter>
      <md-layout class="layout">
        <md-whiteframe class="main">
          <form novalidate @submit.stop.prevent="submit">
            <md-input-container>
              <label>Initial value</label>
              <md-input v-model="inputUrl"></md-input>
              <md-button class="md-raised md-primary" type="submit">Send</md-button>
            </md-input-container>
            </br>
            {{ inputUrl }}
          </form>
        </md-whiteframe>
      </md-layout>
    </md-layout>
  </div>
</template>

<script>
export default {
  name: 'hello',
  data () {
    return {
      inputUrl: '',
      response: ''
    }
  },
  methods: {
    submit (event) {
      const api = 'http://localhost:8000'
      console.log('Api is ' + api)
      this.axios.get(api).then(response => {
        response = response.data
        console.log('Response success!')
      }).catch(error => {
        console.log('AJAX FAILED: ' + error)
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.layout {
  margin: auto;
}
.main {
  height: 200px;
  width: 400px;
}
</style>
