<template>

  <KGrid gutter="16">
    <KGridItem :layout12="{ span: 6 }">
      <FacilityWageManageBlock />
    </KGridItem>
    <KGridItem :layout12="{ span: 6 }">

      <FacilityWageReportBlock />

    </KGridItem>
  </KGrid>

</template>


<script>

  import { mapState } from 'vuex';
  import FacilityWageManageBlock from './block/WageManageBlock.vue';
  import FacilityWageReportBlock from './block/WageReportingBlock.vue';

  export default {
    name: 'FacilityWagePage',
    components: { FacilityWageManageBlock, FacilityWageReportBlock },
    mixins: [],
    computed: {
      ...mapState('wage', ['facilityWageRequests']),
    },
    beforeMount() {
      this.init();
    },
    data() {
      return {};
    },
    methods: {
      init() {},
    },
    $trs: {},
  };

</script>


<style lang="scss" scoped>

</style>
