<template>

  <BaseCard
    :className="`${mentorCardClassname} ${draggedMentorClassname}`"
    :isDraggable="true"
    :onDragStartHandler="handleDragStart"
    :onDropHandler="handleDrop"
  >

    <div slot="header" class="header">
      {{ name }}
      <KIconButton
        v-if="emptyMenteeList"
        class="icon"
        icon="close" 
        appearance="flat-button"
        size="mini"
        :tooltip="$tr('clearMentor')"
        @click="handleMentorRemove"
      />
      <br>
      <div :class="userDetailSpanClassname">
        {{ gender }} 
        <span v-if="hasPhysicalFacilityLevel">, {{ physical_facility_level }}</span>
      </div>

    </div>

    <div slot="content">
      <MenteeCard 
        v-for="(mentee, menteeIndex) in mentees"
        :id="mentee.id"
        :key="mentee.id"
        :gender="mentee.gender"
        :physical_facility_level="mentee.physical_facility_level"
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
    USER_DETAILS_CLASSNAME,
  } from '../constants';
  import BaseCard from './BaseCard';
  import MenteeCard from './MenteeCard';

  export default {
    name: 'MentorCard',
    components: { BaseCard, MenteeCard },
    props: [
      'id',
      'name',
      'gender',
      'physical_facility_level',
      'index',
      'mentees',
      'supervisorId',
      'supervisorIndex',
    ],
    emits: ['mentor-mentee-match-up-update', 'unassigned-mentee-added'],
    data() {
      return {
        draggedMentorClassname: '',
        mentorCardClassname: MENTOR_CARD_CLASSNAME,
        userDetailSpanClassname: USER_DETAILS_CLASSNAME,
      };
    },
    computed: {
      hasPhysicalFacilityLevel() {
        return this.physical_facility_level != undefined;
      },
      emptyMenteeList() {
        return Object.keys(this.mentees).length == 0;
      },
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
        console.log('Handling addition of mentee');
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
          console.log(transferDataObj);
          evt.stopPropagation();
          try {
            transferDataObj = { ...transferDataObj, ...JSON.parse(transferData) };
            this.$emit('unassigned-mentee-added', transferDataObj);
          } catch {}
        }
      },
      handleMentorRemove() {
        console.log('Removing mentor');
        const data = {
          mentorId: this.id,
          originMentorIndex: this.index,
          originSupervisorId: this.supervisorId,
          originSupervisorIndex: this.supervisorIndex,
        };
        this.$emit('remove-mentor', data);
      },
    },
    $trs: {
      clearMentor: { message: 'Remove Mentor' },
    },
  };

</script>

<style lang="scss" scoped>

  .header {
    margin: 0.4rem;
  }
  .mentor-card {
    position: relative;
    justify-content: space-between;
    min-height: 4rem;
    padding: 0.4rem;
    font-weight: bold;
    color: #6d4cd4;
    background-color: white;
    border-radius: 1rem;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
  }
  .user-details {
    font-size: 10px;
  }

  .icon {
    position: absolute;
    top: 0.4rem;
    right: 0.4rem;
    cursor: pointer;
  }

</style>