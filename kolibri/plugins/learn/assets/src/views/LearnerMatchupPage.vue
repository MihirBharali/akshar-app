<template>

  <KPageContainer>
    <h2>
      <KLabeledIcon icon="device" :label="$tr('learnersMatchupHeader')" /> 
    </h2>
    <p> {{ subheaderText }}</p>
    <ul>
      <li> {{ subjectText }} </li>
      <li> {{ roleText }} </li>
    </ul>

    <CoreTable>
      <template #headers>
        <th> {{ supervisorLabel }} </th>
        <th v-if="isMentor">
          {{ menteeLabel }}
        </th>
        <th v-else>
          {{ mentorLabel }}
        </th> 
      </template>
      <template #tbody>
        <tbody>
          <tr>
            <td>
              {{ supervisor }}
            </td>
            <td v-if="isMentor">
              <ul>
                <li v-for="mentee in menteeList" :key="mentee">
                  {{ mentee }}


                </li>
              </ul>
            </td>    
            <td v-else>
              {{ mentor }}
            </td>
          </tr>
        </tbody>
      </template>
    </CoreTable>    

  </KPageContainer>    

</template>
<script>

  import { mapState } from 'vuex';
  import CoreTable from 'kolibri.coreVue.components.CoreTable';

  export default {
    name: 'LearnerMatchupPage',
    components: { CoreTable },
    computed: {
      ...mapState('classes', ['matchups']),

      subheaderText() {
        console.log(this.getSubject());
        return this.$tr('learnersMatchupSubheader', {
          subject: this.getSubject(),
        });
      },
      subjectText() {
        console.log(this.getSubject());
        return this.$tr('subjectDetails', {
          subject: this.getSubject(),
        });
      },
      roleText() {
        console.log(this.getSubject());
        return this.$tr('roleDetails', {
          role: this.role(),
        });
      },
      supervisorLabel() {
        return this.$tr('supervisorLabel');
      },
      menteeLabel() {
        return this.$tr('menteeLabel');
      },
      mentorLabel() {
        return this.$tr('mentorLabel');
      },
      isMentor() {
        console.log(this.role());
        if (this.role() === 'Mentor') {
          return true;
        }
        return false;
      },
      supervisor() {
        return this.matchups[0]['supervisor']['name'];
      },
      mentor() {
        return this.matchups[0]['mentor']['name'];
      },
      menteeList() {
        let menteeNames = [];
        for (var i in this.matchups[0]['mentee_list']) {
          let mentee = this.matchups[0]['mentee_list'][i];
          menteeNames.push(mentee['name']);
        }
        return menteeNames;
      },
    },
    methods: {
      getSubject() {
        return this.matchups[0]['subject'];
      },
      role() {
        return this.matchups[0]['role'];
      },
    },
    $trs: {
      subjectDetails: 'Subject : {subject}',
      roleDetails: 'Role : {role}',
      learnersMatchupHeader: 'Learner matchup',
      learnersMatchupSubheader: 'Please find details of your matchup pairs below.',
      supervisorLabel: 'Supervisor',
      menteeLabel: 'Mentees',
      mentorLabel: 'Mentor',
    },
  };

</script>
<style  lang="scss" scoped>

</style>
