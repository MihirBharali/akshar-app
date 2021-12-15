<template>

  <KPageContainer>
    <h2>
      <KLabeledIcon icon="device" :label="$tr('learnersMatchupHeader')" /> 
    </h2>
    <p> {{ $tr('learnersMatchupSubheader') }}</p>

    <PaginatedListContainer
      :items="learnersListFilteredByDropdown"
      :filterPlaceholder="$tr('searchboxPlaceholderText')"
    >
      <template #otherFilter>
        <KSelect
          v-model="subjectFilter"
          label="Subject"
          :options="listOfSubjects"
          :inline="true"
          class="type-filter"
        />
      </template>

      <template #default="{ items }">
        <CoreTable
          :selectable="true"
          :emptyMessage="$tr('searchNoResultText')"
        >   

          <template #headers>
            <th class="table-header">
              {{ $tr('subjectLabel') }}
            </th>
            <th class="table-header">
              {{ $tr('mentorLabel') }}
            </th>
            <th class="table-header">
              {{ $tr('menteeLabel') }}
            </th>
          </template>
          <template #tbody>
            <tbody>
              <tr v-for="obj in items" :key="obj.mentee">
                <td class="table-data">
                  {{ obj.subject }}
                </td>  
                <td class="table-data">
                  {{ obj.mentor }}
                </td> 
                <td class="table-data">
                  {{ obj.mentee }}
                </td>    
              </tr>
            </tbody>    
          </template>    
        </CoreTable>
      </template>
    </PaginatedListContainer>
  </KPageContainer>

</template>

<script>

  import { mapState } from 'vuex';
  import commonCoreStrings from 'kolibri.coreVue.mixins.commonCoreStrings';
  import CoreBase from 'kolibri.coreVue.components.CoreBase';
  import CoreTable from 'kolibri.coreVue.components.CoreTable';
  import PaginatedListContainer from 'kolibri.coreVue.components.PaginatedListContainer';
  import commonCoach from '../common';

  export default {
    name: 'AllMatchupsList',
    components: {
      CoreBase,
      CoreTable,
      PaginatedListContainer,
    },
    mixins: [commonCoach, commonCoreStrings],
    computed: {
      ...mapState(['matchups']),
      listOfSubjects() {
        let options = [{ label: 'All', value: 'All' }];
        let keys = ['All'];
        let matchupDetails = this.matchups['match_up_details'];
        for (var index in matchupDetails) {
          if (keys.indexOf(matchupDetails[index]['subject'] == -1)) {
            let subject = matchupDetails[index]['subject'];
            options.push({ label: subject, value: subject });
            keys.push(subject);
          }
        }
        return options;
      },

      classListLink() {
        let facility_id;
        if (this.$store.getters.userIsMultiFacilityAdmin) {
          facility_id = this.$store.state.classSummary.facility_id;
        }
        return this.$router.getRoute('CoachClassListPage', {}, { facility_id });
      },
      learnersListFilteredByDropdown() {
        if (this.subjectFilter.value == 'All') {
          return this.listOfMatchups();
        }
        return this.listOfMatchups().filter(item => item['subject'] == this.subjectFilter.value);
      },
    },
    beforeMount() {
      this.subjectFilter = this.listOfSubjects[0];
    },
    methods: {
      listOfMatchups() {
        let matchupList = [];
        let matchups = this.$store.state.matchups['match_up_details'];
        for (var i in matchups) {
          let subject = matchups[i]['subject'];
          let pairs = matchups[i]['pairs'];
          for (var j in pairs) {
            let mentor = pairs[j]['mentor']['name'];
            let mentee = pairs[j]['mentee']['name'];
            let matchup = { subject: subject, mentor: mentor, mentee: mentee };
            matchupList.push(matchup);
          }
        }
        return matchupList;
      },
    },
    $trs: {
      allClassesLabel: {
        message: 'All classes',
        context: "Link to take coach back to the 'Classes' section.",
      },
      learnersMatchupHeader: {
        message: 'Learners matchup',
        context: 'Title for learners matchup section',
      },
      learnersMatchupSubheader: {
        message: 'Matchup pairs under your supervision.',
        context: 'Title for learners matchup section',
      },
      searchboxPlaceholderText: {
        message: 'Find students..',
        context: 'Search box placeholder',
      },
      searchNoResultText: {
        message: 'No users found for the provided search text.',
        context: 'Indicates no learner found matching the search text',
      },
      subjectLabel: {
        message: 'Subject',
        context: 'Indicates the coach who has recommended the learner for promotion',
      },
      mentorLabel: {
        message: 'Mentor',
        context: 'Indicates the coach who has recommended the learner for promotion',
      },
      menteeLabel: {
        message: 'Mentee',
        context: 'Indicates the coach who has recommended the learner for promotion',
      },
    },
  };

</script>


<style lang="scss" scoped>

  .table-header {
    padding: 24px 0;
  }
  .table-data {
    padding-top: 6px;
    vertical-align: middle;
  }
  .type-filter {
    margin-bottom: 0;
  }

</style>
