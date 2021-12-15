<template>

  <div>
    <KRouterLink
      :text="$tr('wagesHomePage')"
      :to="$store.getters.facilityPageLinks.WageDetails"
      icon="back"
    />
    <FacilityRequestsBlock />
    <FacilityLearnerRequestsBlock />
  </div>

</template>


<script>

  import FacilityRequestsBlock from './FacilityRequestsBlock.vue';
  import FacilityLearnerRequestsBlock from './FacilityLearnerRequestsBlock.vue';

  export default {
    name: 'FacilityWageManagePage',
    components: { FacilityRequestsBlock, FacilityLearnerRequestsBlock },
    computed: {},
    beforeMount() {},
    methods: {},
    $trs: {
      wagesHomePage: 'Wages Home',
    },
  };

</script>


<style lang="scss" scoped>

</style>
