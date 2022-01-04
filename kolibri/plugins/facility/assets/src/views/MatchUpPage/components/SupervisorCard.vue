<template>

  <BaseCard
    :className="`${supervisorCardClassname} ${selectedClassname}`"
    :isDraggable="false"
    :onDragEnterHandler="handleDragEnter" 
    :onDropHandler="handleDrop"
    :onDragLeaveHandler="handleDragLeave"
  >
    <template #header>
      <div class="supervisor-header">
        <div class="supervisor-icon">
          {{ $tr('supervisorLabel') }}
        </div>
        <div class="supervisor-label">
          {{ name }}
        </div>
      </div>
    </template>
    <template #content>
      <div>
        <MentorCard
          v-for="(supervisorMatchup, mentorIndex) in supervisorMatchups"
          :id="supervisorMatchup.mentor.id"
          :key="supervisorMatchup.mentor.id"
          :gender="supervisorMatchup.mentor.gender"
          :physical_facility_level="supervisorMatchup.mentor.physical_facility_level"
          :index="mentorIndex"
          :name="supervisorMatchup.mentor.name"
          :mentees="supervisorMatchup.mentee_list"
          :supervisorId="id"
          :supervisorIndex="index"
          @mentor-mentee-match-up-update=" data => $emit('mentor-mentee-match-up-update', data)"
          @unassigned-mentee-added=" data => $emit('unassigned-mentee-added', data)"
          @remove-mentee="data => $emit('remove-mentee', data)"
          @remove-mentor="data => $emit('remove-mentor', data)"
        />
      </div>
    </template>
  </BaseCard>

</template>

<script>

  import _noop from 'lodash/noop';
  import _includes from 'lodash/includes';

  import {
    SUPERVISOR_CARD_CLASSNAME,
    MENTOR_CARD_CLASSNAME,
    UNASSIGNED_MENTORS_CLASSNAME,
  } from '../constants';
  import BaseCard from './BaseCard';
  import MentorCard from './MentorCard';

  export default {
    name: 'SupervisorCard',
    components: { BaseCard, MentorCard },
    props: ['id', 'name', 'supervisorMatchups', 'index'],
    emits: [
      'supervisor-mentor-match-up-update',
      'unassigned-mentor-added',
      'unassigned-mentee-added',
    ],
    data() {
      return {
        selectedClassname: '',
        supervisorCardClassname: SUPERVISOR_CARD_CLASSNAME,
      };
    },
    methods: {
      handleDragEnter(evt) {
        evt.preventDefault();
        this.selectedClassname = 'selected-supervisor';
      },
      handleDragLeave(evt) {
        evt.preventDefault();
        this.selectedClassname = '';
      },
      handleDrop(evt) {
        evt.preventDefault();
        this.selectedClassname = '';
        const droppedItemClassname = evt.dataTransfer.getData('className');
        const transferData = evt.dataTransfer.getData('transferData');
        let transferDataObj = {
          destinationSupervisorId: this.id,
          destinationSupervisorIndex: this.index,
        };

        if (droppedItemClassname === MENTOR_CARD_CLASSNAME) {
          try {
            transferDataObj = { ...transferDataObj, ...JSON.parse(transferData) };
            this.$emit('supervisor-mentor-match-up-update', transferDataObj);
          } catch {}
        }

        if (droppedItemClassname === UNASSIGNED_MENTORS_CLASSNAME) {
          try {
            transferDataObj = { ...transferDataObj, ...JSON.parse(transferData) };
            this.$emit('unassigned-mentor-added', transferDataObj);
          } catch {}
        }
      },
    },
    $trs: {
      supervisorLabel: { message: 'Supervisor' },
    },
  };

</script>
<style lang="scss" scoped>

  .supervisor-header {
    padding: 0.4rem;
  }
  .supervisor-icon {
    display: inline-block;
    padding: 0.3rem 0.5rem;
    font-size: 10px;
    font-weight: bold;
    color: #f11313;
    background-color: #f0d6d6;
    border-radius: 1rem;
  }

  .supervisor-card {
    min-width: 10rem;
    background-color: #f5f5f5 !important;
    border-radius: 0.4rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  }

  .supervisor-card:hover {
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
  }

  .supervisor-label {
    margin: 0.4rem;
    font-weight: bold;
  }

</style>