<template>

  <Block
    :allLinkText="$tr('viewDetailsAction')"
    :allLinkRoute="classRoute('CoachLearnerWageList', {})"
    :showAllLink="true"
  >

    <template #title>
      <h2>{{ $tr('wageDetailsLabel') }}</h2>
    </template>

    {{ $tr('wageDetailsSubheader') }}

  </Block>

</template>


<script>

  import commonCoreStrings from 'kolibri.coreVue.mixins.commonCoreStrings';
  import commonCoach from './common';
  import Block from './home/HomePage/Block.vue';
  import BlockItem from './home/HomePage/BlockItem.vue';

  export default {
    name: 'WageBlock',
    components: {
      Block,
      BlockItem,
    },
    mixins: [commonCoach, commonCoreStrings],
    computed: {},
    $trs: {
      wageDetailsSubheader: 'Create and manage wage requests.',
      viewDetailsAction: 'View Details',
      wageDetailsLabel: 'Wages',
    },
  };

</script>


<style lang="scss" scoped>

</style>
