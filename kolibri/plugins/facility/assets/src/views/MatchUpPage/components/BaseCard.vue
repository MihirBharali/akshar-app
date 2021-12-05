<template>

  <div
    :class="`base-card ${className}`"
    :draggable="isDraggable"
    @dragenter="onDragEnterHandler($event)"
    @dragstart="onDragStartHandler($event)"
    @drop="onDropHandler($event)"
    @dragleave="onDragLeaveHandler($event)"
    @dragover.prevent
  >
    <slot name="header"></slot>
    <slot name="content"></slot>
  </div>

</template>

<script>

  import _noop from 'lodash/noop';

  export default {
    name: 'BaseCard',
    props: {
      isDraggable: Boolean,
      className: String,
      onDragEnterHandler: {
        type: Function,
        default: _noop,
      },
      onDragStartHandler: {
        type: Function,
        default: _noop,
      },
      onDropHandler: {
        type: Function,
        default: _noop,
      },
      onDragLeaveHandler: {
        type: Function,
        default: _noop,
      },
    },
    data() {
      return {};
    },
  };

</script>

<style lang="scss" scoped>

  .base-card {
    padding: 0.4rem;
    margin: 0.4rem;
    font-size: 13px;
    white-space: normal;
  }

</style>