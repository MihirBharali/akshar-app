<template>

  <Block
    :allLinkText="$tr('viewDetailsAction')"
    :allLinkRoute="$store.getters.facilityPageLinks.WageManagePage"
    :showAllLink="true"
  >

    <template #title>
      <h2>{{ $tr('wageDetailsLabel') }}</h2>
    </template>
    {{ $tr('wageDetailsSubheader') }}
  </Block>

</template>


<script>

  import Block from './Block.vue';

  export default {
    name: 'FacilityWageManageBlock',
    components: {
      Block,
    },
    computed: {},
    $trs: {
      wageDetailsSubheader: 'Create and manage wage requests.',
      viewDetailsAction: 'View Details',
      wageDetailsLabel: 'Manage',
    },
  };

</script>


<style lang="scss" scoped>

</style>
