<template>

  <Block
    :allLinkText="$tr('viewDetailsAction')"
    :allLinkRoute="$store.getters.facilityPageLinks.WageReportPage"
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
    name: 'FacilityWageReportBlock',
    components: {
      Block,
    },
    computed: {},
    $trs: {
      wageDetailsSubheader: 'View wage reports for your facility.',
      viewDetailsAction: 'View Details',
      wageDetailsLabel: 'Reports',
    },
  };

</script>


<style lang="scss" scoped>

</style>
