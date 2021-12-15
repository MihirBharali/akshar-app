<template>

  <div>
    <KRouterLink
      :text="$tr('wagesHomePage')"
      :to="$store.getters.facilityPageLinks.WageDetails"
      icon="back"
    />

    <FacilityConsolidatedChartPage />
    <FacilityLearnersReportChart />

  </div>

</template>


<script>

  import { mapState } from 'vuex';
  import FacilityConsolidatedChartPage from './FacilityConsolidatedChart.vue';
  import FacilityLearnersReportChart from './FacilityLearnersReportChart.vue';

  export default {
    name: 'FacilityWageReportingPage',
    components: { FacilityConsolidatedChartPage, FacilityLearnersReportChart },
    mixins: [],
    computed: {
      ...mapState('wage', ['facilityWageRequests']),
    },
    beforeMount() {},
    data() {
      return {};
    },
    methods: {},
    $trs: {
      wagesHomePage: 'Wages Home',
    },
  };

</script>


<style lang="scss" scoped>

</style>
