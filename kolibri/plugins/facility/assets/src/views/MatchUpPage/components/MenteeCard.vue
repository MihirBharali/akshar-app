<template>

  <div
    :class="menteeCardClassname" 
    :draggable="true"
    @dragstart.stop="handleDragStart"
  >  

    <div>

      {{ name }}<br>
      <div :class="userDetailSpanClassname">
        {{ gender }} 
        <span v-if="hasPhysicalFacilityLevel">, {{ physical_facility_level }}</span>
      </div>
    </div>
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

  import { MENTEE_CARD_CLASSNAME, USER_DETAILS_CLASSNAME } from '../constants';

  export default {
    name: 'MenteeCard',
    props: [
      'name',
      'id',
      'gender',
      'physical_facility_level',
      'mentorId',
      'mentorIndex',
      'supervisorId',
      'supervisorIndex',
    ],
    data() {
      return {
        menteeCardClassname: MENTEE_CARD_CLASSNAME,
        userDetailSpanClassname: USER_DETAILS_CLASSNAME,
      };
    },
    computed: {
      hasPhysicalFacilityLevel() {
        return this.physical_facility_level != undefined;
      },
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
    justify-content: space-between;
    padding: 0.4rem;
    margin: 0.4rem;
    font-size: 13px;
    font-weight: bold;
    color: #61ac0d;
    white-space: normal;
    cursor: pointer;
    background-color: #d9e9c6;
    border-radius: 0.5rem;
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
  .user-details {
    font-size: 10px;
  }

</style>