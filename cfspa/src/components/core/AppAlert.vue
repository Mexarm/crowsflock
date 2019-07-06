<template>
  <v-alert error dismissible @input="onClose" :value="true" :type="type">
    {{ text }}
  </v-alert>
</template>

<script>
  export default {
    props: ['text', 'type'],
    methods: {
      onClose () {
        this.$emit('dismissed')
      }
    }
  }
</script>