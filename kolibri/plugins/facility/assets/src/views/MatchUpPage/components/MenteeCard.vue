<template>

  <div
    :class="menteeCardClassname" 
    :draggable="true"
    @dragstart.stop="handleDragStart"
  >
    <div>{{ name }}</div>
    <KIconButton
      icon="close" 
      appearance="flat-button"
      size="mini"
      :tooltip="$tr('clearMentee')"
      @click="handleMenteeRemove"
    />
  </div>

</template>

<script>

  import { MENTEE_CARD_CLASSNAME } from '../constants';

  export default {
    name: 'MenteeCard',
    props: ['name', 'id', 'mentorId', 'mentorIndex', 'supervisorId', 'supervisorIndex'],
    data() {
      return {
        menteeCardClassname: MENTEE_CARD_CLASSNAME,
      };
    },
    methods: {
      handleDragStart(evt) {
        evt.stopPropagation();
        this.draggedMenteeClassname = 'dragged-mentee';
        evt.dataTransfer.dropEffect = 'move';
        evt.dataTransfer.effectAllowed = 'move';
        const transferData = {
          menteeId: this.id,
          originMentorId: this.mentorId,
          originMentorIndex: this.mentorIndex,
          originSupervisorId: this.supervisorId,
          originSupervisorIndex: this.supervisorIndex,
        };
        evt.dataTransfer.setData('className', MENTEE_CARD_CLASSNAME);
        evt.dataTransfer.setData('transferData', JSON.stringify(transferData));
      },
      handleMenteeRemove() {
        const data = {
          menteeId: this.id,
          originMentorId: this.mentorId,
          originMentorIndex: this.mentorIndex,
          originSupervisorId: this.supervisorId,
          originSupervisorIndex: this.supervisorIndex,
        };
        this.$emit('remove-mentee', data);
      },
    },
    $trs: {
      clearMentee: { message: 'Remove Mentee' },
    },
  };

</script>

<style lang="scss" scoped>

  .mentee-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.4rem;
    margin: 0.4rem;
    font-size: 13px;
    font-weight: bold;
    color: #61ac0d;
    text-align: center;
    white-space: normal;
    cursor: pointer;
    background-color: #d9e9c6;
    border-radius: 1rem;
  }

  button {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 20px !important;
    min-width: unset !important;
    height: 20px !important;
    border-radius: 100% !important;
  }

</style>