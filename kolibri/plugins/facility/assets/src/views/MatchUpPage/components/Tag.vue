<template>

  <div
    :class="`tag ${className}`" 
    :draggable="true"
    @dragstart.stop="handleDragStart($event)"
  >
    {{ label }}
  </div>

</template>
<script>

  export default {
    name: 'Tag',
    props: ['id', 'label', 'className', 'index'],
    data() {
      return {};
    },
    methods: {
      handleDragStart(evt) {
        const transferObject = {
          userId: this.id,
          userName: this.label,
          userIndex: this.index,
        };
        evt.dataTransfer.setData('className', this.className);
        evt.dataTransfer.setData('transferData', JSON.stringify(transferObject));
      },
    },
  };

</script>

<style lang="scss" scoped>

  .tag {
    display: inline-block;
    padding: 0.4rem 1rem;
    margin: 0.2rem;
    font-size: 13px;
    font-weight: bold;
    white-space: normal;
    border-radius: 1rem;
  }

</style>