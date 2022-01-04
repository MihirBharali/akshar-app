<template>

  <div
    :class="`tag ${className}`" 
    :draggable="true"
    @dragstart.stop="handleDragStart($event)"
  >
    {{ label }} 
    <br>
    <div :class="userDetailSpanClassname">
      {{ gender }} 
      <span v-if="hasPhysicalFacilityLevel">, {{ physical_facility_level }}</span>
    </div>

  </div>

</template>
<script>

  import { USER_DETAILS_CLASSNAME } from '../constants';

  export default {
    name: 'Tag',
    props: ['id', 'label', 'gender', 'physical_facility_level', 'className', 'index'],
    data() {
      return {
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
        const transferObject = {
          userId: this.id,
          userGender: this.gender,
          userPhysicalFacilityLevel: this.physical_facility_level,
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

  .user-details {
    font-size: 10px;
  }

</style>