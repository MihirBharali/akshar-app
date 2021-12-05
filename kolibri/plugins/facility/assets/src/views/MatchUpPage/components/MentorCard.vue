<template>

  <BaseCard
    :className="`${mentorCardClassname} ${draggedMentorClassname}`"
    :isDraggable="true"
    :onDragStartHandler="handleDragStart"
    :onDropHandler="handleDrop"
  >
    <div slot="header" class="header">
      {{ name }}
    </div>
    <div slot="content">
      <MenteeCard 
        v-for="(mentee, menteeIndex) in mentees"
        :id="mentee.id"
        :key="mentee.id"
        :index="menteeIndex"
        :name="mentee.name"
        :mentorId="id"
        :mentorIndex="index"
        :supervisorId="supervisorId"
        :supervisorIndex="supervisorIndex"
        @remove-mentee="data => $emit('remove-mentee', data)"
      />
    </div>
  </BaseCard>

</template>
<script>

  import _includes from 'lodash/includes';

  import {
    MENTOR_CARD_CLASSNAME,
    MENTEE_CARD_CLASSNAME,
    UNASSIGNED_MENTEES_CLASSNAME,
  } from '../constants';
  import BaseCard from './BaseCard';
  import MenteeCard from './MenteeCard';

  export default {
    name: 'MentorCard',
    components: { BaseCard, MenteeCard },
    props: ['id', 'name', 'index', 'mentees', 'supervisorId', 'supervisorIndex'],
    emits: ['mentor-mentee-match-up-update', 'unassigned-mentee-added'],
    data() {
      return {
        draggedMentorClassname: '',
        mentorCardClassname: MENTOR_CARD_CLASSNAME,
      };
    },
    methods: {
      handleDragStart(evt) {
        evt.stopPropagation();
        this.draggedMentorClassname = 'dragged-mentor';
        evt.dataTransfer.dropEffect = 'move';
        evt.dataTransfer.effectAllowed = 'move';
        const transferData = {
          mentorId: this.id,
          originSupervisorId: this.supervisorId,
          originSupervisorIndex: this.supervisorIndex,
        };
        evt.dataTransfer.setData('className', MENTOR_CARD_CLASSNAME);
        evt.dataTransfer.setData('transferData', JSON.stringify(transferData));
      },
      handleDrop(evt) {
        const droppedItemClassname = evt.dataTransfer.getData('className');
        const transferData = evt.dataTransfer.getData('transferData');
        let transferDataObj = {
          destinationMentorId: this.id,
          destinationMentorIndex: this.index,
          destinationSupervisorId: this.supervisorId,
          destinationSupervisorIndex: this.supervisorIndex,
        };

        if (droppedItemClassname === MENTEE_CARD_CLASSNAME) {
          evt.stopPropagation();
          try {
            transferDataObj = { ...transferDataObj, ...JSON.parse(transferData) };
            this.$emit('mentor-mentee-match-up-update', transferDataObj);
          } catch {}
        }
        if (droppedItemClassname === UNASSIGNED_MENTEES_CLASSNAME) {
          evt.stopPropagation();
          try {
            transferDataObj = { ...transferDataObj, ...JSON.parse(transferData) };
            this.$emit('unassigned-mentee-added', transferDataObj);
          } catch {}
        }
      },
    },
  };

</script>

<style lang="scss" scoped>

  .header {
    margin: 1rem;
  }
  .mentor-card {
    min-height: 4rem;
    font-weight: bold;
    color: #6d4cd4;
    background-color: white;
    border-radius: 1rem;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
  }

</style>