<template>

  <CoreBase
    :immersivePage="false"
    :appBarTitle="$tr('wageLabel')"
    :authorized="$store.getters.userIsAuthorizedForCoach"
    authorizedRole="adminOrCoach"
    :showSubNav="false"
    :pageTitle="$tr('wageLabel')"
  >
    <p>
      <BackLink
        :to="classListLink"
        :text="$tr('allClassesLabel')"
      />
    </p>
    <CoachRequestsBlock />
    <CoachLearnerRequestsBlock />
  </CoreBase>

</template>
<script>

  import CoreBase from 'kolibri.coreVue.components.CoreBase';
  import { mapState } from 'vuex';
  import commonCoach from '../common';
  import CoachRequestsBlock from './CoachRequestsBlock.vue';
  import CoachLearnerRequestsBlock from './CoachLearnerRequestsBlock.vue';

  export default {
    name: 'CoachLearnerWageList',
    components: {
      CoreBase,
      CoachRequestsBlock,
      CoachLearnerRequestsBlock,
    },
    mixins: [commonCoach],
    computed: {
      ...mapState('wage', ['coachWageRequests']),
      transactions() {
        return this.coachWageRequests;
      },
      classListLink() {
        let facility_id;
        if (this.$store.getters.userIsMultiFacilityAdmin) {
          facility_id = this.$store.state.classSummary.facility_id;
        }
        return this.$router.getRoute('CoachClassListPage', {}, { facility_id });
      },
    },
    methods: {},
    $trs: {
      allClassesLabel: 'All Classes',
      wageLabel: 'Wage',
      pageTitle: 'Wage details',
      searchNoResultText: 'You do not have any requests',
    },
  };

</script>
<style lang='scss' scoped>

  .move-down {
    position: relative;
    margin-top: 24px;
  }

</style>
