<template>

  <KPageContainer>
    <h1>
      <KLabeledIcon icon="device" :label="$tr('learnersMatchupHeader')" />
    </h1>
    <p>{{ $tr('learnersMatchupSubheader') }}</p>
    <br>
    <h2>{{ $tr('mentorTableHeader') }}</h2>
    <p v-if="!hasMentors">
      {{ $tr('noMentorLabel') }}
    </p>
    <LearnerMatchupTable
      v-else
      :tableHeaders="getMentorTableColumnHeaders()"
      :tableBodyData="mentorList"
    />
    <br>
    <h2>{{ $tr('menteeTableHeader') }}</h2>
    <p v-if="!hasMentees">
      {{ $tr('noMenteeLabel') }}
    </p>
    <LearnerMatchupTable
      v-else
      :tableHeaders="getMenteeTableColumnHeaders()"
      :tableBodyData="menteeList"
    />
  </KPageContainer>

</template>
<script>

  import _map from 'lodash/map';
  import _get from 'lodash/get';
  import _compact from 'lodash/compact';
  import _isEmpty from 'lodash/isEmpty';

  import { mapState } from 'vuex';
  import CoreTable from 'kolibri.coreVue.components.CoreTable';
  import { LEARNER_ROLES, LEARNER_MATCHUP_TABLE_COLUMNS } from '../constants';
  import LearnerMatchupTable from './LearnerMatchupTable.vue';

  export default {
    name: 'LearnerMatchupPage',
    components: { CoreTable, LearnerMatchupTable },
    computed: {
      ...mapState('classes', ['matchups']),
      menteeList() {
        return _compact(
          _map(this.matchups, matchup => {
            if (_get(matchup, 'role') === LEARNER_ROLES.MENTOR) {
              return {
                [LEARNER_MATCHUP_TABLE_COLUMNS.SUBJECT]: _get(matchup, 'subject', '-'),
                menteeId: _get(matchup, ['mentee_list', 'id'], '-'),
                [LEARNER_MATCHUP_TABLE_COLUMNS.MENTEE]: _get(matchup, ['mentee_list', 'name'], '-'),
                [LEARNER_MATCHUP_TABLE_COLUMNS.SUPERVISOR]: _get(
                  matchup,
                  ['supervisor', 'name'],
                  '-'
                ),
                role: _get(matchup, 'role'),
              };
            }
          })
        );
      },
      mentorList() {
        return _compact(
          _map(this.matchups, matchup => {
            if (_get(matchup, 'role') === LEARNER_ROLES.MENTEE) {
              return {
                [LEARNER_MATCHUP_TABLE_COLUMNS.SUBJECT]: _get(matchup, 'subject', '-'),
                mentorId: _get(matchup, ['mentor', 'id'], '-'),
                [LEARNER_MATCHUP_TABLE_COLUMNS.MENTOR]: _get(matchup, ['mentor', 'name'], '-'),
                [LEARNER_MATCHUP_TABLE_COLUMNS.SUPERVISOR]: _get(
                  matchup,
                  ['supervisor', 'name'],
                  '-'
                ),
                role: _get(matchup, 'role'),
              };
            }
          })
        );
      },
      hasMentees() {
        return !_isEmpty(this.menteeList);
      },
      hasMentors() {
        return !_isEmpty(this.mentorList);
      },
    },
    methods: {
      getMentorTableColumnHeaders() {
        return {
          [LEARNER_MATCHUP_TABLE_COLUMNS.SUBJECT]: this.$tr('subjectLabel'),
          [LEARNER_MATCHUP_TABLE_COLUMNS.MENTOR]: this.$tr('mentorLabel'),
          [LEARNER_MATCHUP_TABLE_COLUMNS.SUPERVISOR]: this.$tr('supervisorLabel'),
        };
      },
      getMenteeTableColumnHeaders() {
        return {
          [LEARNER_MATCHUP_TABLE_COLUMNS.SUBJECT]: this.$tr('subjectLabel'),
          [LEARNER_MATCHUP_TABLE_COLUMNS.MENTEE]: this.$tr('menteeLabel'),
          [LEARNER_MATCHUP_TABLE_COLUMNS.SUPERVISOR]: this.$tr('supervisorLabel'),
        };
      },
    },
    $trs: {
      learnersMatchupHeader: 'Learner matchup',
      learnersMatchupSubheader: 'Here you can find details of your matchup pairs.',
      subjectLabel: 'Subject',
      supervisorLabel: 'Supervisor',
      menteeLabel: 'Mentee',
      mentorLabel: 'Mentor',
      noMentorLabel: 'No mentors have been assigned to you.',
      noMenteeLabel: 'No mentees have been assigned to you.',
      mentorTableHeader: 'Your subjectwise mentors',
      menteeTableHeader: 'Your subjectwise mentees',
    },
  };

</script>
<style  lang="scss" scoped>
</style>
