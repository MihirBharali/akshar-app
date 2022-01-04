<template>

  <div :class="`unassigned-user-container ${className}`">
    <div class="container-label">
      {{ containerLabel }}
    </div>
    <div v-if="isUsersEmpty" class="no-user-label">
      {{ $tr('noUserLabel') }}
    </div>
    <div v-if="!isUsersEmpty" class="list">
      <Tag 
        v-for="(user, index) in users"
        :id="user.id"
        :key="user.id"
        :index="index"
        :label="user.name"
        :gender="user.gender"
        :physical_facility_level="user.physical_facility_level"
        :className="className"
      />
    </div>
  </div>

</template>

<script>

  import _isEmpty from 'lodash/isEmpty';
  import _isNil from 'lodash/isNil';
  import Tag from './Tag';

  export default {
    name: 'UnassignedUserContainer',
    components: { Tag },
    props: ['className', 'containerLabel', 'users'],
    data() {
      return {};
    },
    computed: {
      isUsersEmpty() {
        return _isEmpty(this.users) || _isNil(this.users);
      },
    },
    $trs: {
      noUserLabel: { message: 'No users found' },
    },
  };

</script>

<style lang="scss" scoped>

  .unassigned-user-container {
    margin-top: 1rem;
  }

  .tag.unassigned-mentors {
    color: #6d4cd4;
    background-color: #d7d1eb;
  }

  .tag.unassigned-mentees {
    color: #61ac0d;
    background-color: #d9e9c6;
  }

  .no-user-label {
    font-size: 0.75rem;
    font-weight: bold;
  }

  .container-label {
    font-size: 0.9rem;
  }

</style>